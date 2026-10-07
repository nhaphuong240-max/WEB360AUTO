import csv
from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import (
    AddressBook,
    Article,
    Service,
    Booking,
    CannedReply,
    ChatMessage,
    Conversation,
    Customer,
    GarageCar,
    Order,
    OrderLine,
    PathRedirect,
    Reconciliation,
    Refund,
    ReturnRequest,
    Review,
    Showroom,
    StaffProfile,
    StaticPage,
    Variant,
)
from .phase2 import (
    assign_conversation,
    check_otp,
    current_customer,
    issue_otp,
    login_password,
    notify_order,
    order_gateway,
    password_ok,
    record_customer_message,
    set_password,
    settle_gateway,
)
from .services import available, slot_full
from .views import _cart

MAX_IMAGE = 5 * 1024 * 1024


def image_ok(uploaded):
    if uploaded is None or uploaded.size > MAX_IMAGE:
        return False
    head = uploaded.read(12)
    uploaded.seek(0)
    return head.startswith(b"\xff\xd8\xff") or head.startswith(b"\x89PNG\r\n\x1a\n") or (head[:4] == b"RIFF" and head[8:12] == b"WEBP")


def _merge_cart(request, customer):
    guest = _cart(request)
    member = Cart_for(customer, guest)
    notes = []
    if member.pk != guest.pk:
        for line in list(guest.lines.select_related("variant")):
            location = "ship" if line.mode == "ship" else (line.showroom.slug if line.showroom else "")
            twin = member.lines.filter(variant=line.variant, mode=line.mode, showroom=line.showroom).first()
            if twin is None and line.showroom is None:
                twin = member.lines.filter(variant=line.variant, mode=line.mode, showroom__isnull=True).first()
            room = (twin.qty if twin else 0)
            cap = min(available(line.variant_id, location) if location else 0, 20)
            kept = min(room + line.qty, cap)
            if kept < room + line.qty:
                notes.append(line.variant.product.name)
            if twin:
                twin.qty = max(kept, 1) if kept else twin.qty
                if kept:
                    twin.save(update_fields=["qty"])
            elif kept:
                line.cart = member
                line.qty = kept
                line.save()
        guest.lines.all().delete()
        guest.customer = None
        guest.session_key = "old-" + str(guest.pk)
        guest.save(update_fields=["customer", "session_key"])
        member.session_key = request.session.session_key
        member.save(update_fields=["session_key"])
        request.session["cart_id"] = member.id
    if notes:
        messages.warning(request, "Đã giảm số lượng cho vừa tồn: " + ", ".join(notes))


def Cart_for(customer, guest):
    member = customer.carts.exclude(pk=guest.pk).first()
    if member is None:
        guest.customer = customer
        guest.save(update_fields=["customer"])
        return guest
    return member


def account(request):
    customer = current_customer(request)
    if customer is None:
        return render(request, "account.html", {"otp_preview": request.session.pop("otp_preview", "")})
    orders = customer.orders.prefetch_related("lines").order_by("-created_at")
    return render(request, "account.html", {
        "customer": customer,
        "orders": orders,
        "addresses": customer.addresses.all(),
        "cars": customer.cars.all(),
        "returns": customer.returns.all(),
    })


@require_POST
def account_otp(request):
    phone = "".join(ch for ch in request.POST.get("phone", "") if ch.isdigit())
    purpose = request.POST.get("purpose") or "register"
    if len(phone) != 10 or not phone.startswith("0"):
        messages.error(request, "Nhập đủ 10 số, bắt đầu bằng 0.")
        return redirect("account")
    if purpose == "register" and Customer.objects.filter(phone=phone).exists():
        messages.error(request, "Số này đã có tài khoản. Hãy đăng nhập hoặc chọn quên mật khẩu.")
        return redirect("account")
    code, err = issue_otp(phone, purpose)
    if err:
        messages.error(request, err)
        return redirect("account")
    request.session["otp_phone"] = phone
    request.session["otp_purpose"] = purpose
    if settings_debug():
        request.session["otp_preview"] = code
    messages.success(request, "Đã gửi mã 6 số, hiệu lực 5 phút.")
    return redirect("account")


