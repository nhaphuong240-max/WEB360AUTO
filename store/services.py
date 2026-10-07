import threading
import unicodedata
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone

from .models import Booking, Coupon, CouponRedemption, Customer, Inventory, Order, OrderLine, Reservation, SiteConfig, SlotCapacity

_lock = threading.Lock()
SLOTS = ["08:00", "10:00", "13:00", "15:00", "17:00"]
OPEN_BOOKING = ["cho_xac_nhan", "da_xac_nhan"]


def fold(text):
    raw = unicodedata.normalize("NFD", (text or "").lower())
    return "".join(ch for ch in raw if unicodedata.category(ch) != "Mn")


def gross(amount_excl, vat_rate):
    value = Decimal(amount_excl) * (Decimal(100) + Decimal(vat_rate)) / Decimal(100)
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def excl_from_incl(amount_incl, vat_rate=10):
    guess = int((Decimal(amount_incl) * Decimal(100) / (Decimal(100) + Decimal(vat_rate))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    for delta in range(-3, 4):
        candidate = max(guess + delta, 0)
        if gross(candidate, vat_rate) == amount_incl:
            return candidate
    return guess


def vnd(amount):
    return f"{int(amount or 0):,}".replace(",", ".") + "đ"


def pct(price, compare):
    if not compare or compare <= price:
        return 0
    return round((1 - price / compare) * 100)


def variant_price(variant):
    if variant.price_incl:
        return variant.price_incl
    return gross(variant.price_excl, variant.product.vat_rate)


def variant_compare(variant):
    if variant.compare_incl:
        return variant.compare_incl
    if not variant.compare_excl:
        return 0
    return gross(variant.compare_excl, variant.product.vat_rate)


def _active_reservations(variant_id, location):
    now = timezone.now()
    return Reservation.objects.filter(variant_id=variant_id, location=location, released=False).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=now)
    )


def available(variant_id, location, ignore_session=""):
    on_hand = Inventory.objects.filter(variant_id=variant_id, location=location).values_list("on_hand", flat=True).first() or 0
    reserved = _active_reservations(variant_id, location)
    if ignore_session:
        reserved = reserved.exclude(kind=Reservation.SOFT, session_key=ignore_session)
    used = reserved.aggregate(total=Sum("qty"))["total"] or 0
    return max(0, on_hand - used)


def release_expired():
    now = timezone.now()
    Reservation.objects.filter(kind=Reservation.SOFT, released=False, expires_at__lt=now).update(released=True)
    config = SiteConfig.load()
    cutoff = now - timedelta(hours=config.transfer_hold_hours)
    stale = Order.objects.filter(payment__in=["transfer", "gateway"], paid=False, status="cho_thanh_toan", created_at__lt=cutoff)
    ids = list(stale.values_list("id", flat=True))
    if ids:
        stale.update(status="da_huy")
        Reservation.objects.filter(order_id__in=ids, released=False).update(released=True)


def place_soft_holds(session_key, lines):
    now = timezone.now()
    Reservation.objects.filter(session_key=session_key, kind=Reservation.SOFT, released=False).update(released=True)
    held = []
    for line in lines:
        location = "ship" if line.mode == "ship" else line.showroom.slug
        qty = min(line.qty, available(line.variant_id, location, ignore_session=session_key))
        if qty < 1:
            held.append((line, 0))
            continue
        Reservation.objects.create(
            variant=line.variant,
            location=location,
            qty=qty,
            kind=Reservation.SOFT,
            session_key=session_key,
            expires_at=now + timedelta(minutes=15),
        )
        held.append((line, qty))
    return held


def coupon_result(code, subtotal, mode, phone="", product_ids=None):
    raw = (code or "").strip().upper()
    if not raw:
        return {"ok": True, "code": "", "amount": 0, "free_ship": False, "message": ""}
    coupon = Coupon.objects.filter(code__iexact=raw).first()
    if coupon is None or not coupon.active:
        return {"ok": False, "message": "Không thấy mã này."}
    if coupon.valid_until and coupon.valid_until < timezone.now():
        return {"ok": False, "message": "Mã đã hết hạn."}
    if coupon.min_subtotal and subtotal < coupon.min_subtotal:
        return {"ok": False, "message": "Đơn chưa đạt giá trị tối thiểu " + vnd(coupon.min_subtotal) + "."}
    if coupon.free_ship and mode == "install":
        return {"ok": False, "message": "Mã chỉ áp dụng cho đơn giao hàng."}
    if coupon.members_only and not Customer.objects.filter(phone=phone).exists():
        return {"ok": False, "message": "Mã chỉ dành cho khách đã có tài khoản."}
    if coupon.max_uses and coupon.redemptions.count() >= coupon.max_uses:
        return {"ok": False, "message": "Mã đã hết lượt."}
    if phone and coupon.max_uses_per_phone and coupon.redemptions.filter(phone=phone).count() >= coupon.max_uses_per_phone:
        return {"ok": False, "message": "Bạn đã dùng hết lượt của mã này."}
    scoped = list(coupon.products.values_list("id", flat=True))
    if scoped and product_ids is not None and not set(product_ids).issubset(set(scoped)):
        return {"ok": False, "message": "Mã không áp dụng cho sản phẩm trong giỏ."}
    amount = int(round(subtotal * coupon.percent / 100)) if coupon.percent else 0
    return {"ok": True, "code": coupon.code.upper(), "amount": amount, "free_ship": coupon.free_ship, "message": ""}


