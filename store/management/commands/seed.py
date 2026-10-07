from datetime import datetime

from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand
from django.utils import timezone

from store.models import (
    Banner,
    Category,
    Coupon,
    Inventory,
    Order,
    OrderLine,
    Product,
    ProductSpec,
    Service,
    Showroom,
    SiteConfig,
    SlotCapacity,
    StaffProfile,
    TrustItem,
    Variant,
    Vehicle,
)
from django.contrib.auth.hashers import make_password

from datetime import timedelta

from store.models import Article, ArticleCategory, Booking, CannedReply, ChannelLink, Customer, MailTemplate, Service, StaticPage
from store.services import excl_from_incl


def ensure_phase2():
    if Customer.objects.filter(phone="0901234567").exists():
        return
    customer = Customer.objects.create(phone="0901234567", name="Nguyễn An", email="an@example.com", password=make_password("An123456"))
    Order.objects.filter(code="DH2026000012").update(customer=customer, completed_at=timezone.now())
    category = ArticleCategory.objects.create(slug="cham-soc", name="Chăm sóc xe")
    Article.objects.create(
        slug="rua-xe-dung-cach",
        title="Rửa xe đúng cách",
        category=category,
        summary="Hai xô, không rửa dưới nắng gắt.",
        body="Dùng hai xô, găng và khăn riêng. Không rửa xe khi mặt sơn đang nóng.",
        status="published",
        publish_at=timezone.now(),
    )
    StaticPage.objects.create(
        slug="chinh-sach",
        title="Chính sách dữ liệu",
        body="Website thu thập họ tên, điện thoại, email, địa chỉ, thông tin xe, nội dung chat và nhật ký phục vụ đơn hàng.",
        status="published",
    )
    MailTemplate.objects.create(code="tao_don", subject="Đơn {ma_don}", body="Đơn {ma_don} của {ten}, tổng {tong}.")
    CannedReply.objects.create(title="Chào khách", body="360 Auto Detailing đã nhận tin. Bạn cho mình xin dòng xe nhé.")
    StaffProfile.objects.filter(user__username="tuvan").update(ready=True)
    future = timezone.make_aware(datetime(2027, 1, 1, 0, 0))
    Coupon.objects.get_or_create(code="THANHVIEN", defaults={"percent": 5, "members_only": True, "valid_until": future})


def ensure_phase3():
    ChannelLink.objects.get_or_create(channel="zalo", defaults={"label": "Zalo OA", "connected": True})
    ChannelLink.objects.get_or_create(channel="messenger", defaults={"label": "Facebook Page", "connected": True})
    MailTemplate.objects.get_or_create(
        code="nhac_lich",
        defaults={
            "subject": "Nhắc lịch {ma_lich}",
            "body": "{ten} có lịch {ma_lich} lúc {gio_hen} tại {dia_chi}.",
        },
    )
    if Booking.objects.filter(code="LH2026NHAC").exists():
        return
    showroom = Showroom.objects.filter(slug="q7").first()
    service = Service.objects.exclude(slug="ceramic").first() or Service.objects.first()
    if showroom is None or service is None:
        return
    when = timezone.localtime() + timedelta(minutes=90)
    Booking.objects.create(
        code="LH2026NHAC",
        name="Nguyễn An",
        phone="0901234567",
        showroom=showroom,
        service=service,
        date=when.date(),
        time=when.strftime("%H:%M"),
        car="Toyota Camry",
        note="Lịch để thử nhắc tự động",
    )