def settings_debug():
    from django.conf import settings
    return settings.DEBUG


@require_POST
def account_register(request):
    phone = request.session.get("otp_phone") or ""
    purpose = request.session.get("otp_purpose") or "register"
    ok, err = check_otp(phone, purpose, request.POST.get("code"))
    if not ok:
        messages.error(request, err)
        return redirect("account")
    raw = request.POST.get("password") or ""
    if not password_ok(raw):
        messages.error(request, "Mật khẩu cần từ 8 ký tự, có chữ và số.")
        return redirect("account")
    name = (request.POST.get("name") or "").strip() or "Khách"
    email = (request.POST.get("email") or "").strip()
    if email and Customer.objects.filter(email__iexact=email).exists():
        messages.error(request, "Email đã gắn tài khoản khác.")
        return redirect("account")
    customer = Customer.objects.filter(phone=phone).first()
    if purpose == "register":
        if customer:
            messages.error(request, "Số này đã có tài khoản.")
            return redirect("account")
        customer = Customer(phone=phone, name=name, email=email)
        set_password(customer, raw)
    else:
        if customer is None:
            messages.error(request, "Không thấy tài khoản với số này.")
            return redirect("account")
        set_password(customer, raw)
        if name:
            customer.name = name
            customer.save(update_fields=["name"])
    request.session["customer_id"] = customer.id
    _merge_cart(request, customer)
    messages.success(request, "Đã vào tài khoản " + customer.name)
    return redirect("account")


@require_POST
def account_login(request):
    phone = "".join(ch for ch in request.POST.get("phone", "") if ch.isdigit())
    customer = login_password(phone, request.POST.get("password"))
    if customer is None:
        messages.error(request, "Số điện thoại hoặc mật khẩu chưa đúng.")
        return redirect("account")
    request.session["customer_id"] = customer.id
    _merge_cart(request, customer)
    messages.success(request, "Xin chào " + customer.name)
    return redirect("account")


@require_POST
def account_logout(request):
    request.session.pop("customer_id", None)
    return redirect("account")


@require_POST
def account_profile(request):
    customer = current_customer(request)
    if customer is None:
        return redirect("account")
    customer.name = (request.POST.get("name") or customer.name).strip()
    email = (request.POST.get("email") or "").strip()
    if email and Customer.objects.filter(email__iexact=email).exclude(pk=customer.pk).exists():
        messages.error(request, "Email đã gắn tài khoản khác.")
        return redirect("account")
    customer.email = email
    customer.promo_opt_in = request.POST.get("promo") == "1"
    customer.save(update_fields=["name", "email", "promo_opt_in"])
    raw = request.POST.get("password") or ""
    if raw:
        if not password_ok(raw):
            messages.error(request, "Mật khẩu mới cần từ 8 ký tự, có chữ và số.")
            return redirect("account")
        set_password(customer, raw)
    if request.POST.get("xoa") == "1":
        customer.delete_requested_at = timezone.now()
        customer.save(update_fields=["delete_requested_at"])
        messages.success(request, "Đã nhận yêu cầu xóa. Trong 7 ngày đăng nhập lại sẽ hủy yêu cầu. Đơn hàng vẫn được lưu.")
    else:
        messages.success(request, "Đã lưu hồ sơ.")
    return redirect("account")


@require_POST
def address_add(request):
    customer = current_customer(request)
    if customer is None:
        return redirect("account")
    if customer.addresses.count() >= 10:
        messages.error(request, "Sổ địa chỉ tối đa 10 địa chỉ.")
        return redirect("account")
    row = AddressBook.objects.create(customer=customer, line=request.POST.get("line") or "", district=request.POST.get("district") or "Quận 7", is_default=not customer.addresses.exists())
    if request.POST.get("mac_dinh") == "1":
        customer.addresses.exclude(pk=row.pk).update(is_default=False)
        row.is_default = True
        row.save(update_fields=["is_default"])
    return redirect("account")


