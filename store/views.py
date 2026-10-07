from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookingForm, CheckoutForm, LookupForm
from .models import Article, Banner, Booking, Cart, CartLine, Category, Order, Product, Review, Service, Showroom, TrustItem, Variant, Vehicle
from .services import (
    available,
    cancel_order,
    coupon_result,
    create_order,
    fit_text,
    fold,
    install_slot_full,
    pct,
    place_soft_holds,
    ship_fee,
    slot_full,
    variant_compare,
    variant_price,
    vnd,
)

STATUS_LABEL = {
    "cho_thanh_toan": "Chờ thanh toán",
    "cho_xac_nhan": "Chờ xác nhận",
    "dang_chuan_bi": "Đang chuẩn bị",
    "dang_giao": "Đang giao",
    "cho_khach": "Chờ khách đến",
    "hoan_thanh": "Hoàn thành",
    "da_huy": "Đã hủy",
}


def _cart(request):
    if not request.session.session_key:
        request.session.create()
    cart_id = request.session.get("cart_id")
    cart = Cart.objects.filter(pk=cart_id).first() if cart_id else None
    if cart is None:
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    elif cart.session_key != request.session.session_key:
        cart.session_key = request.session.session_key
        cart.save(update_fields=["session_key"])
    request.session["cart_id"] = cart.id
    return cart


def _vehicle(request):
    slug = request.session.get("vehicle") or ""
    if not slug:
        return None
    return Vehicle.objects.filter(slug=slug).first()


def _decorate(product, vehicle):
    variant = product.variants.all()[0]
    price = variant_price(variant)
    compare = variant_compare(variant)
    product.card_price = price
    product.card_compare = compare
    product.card_off = pct(price, compare)
    product.card_variant = variant
    product.fit_text = fit_text(product, vehicle)
    product.multi = product.variants.count() > 1
    ship = available(variant.id, "ship") if product.allow_ship else 0
    shops = 0
    if product.allow_install:
        shops = sum(available(variant.id, shop.slug) for shop in Showroom.objects.all())
    product.in_stock = ship + shops > 0
    return product


def home(request):
    vehicle = _vehicle(request)
    now_banners = []
    from django.utils import timezone
    now = timezone.now()
    for banner in Banner.objects.filter(enabled=True):
        if banner.starts_at and banner.starts_at > now:
            continue
        if banner.ends_at and banner.ends_at < now:
            continue
        now_banners.append(banner)
    services = Service.objects.all()
    categories = Category.objects.filter(show_on_home=True)
    featured = [_decorate(item, vehicle) for item in Product.objects.filter(status="published", featured=True).prefetch_related("variants")]
    return render(request, "home.html", {
        "banner": now_banners[0] if now_banners else None,
        "services": services,
        "categories": categories,
        "featured": featured,
        "trust": TrustItem.objects.filter(enabled=True),
        "primary": Showroom.objects.filter(is_primary=True).first(),
    })