class Command(BaseCommand):
    help = "Nạp dữ liệu mở bán giai đoạn 1"

    def handle(self, *args, **options):
        if Product.objects.exists():
            ensure_phase2()
            ensure_phase3()
            self.stdout.write("Đã có sản phẩm, bỏ qua seed giai đoạn 1.")
            return
        shops = {}
        for slug, name, address, phone, hours, primary in [
            ("q7", "Quận 7", "215 Nguyễn Hữu Thọ, Tân Hưng, Quận 7, TP. Hồ Chí Minh", "0901 360 360", "08:00–20:00", True),
            ("td", "Thủ Đức", "12 Võ Văn Ngân, Linh Chiểu, TP. Thủ Đức", "0901 360 361", "08:00–20:00", False),
            ("bt", "Bình Thạnh", "88 Xô Viết Nghệ Tĩnh, Bình Thạnh, TP. Hồ Chí Minh", "0901 360 362", "08:00–19:00", False),
        ]:
            shops[slug] = Showroom.objects.create(slug=slug, name=name, address=address, phone=phone, hours=hours, is_primary=primary, email="datlich@360autodetailing.vn")

        cars = {}
        for slug, make, model, year in [("camry", "Toyota", "Camry", 2022), ("civic", "Honda", "Civic", 2021), ("vf8", "VinFast", "VF8", 2024)]:
            cars[slug] = Vehicle.objects.create(slug=slug, make=make, model_name=model, year=year)

        categories = {}
        for sort, slug, name, badge, image, home in [
            (1, "man-hinh-android", "Màn hình Android", "Hot", "img/steer.jpg", True),
            (2, "camera-hanh-trinh", "Camera hành trình", "", "img/svc-front.jpg", True),
            (3, "tham-lot-san", "Thảm lót sàn", "-30%", "img/steer.jpg", True),
            (4, "den-bi-laser", "Đèn bi laser", "", "img/hero5.jpg", True),
            (5, "mam-xe", "Mâm xe", "", "img/rim.jpg", True),
            (6, "cam-bien-lop", "Cảm biến lốp", "-20%", "img/blackcar.jpg", True),
            (7, "phu-kien-cop", "Phụ kiện cốp", "", "img/svc-film.jpg", False),
            (8, "noi-that", "Nội thất", "", "img/steer.jpg", False),
        ]:
            categories[slug] = Category.objects.create(slug=slug, name=name, badge=badge, image=image, show_on_home=home, sort=sort)

        catalog = [
            ("thung-cop-360", "Thùng lưu trữ cốp xe 360", "360 Gear", "phu-kien-cop", "img/svc-film.jpg", "all", [], True, False, 12, True, 1,
             "Chống nước, cố định trong cốp, ngăn đồ gọn.", [("Chất liệu", "Nhựa cứng có gioăng"), ("Xuất xứ", "Lắp ráp trong nước")],
             [("thung-den", "Màu đen", "COP-DEN", 890000, 1690000, 1800, 12, {"q7": 2, "td": 1, "bt": 0})]),
            ("nuoc-hoa-khe-gio", "Nước hoa khe gió", "360 Scent", "noi-that", "img/steer.jpg", "all", [], True, False, 0, True, 2,
             "Kẹp cửa gió, hương gỗ nhẹ.", [("Dung tích", "8 ml"), ("Lắp", "Khe gió điều hòa")],
             [("nh-go", "Hương gỗ", "SCENT-GO", 219000, 390000, 80, 40, {"q7": 6, "td": 4, "bt": 4})]),
            ("oc-mam-titan", "Bộ ốc mâm titan", "360 Wheel", "mam-xe", "img/rim.jpg", "list", ["camry", "civic"], True, True, 12, True, 3,
             "Bộ 20 ốc, kiểu đóng. Cần đúng lazang xe.", [("Số lượng", "20"), ("Kiểu", "Đóng")],
             [("oc-20", "Bộ 20 chiếc", "LUG-20", 259000, 450000, 600, 18, {"q7": 4, "td": 2, "bt": 0})]),
            ("camera-hanh-trinh-4k", "Camera hành trình 4K", "360 Cam", "camera-hanh-trinh", "img/hero5.jpg", "consult", ["camry", "civic", "vf8"], True, True, 12, True, 4,
             "Ghi hình phía trước. Bản Pro thêm camera lùi. Cần xác nhận độ vừa trước khi lắp.", [("Độ phân giải", "4K phía trước"), ("Kết nối", "Wi-Fi")],
             [("cam-std", "Tiêu chuẩn", "CAM-4K", 1890000, 3290000, 350, 6, {"q7": 2, "td": 1, "bt": 0}),
              ("cam-pro", "Pro + camera lùi", "CAM-4K-PRO", 2490000, 3990000, 480, 2, {"q7": 1, "td": 0, "bt": 0})]),
            ("man-hinh-android", "Màn hình Android", "360 Play", "man-hinh-android", "img/steer.jpg", "list", ["camry", "vf8"], True, True, 24, False, 5,
             "Màn hình theo xe, có CarPlay. Chọn kích thước đúng đời xe.", [("Hệ điều hành", "Android"), ("Bảo hành", "24 tháng")],
             [("mh-9", "9 inch", "AND-9", 5490000, 6990000, 1600, 4, {"q7": 1, "td": 1, "bt": 0}),
              ("mh-10", "10 inch", "AND-10", 6290000, 7990000, 1700, 0, {"q7": 0, "td": 1, "bt": 0})]),
            ("tham-lot-san", "Thảm lót sàn", "360 Mat", "tham-lot-san", "img/svc-ceramic.jpg", "list", ["camry", "civic", "vf8"], True, False, 12, False, 6,
             "Thảm khay, ôm sàn theo xe.", [("Chất liệu", "TPE"), ("Bộ", "Hàng trước và sau")],
             [("tham-den", "Đen", "MAT-DEN", 1250000, 1790000, 4200, 9, {"q7": 3, "td": 2, "bt": 1})]),
            ("den-bi-laser", "Đèn bi laser", "360 Light", "den-bi-laser", "img/hero5.jpg", "consult", [], False, True, 12, False, 7,
             "Nâng cấp ánh sáng. Chỉ lắp tại showroom. Cần xác nhận độ vừa trước khi lắp.", [("Nhiệt màu", "5500K"), ("Lắp", "Tại showroom")],
             [("den-bo", "Bộ 2 bi", "LASER-2", 8900000, 12500000, 2200, 0, {"q7": 2, "td": 1, "bt": 0})]),
            ("cam-bien-lop", "Cảm biến áp suất lốp", "360 Safe", "cam-bien-lop", "img/blackcar.jpg", "all", [], True, True, 12, False, 8,
             "Hiển thị áp suất từng lốp, gắn van trong.", [("Cảm biến", "Van trong"), ("Màn hình", "Pin rời")],
             [("tpms", "Bộ 4 van", "TPMS-4", 1590000, 1990000, 500, 1, {"q7": 0, "td": 2, "bt": 1})]),
        ]
        for slug, name, brand, cat, image, fit, fits, ship, install, warranty, featured, sort, blurb, specs, variants in catalog:
            product = Product.objects.create(
                slug=slug, name=name, brand=brand, category=categories[cat], image=image, fitment=fit,
                allow_ship=ship, allow_install=install, warranty_months=warranty, featured=featured,
                home_sort=sort, blurb=blurb, vat_rate=10, status="published",
            )
            if fits:
                product.vehicles.set([cars[item] for item in fits])
            for index, (label, value) in enumerate(specs):
                ProductSpec.objects.create(product=product, name=label, value=value, sort=index)
            for _vid, vname, sku, price, compare, weight, ship_stock, shop_stock in variants:
                variant = Variant.objects.create(
                    product=product, sku=sku, name=vname, weight_grams=weight,
                    price_excl=excl_from_incl(price), price_incl=price,
                    compare_excl=excl_from_incl(compare), compare_incl=compare,
                )
                Inventory.objects.create(variant=variant, location="ship", on_hand=ship_stock)
                for shop_slug, qty in shop_stock.items():
                    Inventory.objects.create(variant=variant, location=shop_slug, on_hand=qty)

        services = [
            ("ceramic", "Phủ ceramic 9H", "img/polish.jpg", 240, 4500000, 12000000, "Lớp phủ bóng sâu, hạn chế bám nước và trầy xước nhẹ.", ["Rửa và khử nhiễm sơn", "Đánh bóng nếu sơn còn tốt", "Phủ ceramic và nghỉ đóng rắn", "Bàn giao phiếu bảo hành"], ["q7", "td"]),
            ("film", "Dán phim cách nhiệt", "img/svc-film.jpg", 150, 2800000, 7500000, "Cản nhiệt, chống UV, giảm chói cho kính lái, sườn và hậu.", ["Đo kính theo xe", "Dán phim và ép mép", "Kiểm tra bọt và tầm nhìn"], ["q7", "td", "bt"]),
            ("leather", "Bọc ghế da", "img/steer.jpg", 480, 6500000, 18000000, "May form ghế zin, giữ túi khí, chọn màu tại showroom.", ["Chọn da và chỉ may", "Lấy form", "Bọc và lắp lại nội thất"], ["q7", "td"]),
            ("detail", "Detailing nội thất", "img/svc-ceramic.jpg", 180, 1200000, 3500000, "Vệ sinh sâu ghế, trần, sàn và khử mùi khoang máy lạnh.", ["Hút bụi toàn khoang", "Xử lý theo chất liệu", "Khử mùi và dưỡng bề mặt"], ["q7", "td", "bt"]),
            ("sound", "Cách âm chống ồn", "img/dash2.jpg", 360, 5000000, 15000000, "Dán cách âm sàn, cửa và hốc bánh.", ["Tháo nội thất cần thiết", "Dán vật liệu", "Lắp lại và chạy thử"], ["q7"]),
            ("wash", "Rửa xe chuyên sâu", "img/svc-wash.jpg", 60, 250000, 650000, "Quy trình 2 xô, dưỡng lốp và kính.", ["Xả và rửa 2 xô", "Làm khô", "Dưỡng lốp, kính"], ["q7", "td", "bt"]),
        ]
        for index, (slug, name, image, minutes, low, high, summary, steps, shop_slugs) in enumerate(services):
            service = Service.objects.create(slug=slug, name=name, image=image, minutes=minutes, price_from=low, price_to=high, summary=summary, steps="\n".join(steps), sort=index)
            service.showrooms.set([shops[item] for item in shop_slugs])
        ceramic = Service.objects.get(slug="ceramic")
        SlotCapacity.objects.create(showroom=shops["q7"], service=ceramic, time="10:00", capacity=0)

        past = timezone.make_aware(datetime(2026, 1, 1, 0, 0))
        future = timezone.make_aware(datetime(2027, 1, 1, 0, 0))
        Banner.objects.create(eyebrow="360 AUTO DETAILING", title="Ưu đãi phụ kiện xe hơi", subtitle="Màn hình Android, camera 360, thảm lót sàn, đèn bi và gói chăm sóc xe — lắp đặt tại showroom, bảo hành rõ ràng.", image="img/svc-front.jpg", cta_label="Mua ngay", cta_url="/phu-kien/", ends_at=future, sort=1)
        Banner.objects.create(title="Flash đã kết thúc", subtitle="Banner hết hạn, không hiện trên trang chủ.", image="img/svc-front.jpg", ends_at=past, sort=2)
        for index, (title, text) in enumerate([
            ("Bảo hành chính hãng", "Hóa đơn và tem bảo hành"),
            ("Giao hàng toàn quốc", "Đóng gói chắc, giao nhanh"),
            ("Showroom trải nghiệm", "Xem hàng thật trước khi lắp"),
            ("Hỗ trợ 24/7", "Tư vấn phụ kiện theo dòng xe"),
        ]):
            TrustItem.objects.create(title=title, text=text, sort=index)
        SiteConfig.load()
        SiteConfig.objects.filter(pk=1).update(zalo_url="https://zalo.me/0901360360", messenger_url="https://m.me/360autodetailing")
        Coupon.objects.create(code="GIAM10", percent=10, min_subtotal=500000, valid_until=future)
        Coupon.objects.create(code="FREESHIP", free_ship=True, valid_until=future)
        Coupon.objects.create(code="HETHAN", percent=10, valid_until=past)
        Coupon.objects.create(code="THIEU", percent=10, min_subtotal=5000000, valid_until=future)

        scent = Variant.objects.get(sku="SCENT-GO")
        order = Order.objects.create(code="DH2026000012", name="Nguyễn An", phone="0901234567", email="an@example.com", mode="ship", payment="transfer", status="hoan_thanh", paid=True, address="12 Nguyễn Huệ, Quận 1", district="Quận 1", subtotal=219000, total=219000)
        OrderLine.objects.create(order=order, variant=scent, slug="nuoc-hoa-khe-gio", name="Nước hoa khe gió", variant_name="Hương gỗ", qty=1, unit_price=219000)

        admin = User.objects.create_superuser("quantri", "quantri@360autodetailing.vn", "360-admin")
        StaffProfile.objects.create(user=admin, role="admin")
        sales = User.objects.create_user("tuvan", "tuvan@360autodetailing.vn", "360-tuvan", is_staff=True)
        sales.user_permissions.set(Permission.objects.filter(content_type__app_label="store"))
        StaffProfile.objects.create(user=sales, role="sales", showroom=shops["q7"])
        ensure_phase2()
        ensure_phase3()
        self.stdout.write(self.style.SUCCESS("Đã nạp dữ liệu giai đoạn 1."))