@require_POST
def garage_add(request):
    customer = current_customer(request)
    if customer is None:
        return redirect("account")
    if customer.cars.count() >= 10:
        messages.error(request, "Garage tối đa 10 xe.")
        return redirect("account")
    GarageCar.objects.create(customer=customer, label=(request.POST.get("label") or "").strip())
    return redirect("account")


@require_POST
def review_add(request, slug):
    customer = current_customer(request)
    variant = get_object_or_404(Variant, sku=request.POST.get("sku") or "", product__slug=slug)
    if customer is None:
        messages.error(request, "Đăng nhập để đánh giá.")
        return redirect("product", slug=slug)
    order = Order.objects.filter(customer=customer, status="hoan_thanh", lines__variant=variant).first()
    if order is None:
        messages.error(request, "Chỉ đánh giá được sau khi đơn chứa sản phẩm này đã hoàn thành.")
        return redirect("product", slug=slug)
    if Review.objects.filter(order=order, variant=variant).exists():
        messages.error(request, "Đơn này đã có đánh giá cho phiên bản đó.")
        return redirect("product", slug=slug)
    body = (request.POST.get("body") or "").strip()
    stars = int(request.POST.get("stars") or 0)
    if stars < 1 or stars > 5 or len(body) < 20 or len(body) > 1000:
        messages.error(request, "Cần từ 1 đến 5 sao và nội dung từ 20 đến 1000 ký tự.")
        return redirect("product", slug=slug)
    files = [item for item in request.FILES.getlist("images") if item][:4]
    if any(not image_ok(item) for item in files):
        messages.error(request, "Ảnh đánh giá chỉ nhận jpg, png, webp, tối đa 5 MB.")
        return redirect("product", slug=slug)
    review = Review.objects.create(order=order, variant=variant, customer=customer, stars=stars, body=body, status="cho_duyet")
    for item in files:
        review.images.create(image=item)
    messages.success(request, "Đã gửi đánh giá, đang chờ duyệt. Điểm trung bình chưa đổi.")
    return redirect("product", slug=slug)


@require_POST
def return_create(request, code):
    customer = current_customer(request)
    if customer is None:
        return redirect("account")
    order = get_object_or_404(Order, code=code, customer=customer, status="hoan_thanh")
    line = get_object_or_404(OrderLine, pk=request.POST.get("line"), order=order)
    product = line.variant.product if line.variant_id else None
    days = product.return_days if product else 7
    if order.completed_at and order.completed_at + timedelta(days=days) < timezone.now():
        messages.error(request, "Đã quá hạn đổi trả của sản phẩm này.")
        return redirect("account")
    qty = min(int(request.POST.get("qty") or 1), line.qty)
    seq = ReturnRequest.objects.count() + 1
    ticket = ReturnRequest.objects.create(code=f"DT{timezone.localdate().year}{seq:06d}", order=order, customer=customer, reason=request.POST.get("reason") or "")
    ticket.lines.create(order_line=line, qty=qty)
    if order.status != "dang_doi_tra":
        order.status = "dang_doi_tra"
        order.save(update_fields=["status"])
    messages.success(request, "Đã tạo phiếu " + ticket.code + ", chờ duyệt.")
    return redirect("account")


def articles(request):
    now = timezone.now()
    rows = Article.objects.filter(status="published", publish_at__lte=now)
    return render(request, "articles.html", {"articles": rows})


def article_detail(request, slug):
    now = timezone.now()
    article = get_object_or_404(Article, slug=slug, status="published", publish_at__lte=now)
    return render(request, "article.html", {"article": article})


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, status="published")
    return render(request, "page.html", {"page": page})


def chat_page(request):
    conversation = _conversation(request)
    return render(request, "chat.html", {"conversation": conversation, "thread": _visible(conversation)})