def catalog(request, slug=""):
    vehicle = _vehicle(request)
    category = Category.objects.filter(slug=slug).first() if slug else None
    items = Product.objects.filter(status="published").prefetch_related("variants", "vehicles")
    if category:
        items = items.filter(category=category)
    if request.GET.get("stock") == "1":
        items = [item for item in items if _decorate(item, vehicle).in_stock]
    else:
        items = [_decorate(item, vehicle) for item in items]
    sort = request.GET.get("sort") or "new"
    if sort == "price-asc":
        items.sort(key=lambda item: item.card_price)
    elif sort == "price-desc":
        items.sort(key=lambda item: item.card_price, reverse=True)
    elif sort == "discount":
        items.sort(key=lambda item: item.card_off, reverse=True)
    page = max(int(request.GET.get("page") or 1), 1)
    start = (page - 1) * 24
    return render(request, "catalog.html", {
        "category": category,
        "categories": Category.objects.all(),
        "vehicles": Vehicle.objects.all(),
        "selected": vehicle,
        "products": items[start:start + 24],
        "page": page,
        "pages": max((len(items) + 23) // 24, 1),
        "sort": sort,
        "stock": request.GET.get("stock") == "1",
    })


def product(request, slug):
    item = get_object_or_404(Product.objects.prefetch_related("variants", "specs", "vehicles"), slug=slug)
    if item.status == "draft":
        return render(request, "404.html", status=404)
    variants = list(item.variants.all())
    current = next((v for v in variants if v.sku == request.GET.get("v")), variants[0])
    mode = request.GET.get("mode") or ("ship" if item.allow_ship and available(current.id, "ship") else "install")
    shops = []
    for shop in Showroom.objects.all():
        qty = available(current.id, shop.slug)
        if qty:
            shops.append({"shop": shop, "qty": qty})
    shop_slug = request.GET.get("shop") or (shops[0]["shop"].slug if shops else "")
    from .phase2 import current_customer
    customer = current_customer(request)
    owned = None
    if customer:
        owned = Order.objects.filter(customer=customer, status="hoan_thanh", lines__variant=current).exclude(reviews__variant=current).first()
    return render(request, "product.html", {
        "product": item,
        "variants": variants,
        "current": current,
        "price": variant_price(current),
        "compare": variant_compare(current),
        "off": pct(variant_price(current), variant_compare(current)),
        "mode": mode,
        "ship_qty": available(current.id, "ship"),
        "shops": shops,
        "shop_slug": shop_slug,
        "fit_text": fit_text(item, _vehicle(request)),
        "stopped": item.status == "discontinued",
        "reviews": Review.objects.filter(variant__product=item, status="da_duyet"),
        "review_avg": Review.objects.filter(variant__product=item, status="da_duyet").aggregate(avg=Avg("stars"))["avg"],
        "can_review": owned is not None,
    })


@require_POST
def cart_add(request):
    variant = get_object_or_404(Variant.objects.select_related("product"), sku=request.POST.get("sku", ""))
    product = variant.product
    mode = request.POST.get("mode") or "ship"
    qty = max(int(request.POST.get("qty") or 1), 1)
    if product.status != "published":
        messages.error(request, "Sản phẩm không còn mở bán.")
        return redirect(request.POST.get("next") or "cart")
    if mode == "ship" and not product.allow_ship:
        messages.error(request, "Sản phẩm không giao hàng.")
        return redirect("product", slug=product.slug)
    showroom = None
    location = "ship"
    if mode == "install":
        if not product.allow_install:
            messages.error(request, "Sản phẩm không lắp tại showroom.")
            return redirect("product", slug=product.slug)
        showroom = get_object_or_404(Showroom, slug=request.POST.get("shop") or "")
        location = showroom.slug
    cart = _cart(request)
    avail = available(variant.id, location)
    existing = CartLine.objects.filter(cart=cart, variant=variant, mode=mode)
    line = existing.filter(showroom=showroom).first() if showroom else existing.filter(showroom__isnull=True).first()
    current = line.qty if line else 0
    if avail < 1 or current + qty > avail or current + qty > 20:
        messages.error(request, f"Chỉ còn {avail} sản phẩm cho hình thức này.")
    else:
        if line:
            line.qty = current + qty
            line.save(update_fields=["qty"])
        else:
            CartLine.objects.create(cart=cart, variant=variant, mode=mode, showroom=showroom, qty=qty)
        messages.success(request, "Đã thêm " + product.name)
    nxt = request.POST.get("next") or ""
    if nxt.startswith("/"):
        return redirect(nxt)
    return redirect("cart")


def _lines(cart):
    rows = []
    for line in cart.lines.select_related("variant__product", "showroom"):
        location = "ship" if line.mode == "ship" else (line.showroom.slug if line.showroom else "")
        avail = available(line.variant_id, location, ignore_session=cart.session_key) if location else 0
        price = variant_price(line.variant)
        line.unit = price
        line.avail = avail
        line.invalid = "" if avail >= line.qty else ("Hết hàng." if avail < 1 else "Vượt tồn.")
        line.line_total = 0 if line.invalid else price * line.qty
        rows.append(line)
    return rows


def cart_page(request):
    cart = _cart(request)
    lines = _lines(cart)
    modes = []
    for mode in ("ship", "install"):
        group = [line for line in lines if line.mode == mode]
        if group:
            modes.append({
                "mode": mode,
                "lines": group,
                "subtotal": sum(line.line_total for line in group),
                "blocked": any(line.invalid for line in group),
            })
    return render(request, "cart.html", {"lines": lines, "modes": modes, "mixed": len(modes) > 1})


@require_POST
def cart_qty(request):
    line = get_object_or_404(CartLine, pk=request.POST.get("line"), cart=_cart(request))
    delta = int(request.POST.get("dir") or 0)
    location = "ship" if line.mode == "ship" else line.showroom.slug
    avail = available(line.variant_id, location)
    line.qty = max(1, min(line.qty + delta, avail, 20))
    line.save(update_fields=["qty"])
    return redirect("cart")


@require_POST
def cart_remove(request):
    CartLine.objects.filter(pk=request.POST.get("line"), cart=_cart(request)).delete()
    return redirect("cart")


def checkout(request):
    mode = "install" if request.GET.get("mode") == "install" else "ship"
    cart = _cart(request)
    lines = [line for line in _lines(cart) if line.mode == mode and not line.invalid]
    if not lines:
        messages.error(request, "Không có món hợp lệ để thanh toán ở nhóm này.")
        return redirect("cart")
    place_soft_holds(request.session.session_key, lines)
    lines = [line for line in _lines(cart) if line.mode == mode and not line.invalid]
    subtotal = sum(line.line_total for line in lines)
    form = CheckoutForm(request.POST or None, initial={"payment": "cash" if mode == "install" else "transfer", "coupon": request.GET.get("coupon", "")})
    coupon_code = (request.POST.get("coupon") if request.method == "POST" else request.GET.get("coupon")) or ""
    from .phase2 import current_customer, notify_order
    phone_now = (request.POST.get("phone") if request.method == "POST" else "") or (getattr(current_customer(request), "phone", "") or "")
    coupon = coupon_result(coupon_code, subtotal, mode, phone=phone_now, product_ids=[line.variant.product_id for line in lines])
    district = request.POST.get("district") if request.method == "POST" else ""
    fee = SiteFee(mode, subtotal, district, coupon)
    if request.method == "POST" and "dat-hang" in request.POST and form.is_valid():
        data = form.cleaned_data
        if not data["agree"]:
            form.add_error("agree", "Cần đồng ý điều kiện mua hàng.")
            data = None
        error = _checkout_error(mode, data, lines, coupon) if data else "Cần đồng ý điều kiện mua hàng."
        if error:
            form.add_error(None, error)
        elif data["payment"] == "cash" and mode != "install":
            form.add_error("payment", "Đơn giao hàng không thu tiền mặt tại showroom.")
        else:
            showroom = lines[0].showroom if mode == "install" else None
            status = "cho_xac_nhan" if data["payment"] == "cash" else "cho_thanh_toan"
            payload = {
                "name": data["name"],
                "phone": data["phone"],
                "email": data["email"],
                "mode": mode,
                "payment": data["payment"],
                "status": status,
                "paid": False,
                "showroom": showroom,
                "address": (data["address"] + ", " + data["district"]) if mode == "ship" else "",
                "district": data["district"],
                "appointment_date": data["appointment_date"] if mode == "install" else None,
                "appointment_time": data["appointment_time"] if mode == "install" else "",
                "car": data["car"],
                "subtotal": subtotal,
                "discount": coupon["amount"] if coupon["ok"] else 0,
                "fee": fee or 0,
                "total": subtotal - (coupon["amount"] if coupon["ok"] else 0) + (fee or 0),
                "coupon_code": coupon.get("code") or "",
                "customer": current_customer(request),
            }
            if mode == "install" and install_slot_full(showroom, data["appointment_time"], data["appointment_date"]):
                form.add_error("appointment_time", "Khung giờ vừa hết chỗ.")
            else:
                order, err = create_order(request.session.session_key, lines, payload)
                if err:
                    messages.error(request, err)
                    return redirect("cart")
                CartLine.objects.filter(id__in=[line.id for line in lines]).delete()
                notify_order(order)
                if data["payment"] == "gateway":
                    return redirect("gateway", code=order.code)
                return redirect("confirm", code=order.code)
    return render(request, "checkout.html", {
        "form": form,
        "mode": mode,
        "lines": lines,
        "subtotal": subtotal,
        "coupon": coupon,
        "fee": fee,
        "total": max(subtotal - (coupon["amount"] if coupon["ok"] else 0) + (fee or 0), 0),
        "showroom": lines[0].showroom if mode == "install" else None,
        "needs_car": mode == "install" or any(line.variant.product.fitment == "consult" for line in lines),
    })


def SiteFee(mode, subtotal, district, coupon):
    from .models import SiteConfig
    if mode == "install":
        return SiteConfig.load().install_fee
    return ship_fee(subtotal, district, bool(coupon.get("ok") and coupon.get("free_ship")))


def _checkout_error(mode, data, lines, coupon):
    if data["coupon"] and not coupon["ok"]:
        return coupon["message"]
    if mode == "ship":
        if not data["district"] or data["district"] == "Chọn":
            return "Chọn khu vực để tính phí giao."
        if not data["address"]:
            return "Nhập địa chỉ giao hàng."
        if any(line.variant.product.fitment == "consult" for line in lines) and not data["car"]:
            return "Đơn có sản phẩm cần xác nhận độ vừa. Nhập hãng và dòng xe."
    else:
        if not data["appointment_date"]:
            return "Chọn ngày lắp."
        if not data["car"]:
            return "Nhập hãng và dòng xe."
    return ""


def confirm(request, code):
    from .models import Order
    order = get_object_or_404(Order.objects.prefetch_related("lines"), code=code)
    config_bank = order.payment == "transfer" and not order.paid and order.status == "cho_thanh_toan"
    return render(request, "confirm.html", {"order": order, "status_label": STATUS_LABEL.get(order.status, order.status), "show_bank": config_bank})


@require_POST
def cancel(request, code):
    from .models import Order
    order = get_object_or_404(Order, code=code)
    phone = "".join(ch for ch in request.POST.get("phone", "") if ch.isdigit())
    if phone != "".join(ch for ch in order.phone if ch.isdigit()):
        messages.error(request, "Số điện thoại không khớp đơn.")
    elif cancel_order(order):
        messages.success(request, "Đã hủy đơn và nhả hàng giữ.")
    else:
        messages.error(request, "Đơn này không còn hủy được.")
    return redirect("confirm", code=code)


def services(request):
    return render(request, "services.html", {"services": Service.objects.all()})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    form = BookingForm(request.POST or None, service=service)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        if slot_full(data["showroom"], service, data["time"], data["date"]):
            form.add_error("time", "Khung giờ vừa hết chỗ. Chọn giờ khác.")
        else:
            seq = Booking.objects.count() + 1
            Booking.objects.create(
                code=f"LH{seq:06d}",
                name=data["name"],
                phone=data["phone"],
                showroom=data["showroom"],
                service=service,
                date=data["date"],
                time=data["time"],
                car=data["car"],
            )
            messages.success(request, "Đã nhận lịch " + f"LH{seq:06d}")
            return redirect("service", slug=slug)
    return render(request, "service.html", {"service": service, "form": form, "services": Service.objects.all()})


def search(request):
    q = (request.GET.get("q") or "").strip()
    query = fold(q)
    products = []
    services_found = []
    if query:
        for item in Product.objects.filter(status="published").prefetch_related("variants"):
            blob = fold(item.name + " " + item.blurb + " " + " ".join(v.sku for v in item.variants.all()))
            if query in blob:
                products.append(_decorate(item, _vehicle(request)))
        services_found = [item for item in Service.objects.all() if query in fold(item.name + " " + item.summary)]
    articles = []
    if query:
        from django.utils import timezone
        for item in Article.objects.filter(status="published", publish_at__lte=timezone.now()):
            if query in fold(item.title + " " + item.summary + " " + item.body):
                articles.append(item)
    return render(request, "search.html", {"q": q, "products": products, "services": services_found, "articles": articles})


def lookup(request):
    form = LookupForm(request.GET or None)
    order = None
    checked = False
    if request.GET.get("ma") and request.GET.get("phone"):
        checked = True
        from .models import Order
        phone = "".join(ch for ch in request.GET.get("phone") if ch.isdigit())
        found = Order.objects.filter(code__iexact=request.GET.get("ma").strip()).first()
        if found and "".join(ch for ch in found.phone if ch.isdigit()) == phone:
            order = found
    return render(request, "lookup.html", {
        "form": form,
        "order": order,
        "checked": checked,
        "status_label": STATUS_LABEL.get(order.status, "") if order else "",
    })


def showrooms(request):
    return render(request, "showrooms.html", {"showrooms": Showroom.objects.all()})


def account(request):
    return render(request, "account.html")


@require_POST
def set_vehicle(request):
    slug = request.POST.get("vehicle") or ""
    if slug and Vehicle.objects.filter(slug=slug).exists():
        request.session["vehicle"] = slug
    else:
        request.session.pop("vehicle", None)
    nxt = request.POST.get("next") or "/phu-kien/"
    if not nxt.startswith("/"):
        nxt = "/phu-kien/"
    return redirect(nxt)
