import random
import re
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import (
    ChatMessage,
    Conversation,
    Customer,
    MailTemplate,
    NoticeLog,
    OtpGate,
    Payment,
    PhoneCode,
    Receipt,
    Reconciliation,
    Showroom,
    StaffProfile,
)
from .services import _lock

PASSWORD_RULE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$")


def current_customer(request):
    cid = request.session.get("customer_id")
    if not cid:
        return None
    customer = Customer.objects.filter(pk=cid).first()
    if customer and customer.delete_requested_at and customer.delete_requested_at + timedelta(days=7) <= timezone.now():
        request.session.pop("customer_id", None)
        return None
    return customer


def password_ok(raw):
    return bool(PASSWORD_RULE.match(raw or ""))


def issue_otp(phone, purpose):
    now = timezone.now()
    gate, _ = OtpGate.objects.get_or_create(phone=phone)
    if gate.locked_until and gate.locked_until > now:
        return None, "Số này đang tạm khóa. Thử lại sau 15 phút."
    sent = PhoneCode.objects.filter(phone=phone, created_at__gte=now - timedelta(hours=1)).count()
    if sent >= 5:
        return None, "Đã gửi đủ 5 mã trong một giờ."
    code = f"{random.randint(0, 999999):06d}"
    PhoneCode.objects.create(phone=phone, purpose=purpose, code=code, expires_at=now + timedelta(minutes=5))
    return code, ""


def check_otp(phone, purpose, code):
    now = timezone.now()
    gate, _ = OtpGate.objects.get_or_create(phone=phone)
    if gate.locked_until and gate.locked_until > now:
        return False, "Số này đang tạm khóa. Thử lại sau 15 phút."
    row = PhoneCode.objects.filter(phone=phone, purpose=purpose, expires_at__gte=now).order_by("-created_at").first()
    if row is None or row.code != (code or "").strip():
        gate.fail_count += 1
        if gate.fail_count >= 5:
            gate.locked_until = now + timedelta(minutes=15)
            gate.fail_count = 0
            gate.save()
            return False, "Số này đang tạm khóa. Thử lại sau 15 phút."
        gate.save()
        return False, "Mã không đúng hoặc đã hết hạn."
    gate.fail_count = 0
    gate.locked_until = None
    gate.save()
    row.delete()
    return True, ""


def set_password(customer, raw):
    customer.password = make_password(raw)
    if customer.pk:
        customer.save(update_fields=["password"])
    else:
        customer.save()


def login_password(phone, raw):
    customer = Customer.objects.filter(phone=phone).first()
    if customer is None or not check_password(raw or "", customer.password):
        return None
    if customer.delete_requested_at and customer.delete_requested_at + timedelta(days=7) <= timezone.now():
        return None
    if customer.delete_requested_at:
        customer.delete_requested_at = None
        customer.save(update_fields=["delete_requested_at"])
    return customer


def shop_open(moment=None):
    showroom = Showroom.objects.filter(is_primary=True).first()
    moment = timezone.localtime(moment or timezone.now())
    hours = (showroom.hours if showroom else "08:00–20:00").replace("–", "-").replace("—", "-")
    try:
        start, end = [part.strip() for part in hours.split("-", 1)]
        sh, sm = [int(x) for x in start.split(":")]
        eh, em = [int(x) for x in end.split(":")]
    except ValueError:
        return True, showroom
    minutes = moment.hour * 60 + moment.minute
    return sh * 60 + sm <= minutes < eh * 60 + em, showroom


def settle_gateway(order, gateway_txn, amount, ok):
    with _lock:
        with transaction.atomic():
            existing = Payment.objects.filter(gateway_txn=gateway_txn).first()
            if existing and existing.status == "success":
                receipt = Receipt.objects.filter(order=order).first()
                return receipt, "Đã ghi nhận phiếu thu này."
            if not ok:
                Payment.objects.update_or_create(
                    gateway_txn=gateway_txn,
                    defaults={"order": order, "gateway": order_gateway(), "amount": amount, "status": "failed"},
                )
                return None, "Thanh toán chưa xong. Đơn vẫn chờ trong hạn giữ hàng."
            if int(amount) != order.total:
                Payment.objects.update_or_create(
                    gateway_txn=gateway_txn,
                    defaults={"order": order, "gateway": order_gateway(), "amount": amount, "status": "mismatch"},
                )
                Reconciliation.objects.get_or_create(
                    order=order,
                    gateway_txn=gateway_txn,
                    defaults={"reported_amount": amount, "expected_amount": order.total, "note": "Lệch số tiền"},
                )
                return None, "Số tiền lệch đơn. Đơn chưa đánh dấu đã thanh toán và đã vào hàng đối soát."
            Payment.objects.update_or_create(
                gateway_txn=gateway_txn,
                defaults={"order": order, "gateway": order_gateway(), "amount": amount, "status": "success"},
            )
            receipt, created = Receipt.objects.get_or_create(
                order=order,
                defaults={"amount": order.total, "gateway_txn": gateway_txn},
            )
            if created or not order.paid:
                order.paid = True
                if order.status == "cho_thanh_toan":
                    order.status = "cho_xac_nhan"
                order.save(update_fields=["paid", "status"])
            return receipt, "Đã thanh toán."


def order_gateway():
    from .models import SiteConfig
    return SiteConfig.load().gateway or "vnpay"


def notify(channel, target, subject, body):
    NoticeLog.objects.create(channel=channel, target=target or "", subject=subject, body=body)
    if channel == "email" and target:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [target], fail_silently=True)


def notify_order(order):
    template = MailTemplate.objects.filter(code="tao_don").first()
    subject = template.subject if template else "Đơn " + order.code
    body = (template.body if template else "Đơn {ma_don} của {ten} tổng {tong}.").format(
        ma_don=order.code, ten=order.name, tong=order.total, gio_hen=order.appointment_time or "", dia_chi=order.address
    )
    if order.email:
        notify("email", order.email, subject, body)


def assign_conversation(conversation):
    open_now, showroom = shop_open()
    conversation.showroom = showroom
    if open_now:
        staff = StaffProfile.objects.filter(role="sales", ready=True, showroom=showroom).order_by("last_assigned_at").first()
        if staff:
            conversation.assignee = staff.user
            staff.last_assigned_at = timezone.now()
            staff.save(update_fields=["last_assigned_at"])
    conversation.save()


def record_customer_message(conversation, body, image=None, moment=None):
    extra = {"image": image} if image else {}
    ChatMessage.objects.create(conversation=conversation, sender="khach", body=body, **extra)
    open_now, showroom = shop_open(moment)
    if not open_now and not conversation.messages.filter(sender="he_thong").exists():
        hours = showroom.hours if showroom else "08:00–20:00"
        ChatMessage.objects.create(
            conversation=conversation,
            sender="he_thong",
            body=f"Showroom đang đóng cửa ({hours}). Để lại số điện thoại, tư vấn sẽ gọi lại khi mở cửa.",
        )
    elif not conversation.messages.filter(sender="nhan_vien").exists():
        first = conversation.messages.filter(sender="khach").order_by("created_at").first()
        if first and timezone.now() - first.created_at >= timedelta(minutes=5):
            conversation.overdue = True
    conversation.status = "moi" if conversation.assignee_id is None else conversation.status
    conversation.save()
