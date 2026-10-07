from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone

from .models import (
    Booking,
    ChannelLink,
    ChatMessage,
    Conversation,
    Inventory,
    MailTemplate,
    NoticeLog,
    Showroom,
    StockTransfer,
)
from .phase2 import notify
from .services import _lock, available


def channel_open(channel):
    if channel not in {"zalo", "messenger"}:
        return True
    link = ChannelLink.objects.filter(channel=channel).first()
    return bool(link and link.connected)


def ingest_channel_message(channel, external_id, name, phone, body):
    row = Conversation.objects.filter(channel=channel, external_id=external_id).first()
    if row is None:
        row = Conversation.objects.create(
            channel=channel,
            external_id=external_id,
            name=name,
            phone=phone,
        )
        from .phase2 import assign_conversation
        assign_conversation(row)
    else:
        if name:
            row.name = name
        if phone:
            row.phone = phone
        row.save(update_fields=["name", "phone", "updated_at"])
    ChatMessage.objects.create(conversation=row, sender="khach", body=body)
    return row


def push_channel_reply(conversation, body):
    if not channel_open(conversation.channel):
        return False, "Kênh đang ngắt"
    ChatMessage.objects.create(conversation=conversation, sender="nhan_vien", body=body)
    conversation.status = "dang_xu_ly"
    conversation.overdue = False
    conversation.save(update_fields=["status", "overdue", "updated_at"])
    return True, ""


def appointment_at(booking):
    clock = datetime.strptime(booking.time, "%H:%M").time()
    naive = datetime.combine(booking.date, clock)
    return timezone.make_aware(naive, timezone.get_current_timezone())


def send_due_reminders(moment=None):
    moment = moment or timezone.now()
    horizon = moment + timedelta(hours=2)
    pending = Booking.objects.filter(reminded_at__isnull=True, reminder_error="", status="cho_xac_nhan")
    for booking in pending:
        try:
            start = appointment_at(booking)
        except ValueError:
            continue
        if start < moment or start > horizon:
            continue
        try:
            template = MailTemplate.objects.filter(code="nhac_lich").first()
            subject = template.subject if template else "Nhắc lịch {ma_lich}"
            body = template.body if template else "{ten} có lịch {ma_lich} lúc {gio_hen} tại {dia_chi}."
            text_subject = subject.format(ma_lich=booking.code, ten=booking.name, gio_hen=booking.time, dia_chi=booking.showroom.address)
            text_body = body.format(ma_lich=booking.code, ten=booking.name, gio_hen=booking.time, dia_chi=booking.showroom.address)
            if not booking.phone:
                raise ValueError("Thiếu số điện thoại")
            notify("zalo", booking.phone, text_subject, text_body)
            booking.reminded_at = moment
            booking.save(update_fields=["reminded_at"])
        except Exception as exc:
            booking.reminder_error = str(exc)[:200]
            booking.save(update_fields=["reminder_error"])
            NoticeLog.objects.create(
                channel="zalo",
                target=booking.phone,
                subject="Nhắc lịch " + booking.code,
                body="",
                ok=False,
                error=str(exc)[:200],
            )


def location_choices():
    rows = [("ship", "Kho giao hàng")]
    rows.extend((shop.slug, shop.name) for shop in Showroom.objects.all())
    return rows


def location_label(code):
    return dict(location_choices()).get(code, code)


def _stock(variant, location):
    row, _ = Inventory.objects.get_or_create(variant=variant, location=location, defaults={"on_hand": 0})
    return row


def create_transfer(variant, qty, source, destination):
    if source == destination:
        return None, "Điểm đi và điểm đến phải khác nhau."
    if qty < 1:
        return None, "Số lượng phải từ 1."
    seq = StockTransfer.objects.count() + 1
    ticket = StockTransfer.objects.create(
        code=f"DC{timezone.localdate().year}{seq:06d}",
        variant=variant,
        qty=qty,
        source=source,
        destination=destination,
    )
    return ticket, ""


def ship_transfer(ticket):
    with _lock:
        with transaction.atomic():
            row = StockTransfer.objects.get(pk=ticket.pk)
            if row.status != "cho_xuat":
                return "Phiếu này không còn chờ xuất."
            if available(row.variant_id, row.source) < row.qty:
                return "Điểm đi không đủ hàng khả dụng."
            stock = _stock(row.variant, row.source)
            if stock.on_hand < row.qty:
                return "Điểm đi không đủ tồn thực."
            stock.on_hand -= row.qty
            stock.save(update_fields=["on_hand"])
            row.status = "dang_di"
            row.shipped_at = timezone.now()
            row.save(update_fields=["status", "shipped_at"])
    return ""


def receive_transfer(ticket):
    with _lock:
        with transaction.atomic():
            row = StockTransfer.objects.get(pk=ticket.pk)
            if row.status != "dang_di":
                return "Chỉ nhận phiếu đang trên đường."
            stock = _stock(row.variant, row.destination)
            stock.on_hand += row.qty
            stock.save(update_fields=["on_hand"])
            row.status = "da_nhan"
            row.received_at = timezone.now()
            row.save(update_fields=["status", "received_at"])
    return ""


def cancel_transfer(ticket):
    if ticket.status != "cho_xuat":
        return "Chỉ hủy phiếu chưa xuất."
    ticket.status = "da_huy"
    ticket.save(update_fields=["status"])
    return ""
