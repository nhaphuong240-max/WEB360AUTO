import csv

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import ChannelLink, NoticeLog, Order, StaffProfile, StockTransfer, Variant
from .phase3 import (
    cancel_transfer,
    create_transfer,
    ingest_channel_message,
    location_choices,
    receive_transfer,
    ship_transfer,
)


def _profile(request):
    return StaffProfile.objects.filter(user=request.user).first()


@staff_member_required
def channel_sandbox(request):
    if request.method == "POST":
        action = request.POST.get("viec")
        channel = request.POST.get("kenh")
        if action == "ket_noi" and channel in {"zalo", "messenger"}:
            ChannelLink.objects.filter(channel=channel).update(connected=request.POST.get("noi") == "1")
            messages.success(request, "Đã cập nhật kết nối kênh.")
        elif action == "gui":
            external = (request.POST.get("external") or "").strip() or "khach-kenh"
            body = (request.POST.get("body") or "").strip()
            if channel not in {"zalo", "messenger"} or not body:
                messages.error(request, "Chọn kênh và nhập nội dung.")
            else:
                row = ingest_channel_message(
                    channel,
                    external,
                    (request.POST.get("name") or "").strip(),
                    "".join(ch for ch in request.POST.get("phone", "") if ch.isdigit()),
                    body,
                )
                messages.success(request, "Đã đưa tin vào hộp thư.")
                return redirect("/hop-thu/?id=" + str(row.pk))
        return redirect("channels")
    return render(request, "channels.html", {"links": ChannelLink.objects.all()})


@staff_member_required
def transfers(request):
    profile = _profile(request)
    if profile is None or profile.role not in {"warehouse", "manager", "admin"}:
        messages.error(request, "Chỉ thủ kho, quản lý và quản trị tạo phiếu điều chuyển.")
        return redirect("/quan-tri/")
    rows = StockTransfer.objects.select_related("variant")
    if profile.role == "manager" and profile.showroom_id:
        slug = profile.showroom.slug
        rows = rows.filter(source=slug) | rows.filter(destination=slug)
    labels = dict(location_choices())
    listed = []
    for row in rows:
        row.source_name = labels.get(row.source, row.source)
        row.destination_name = labels.get(row.destination, row.destination)
        listed.append(row)
    return render(request, "transfers.html", {
        "rows": listed,
        "variants": Variant.objects.select_related("product"),
        "places": location_choices(),
    })


@staff_member_required
@require_POST
def transfer_create(request):
    profile = _profile(request)
    if profile is None or profile.role not in {"warehouse", "manager", "admin"}:
        return redirect("/quan-tri/")
    variant = get_object_or_404(Variant, pk=request.POST.get("variant"))
    source = request.POST.get("source") or ""
    destination = request.POST.get("destination") or ""
    places = {code for code, _name in location_choices()}
    if source not in places or destination not in places:
        messages.error(request, "Chọn điểm đi và điểm đến.")
        return redirect("transfers")
    if profile.role == "manager" and profile.showroom_id and profile.showroom.slug not in {source, destination}:
        messages.error(request, "Quản lý chỉ điều chuyển kho showroom của mình.")
        return redirect("transfers")
    try:
        qty = int(request.POST.get("qty") or 0)
    except ValueError:
        qty = 0
    _ticket, err = create_transfer(variant, qty, source, destination)
    if err:
        messages.error(request, err)
    else:
        messages.success(request, "Đã tạo phiếu. Tồn chưa đổi cho đến khi xuất kho.")
    return redirect("transfers")


@staff_member_required
@require_POST
def transfer_act(request, code):
    ticket = get_object_or_404(StockTransfer, code=code)
    action = request.POST.get("viec")
    if action == "xuat":
        err = ship_transfer(ticket)
    elif action == "nhan":
        err = receive_transfer(ticket)
    else:
        err = cancel_transfer(ticket)
    if err:
        messages.error(request, err)
    else:
        messages.success(request, "Đã cập nhật phiếu " + ticket.code)
    return redirect("transfers")


@staff_member_required
def invoices(request):
    profile = _profile(request)
    if profile is None or profile.role not in {"admin", "manager"}:
        messages.error(request, "Chỉ quản trị và quản lý showroom xuất dữ liệu hóa đơn.")
        return redirect("/quan-tri/")
    orders = Order.objects.filter(completed_at__isnull=False).exclude(status="da_huy").prefetch_related("lines")
    if profile.role == "manager" and profile.showroom_id:
        orders = orders.filter(showroom=profile.showroom)
    if request.GET.get("xuat") == "1":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=hoa-don.csv"
        writer = csv.writer(response)
        writer.writerow(["Website không phát hành hóa đơn cơ quan thuế. Tệp này để nhập phần mềm hóa đơn."])
        writer.writerow(["ma_don", "ngay_hoan_thanh", "ten", "dien_thoai", "sku", "ten_hang", "so_luong", "don_gia", "thanh_tien", "tong_don", "nguon", "showroom", "phat_hanh_thue"])
        for order in orders:
            shop = order.showroom.slug if order.showroom_id else ""
            lines = list(order.lines.all()) or [None]
            for line in lines:
                writer.writerow([
                    order.code,
                    order.completed_at.isoformat() if order.completed_at else "",
                    order.name,
                    order.phone,
                    line.variant.sku if line and line.variant_id else "",
                    line.name if line else "",
                    line.qty if line else "",
                    line.unit_price if line else "",
                    (line.unit_price * line.qty) if line else "",
                    order.total,
                    order.source,
                    shop,
                    "khong",
                ])
        return response
    return render(request, "invoices.html", {"orders": orders[:30]})


@staff_member_required
def reminders(request):
    bookings_sent = NoticeLog.objects.filter(channel="zalo").order_by("-created_at")[:20]
    return render(request, "reminders.html", {"logs": bookings_sent})