def ship_fee(subtotal, district, free_ship):
    if free_ship:
        return 0
    if not district:
        return None
    base = 50000 if district == "Khác" else 35000
    return 0 if subtotal >= 1000000 else base


def fit_text(product, vehicle):
    if vehicle is None:
        return ""
    if product.fitment == "consult":
        return "Cần xác nhận độ vừa trước khi lắp."
    slugs = {item.slug for item in product.vehicles.all()}
    if product.fitment == "all" or (vehicle.slug in slugs):
        return "Vừa xe của bạn"
    return "Không nằm trong danh sách vừa xe đã chọn"


def install_slot_full(showroom, time, date):
    used = Order.objects.filter(
        mode="install", showroom=showroom, appointment_time=time, appointment_date=date
    ).exclude(status="da_huy").count()
    return used >= 2


def slot_full(showroom, service, time, date):
    rule = SlotCapacity.objects.filter(showroom=showroom, service=service, time=time).first()
    capacity = rule.capacity if rule else 2
    used = Booking.objects.filter(showroom=showroom, service=service, time=time, date=date, status__in=OPEN_BOOKING).count()
    return used >= capacity


def create_order(session_key, lines, payload):
    with _lock:
        with transaction.atomic():
            prepared = []
            for line in lines:
                location = "ship" if line.mode == "ship" else line.showroom.slug
                qty_ok = available(line.variant_id, location, ignore_session=session_key)
                if line.qty > qty_ok:
                    return None, "Không đủ hàng cho " + line.variant.product.name + "."
                prepared.append((line, location))
            year = timezone.localdate().year
            prefix = f"DH{year}"
            last = Order.objects.filter(code__startswith=prefix).order_by("-code").first()
            seq = int(last.code[-6:]) + 1 if last else 1
            code = f"{prefix}{seq:06d}"
            coupon_code = payload.get("coupon_code") or ""
            if coupon_code:
                coupon = Coupon.objects.filter(code__iexact=coupon_code, active=True).first()
                phone = payload.get("phone") or ""
                if coupon and coupon.max_uses and coupon.redemptions.count() >= coupon.max_uses:
                    return None, "Mã đã hết lượt."
                if coupon and phone and coupon.max_uses_per_phone and coupon.redemptions.filter(phone=phone).count() >= coupon.max_uses_per_phone:
                    return None, "Bạn đã dùng hết lượt của mã này."
            order = Order.objects.create(code=code, **payload)
            if coupon_code:
                coupon = Coupon.objects.filter(code__iexact=coupon_code).first()
                if coupon:
                    CouponRedemption.objects.create(coupon=coupon, order=order, phone=payload.get("phone") or "", amount=payload.get("discount") or 0)
            for line, location in prepared:
                unit = variant_price(line.variant)
                OrderLine.objects.create(
                    order=order,
                    variant=line.variant,
                    slug=line.variant.product.slug,
                    name=line.variant.product.name,
                    variant_name=line.variant.name,
                    qty=line.qty,
                    unit_price=unit,
                )
                Reservation.objects.create(
                    variant=line.variant,
                    location=location,
                    qty=line.qty,
                    kind=Reservation.HARD,
                    order=order,
                    session_key=session_key,
                    expires_at=None if payload["payment"] == "cash" else timezone.now() + timedelta(hours=SiteConfig.load().transfer_hold_hours),
                )
            Reservation.objects.filter(session_key=session_key, kind=Reservation.SOFT, released=False).update(released=True)
            return order, ""


def cancel_order(order):
    if order.status not in {"cho_thanh_toan", "cho_xac_nhan"}:
        return False
    with _lock:
        with transaction.atomic():
            order.status = "da_huy"
            order.save(update_fields=["status"])
            order.reservations.filter(released=False).update(released=True)
    return True