@require_POST
def chat_send(request):
    conversation = _conversation(request)
    body = (request.POST.get("body") or "").strip()
    image = request.FILES.get("image")
    if image and not image_ok(image):
        messages.error(request, "Ảnh chat chỉ nhận jpg, png, webp, tối đa 5 MB.")
        return redirect(request.POST.get("next") or "chat")
    if not body and not image:
        return redirect(request.POST.get("next") or "chat")
    posted_name = (request.POST.get("name") or "").strip()
    posted_phone = "".join(ch for ch in request.POST.get("phone", "") if ch.isdigit())
    if posted_name:
        conversation.name = posted_name
    if posted_phone:
        conversation.phone = posted_phone
        conversation.customer = Customer.objects.filter(phone=posted_phone).first()
    customer = current_customer(request)
    if customer:
        conversation.customer = customer
        conversation.name = conversation.name or customer.name
        conversation.phone = conversation.phone or customer.phone
    if conversation.showroom_id is None:
        assign_conversation(conversation)
    else:
        conversation.save()
    record_customer_message(conversation, body, image)
    return redirect(request.POST.get("next") or "chat")


def _conversation(request):
    if not request.session.session_key:
        request.session.create()
    cid = request.session.get("chat_id")
    row = Conversation.objects.filter(pk=cid).first() if cid else None
    if row is None:
        row = Conversation.objects.create(session_key=request.session.session_key, channel="web")
        customer = current_customer(request)
        if customer:
            row.customer = customer
            row.name = customer.name
            row.phone = customer.phone
            row.save()
        request.session["chat_id"] = row.id
    return row


def _visible(conversation):
    return conversation.messages.filter(internal=False)


@staff_member_required
def inbox(request):
    rows = Conversation.objects.all()
    profile = StaffProfile.objects.filter(user=request.user).first()
    if profile and profile.role in {"sales", "manager"} and profile.showroom_id:
        rows = rows.filter(showroom=profile.showroom)
    now = timezone.now()
    for row in rows.filter(overdue=False):
        first = row.messages.filter(sender="khach").order_by("created_at").first()
        if first and not row.messages.filter(sender="nhan_vien").exists() and now - first.created_at >= timedelta(minutes=5):
            row.overdue = True
            row.save(update_fields=["overdue"])
    channel = request.GET.get("kenh") or ""
    if channel:
        rows = rows.filter(channel=channel)
    current = None
    if request.GET.get("id"):
        current = rows.filter(pk=request.GET.get("id")).first()
    from .phase3 import channel_open
    return render(request, "inbox.html", {
        "rows": rows,
        "current": current,
        "thread": current.messages.all() if current else [],
        "replies": CannedReply.objects.all(),
        "showrooms": Showroom.objects.all(),
        "services": Service.objects.all(),
        "kenh": channel,
        "channel_closed": bool(current and not channel_open(current.channel)),
    })


@staff_member_required
@require_POST
def inbox_reply(request, pk):
    row = get_object_or_404(Conversation, pk=pk)
    body = (request.POST.get("body") or "").strip()
    internal = request.POST.get("noi_bo") == "1"
    if body and not internal and row.channel in {"zalo", "messenger"}:
        from .phase3 import push_channel_reply
        ok, err = push_channel_reply(row, body)
        if not ok:
            messages.error(request, err)
            return redirect("/hop-thu/?id=" + str(row.pk))
        row.assignee = request.user
        row.save(update_fields=["assignee"])
    elif body:
        ChatMessage.objects.create(conversation=row, sender="nhan_vien", body=body, internal=internal)
        if not internal:
            row.status = "dang_xu_ly"
            row.overdue = False
            row.assignee = request.user
            row.save(update_fields=["status", "overdue", "assignee"])
    if request.POST.get("phone"):
        row.phone = "".join(ch for ch in request.POST.get("phone") if ch.isdigit())
        row.name = request.POST.get("name") or row.name
        row.save(update_fields=["phone", "name"])
    return redirect("/hop-thu/?id=" + str(row.pk))


@staff_member_required
@require_POST
def inbox_booking(request, pk):
    from .models import Service
    row = get_object_or_404(Conversation, pk=pk)
    showroom = get_object_or_404(Showroom, pk=request.POST.get("showroom"))
    service = get_object_or_404(Service, pk=request.POST.get("service"))
    if slot_full(showroom, service, request.POST.get("time"), request.POST.get("date")):
        messages.error(request, "Khung giờ vừa hết chỗ. Chọn giờ khác.")
        return redirect("/hop-thu/?id=" + str(row.pk))
    seq = Booking.objects.count() + 1
    Booking.objects.create(
        code=f"LH{seq:06d}",
        name=row.name or "Khách chat",
        phone=row.phone or request.POST.get("phone") or "",
        showroom=showroom,
        service=service,
        date=request.POST.get("date"),
        time=request.POST.get("time"),
        car=request.POST.get("car") or "Chưa rõ",
        note="Từ hội thoại " + str(row.pk),
    )
    messages.success(request, "Đã tạo lịch từ số " + (row.phone or ""))
    return redirect("/hop-thu/?id=" + str(row.pk))


def gateway(request, code):
    order = get_object_or_404(Order, code=code, payment="gateway")
    return render(request, "gateway.html", {"order": order, "gateway": order_gateway()})


@require_POST
def gateway_result(request, code):
    order = get_object_or_404(Order, code=code, payment="gateway")
    kind = request.POST.get("ket_qua")
    txn = "PAY-" + order.code
    amount = order.total
    ok = True
    if kind == "lech":
        txn = "PAY-" + order.code + "-LECH"
        amount = order.total + 1000
    elif kind == "huy":
        ok = False
        txn = "PAY-" + order.code + "-HUY"
    elif kind == "that_bai":
        ok = False
    _receipt, text = settle_gateway(order, txn, amount, ok)
    messages.success(request, text)
    if request.POST.get("kenh") == "ipn":
        return HttpResponse(text)
    return redirect("confirm", code=order.code)


@csrf_exempt
@require_POST
def gateway_ipn(request, code):
    return gateway_result(request, code)


@staff_member_required
def reports(request):
    profile = StaffProfile.objects.filter(user=request.user).first()
    if profile is None or profile.role not in {"admin", "manager"}:
        messages.error(request, "Chỉ quản trị và quản lý showroom xem báo cáo.")
        return redirect("/quan-tri/")
    orders = Order.objects.all()
    if profile.role == "manager" and profile.showroom_id:
        orders = orders.filter(showroom=profile.showroom)
    done = orders.filter(status="hoan_thanh")
    summary = {
        "revenue": done.aggregate(total=Sum("total"))["total"] or 0,
        "by_status": list(orders.values("status").annotate(n=Count("id"))),
        "products": list(OrderLine.objects.filter(order__in=done).values("name").annotate(qty=Sum("qty"), money=Sum("unit_price"))),
    }
    if request.GET.get("xuat") == "1":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=bao-cao.csv"
        writer = csv.writer(response)
        writer.writerow(["ma", "trang_thai", "tong", "showroom", "nguon", "ngay_hoan_thanh"])
        for order in done:
            writer.writerow([order.code, order.status, order.total, order.showroom.slug if order.showroom else "", order.source, order.completed_at])
        return response
    return render(request, "reports.html", {"summary": summary, "reconcile": Reconciliation.objects.all()[:20]})


@login_required
def return_decide(request, code):
    if request.method != "POST":
        return redirect("reports")
    ticket = get_object_or_404(ReturnRequest, code=code)
    choice = request.POST.get("xu_ly")
    if choice == "tu_choi":
        ticket.status = "tu_choi"
        ticket.customer_note = request.POST.get("ly_do") or ""
    elif choice == "doi_moi":
        ticket.status = "cho_hang"
        ticket.resolution = "doi_moi"
    elif choice == "hoan_tien":
        ticket.status = "da_hoan"
        ticket.resolution = "hoan_tien"
        Refund.objects.get_or_create(
            request=ticket,
            defaults={
                "amount": ticket.order.total,
                "gateway_refund_id": request.POST.get("ma_hoan") or "",
                "transfer_receipt": request.POST.get("bien_lai") or "",
            },
        )
    ticket.save()
    messages.success(request, "Đã cập nhật phiếu " + ticket.code)
    return redirect("reports")
