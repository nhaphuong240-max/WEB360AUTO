from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Showroom(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    hours = models.CharField(max_length=80)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "showroom"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_primary:
            Showroom.objects.exclude(pk=self.pk).update(is_primary=False)


class Vehicle(models.Model):
    slug = models.SlugField(unique=True)
    make = models.CharField(max_length=40)
    model_name = models.CharField(max_length=40)
    year = models.PositiveIntegerField()

    class Meta:
        ordering = ["make", "model_name"]
        verbose_name = "phiên bản xe"

    def __str__(self):
        return f"{self.make} {self.model_name} {self.year}"


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    image = models.CharField(max_length=200, blank=True)
    badge = models.CharField(max_length=20, blank=True)
    show_on_home = models.BooleanField(default=False)
    sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort", "name"]
        verbose_name = "danh mục"

    def __str__(self):
        return self.name


class Product(models.Model):
    FIT = [("all", "Mọi xe"), ("list", "Danh sách phiên bản"), ("consult", "Cần tư vấn")]
    STATUS = [("draft", "Nháp"), ("published", "Đang bán"), ("discontinued", "Ngừng bán")]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=160)
    brand = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    image = models.CharField(max_length=200)
    blurb = models.TextField()
    fitment = models.CharField(max_length=12, choices=FIT, default="all")
    vehicles = models.ManyToManyField(Vehicle, blank=True, related_name="products")
    allow_ship = models.BooleanField(default=True)
    allow_install = models.BooleanField(default=False)
    warranty_months = models.PositiveIntegerField(default=0)
    return_days = models.PositiveIntegerField(default=7)
    vat_rate = models.PositiveSmallIntegerField(default=10)
    status = models.CharField(max_length=16, choices=STATUS, default="published")
    featured = models.BooleanField(default=False)
    home_sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["home_sort", "name"]
        verbose_name = "sản phẩm"

    def __str__(self):
        return self.name


class ProductSpec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specs")
    name = models.CharField(max_length=80)
    value = models.CharField(max_length=160)
    sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort"]


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=80)
    price_excl = models.PositiveIntegerField(help_text="Giá trước VAT, đồng")
    price_incl = models.PositiveIntegerField(default=0, help_text="Giá niêm yết đã gồm VAT")
    compare_excl = models.PositiveIntegerField(default=0)
    compare_incl = models.PositiveIntegerField(default=0)
    weight_grams = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["id"]
        verbose_name = "biến thể"

    def __str__(self):
        return f"{self.product.name} · {self.name}"


class Inventory(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="stocks")
    location = models.CharField(max_length=40)
    on_hand = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("variant", "location")]
        verbose_name = "tồn kho"

    def __str__(self):
        return f"{self.variant.sku} @ {self.location}: {self.on_hand}"


class Reservation(models.Model):
    SOFT = "soft"
    HARD = "hard"
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="reservations")
    location = models.CharField(max_length=40)
    qty = models.PositiveIntegerField()
    kind = models.CharField(max_length=8)
    session_key = models.CharField(max_length=64, blank=True)
    order = models.ForeignKey("Order", null=True, blank=True, on_delete=models.CASCADE, related_name="reservations")
    expires_at = models.DateTimeField(null=True, blank=True)
    released = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Service(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    summary = models.TextField()
    minutes = models.PositiveIntegerField()
    price_from = models.PositiveIntegerField()
    price_to = models.PositiveIntegerField()
    image = models.CharField(max_length=200)
    steps = models.TextField(help_text="Mỗi bước một dòng")
    showrooms = models.ManyToManyField(Showroom, related_name="services")
    sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort"]
        verbose_name = "dịch vụ"

    def __str__(self):
        return self.name

    def step_list(self):
        return [line for line in self.steps.splitlines() if line.strip()]


class SlotCapacity(models.Model):
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    time = models.CharField(max_length=5)
    capacity = models.PositiveIntegerField(default=2)

    class Meta:
        unique_together = [("showroom", "service", "time")]
        verbose_name = "sức chứa khung giờ"


class Booking(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    showroom = models.ForeignKey(Showroom, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.CharField(max_length=5)
    car = models.CharField(max_length=120)
    note = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default="cho_xac_nhan")
    reminded_at = models.DateTimeField(null=True, blank=True)
    reminder_error = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "lịch hẹn"

    def __str__(self):
        return self.code


class Cart(models.Model):
    session_key = models.CharField(max_length=64, unique=True)
    customer = models.ForeignKey("Customer", null=True, blank=True, on_delete=models.SET_NULL, related_name="carts")
    updated_at = models.DateTimeField(auto_now=True)


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="lines")
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10)
    showroom = models.ForeignKey(Showroom, null=True, blank=True, on_delete=models.SET_NULL)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [("cart", "variant", "mode", "showroom")]


class Coupon(models.Model):
    code = models.CharField(max_length=40, unique=True)
    percent = models.PositiveSmallIntegerField(default=0)
    free_ship = models.BooleanField(default=False)
    min_subtotal = models.PositiveIntegerField(default=0)
    valid_until = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(default=0, help_text="0 là không giới hạn")
    max_uses_per_phone = models.PositiveIntegerField(default=0)
    members_only = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, blank=True, related_name="coupons")

    class Meta:
        verbose_name = "mã giảm giá"

    def __str__(self):
        return self.code


class Order(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    mode = models.CharField(max_length=10)
    payment = models.CharField(max_length=12)
    status = models.CharField(max_length=24)
    paid = models.BooleanField(default=False)
    showroom = models.ForeignKey(Showroom, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=40, blank=True)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.CharField(max_length=5, blank=True)
    car = models.CharField(max_length=120, blank=True)
    subtotal = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    fee = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    coupon_code = models.CharField(max_length=40, blank=True)
    customer = models.ForeignKey("Customer", null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    completed_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=12, default="web")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "đơn hàng"

    def __str__(self):
        return self.code


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    variant = models.ForeignKey(Variant, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField()
    name = models.CharField(max_length=160)
    variant_name = models.CharField(max_length=80)
    qty = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()


class Banner(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=160)
    subtitle = models.TextField(blank=True)
    image = models.CharField("Đường dẫn ảnh cũ", max_length=200, blank=True)
    media = models.FileField("Tệp đính kèm", upload_to="banners/", blank=True)
    poster = models.FileField("Ảnh dự phòng", upload_to="banners/", blank=True)
    cta_label = models.CharField(max_length=40, blank=True)
    cta_url = models.CharField(max_length=200, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort"]
        verbose_name = "banner"

    @property
    def is_video(self):
        return (self.media.name or "").lower().endswith((".mp4", ".webm", ".mov"))


class TrustItem(models.Model):
    title = models.CharField(max_length=40)
    text = models.CharField(max_length=80)
    enabled = models.BooleanField(default=True)
    sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort"]
        verbose_name = "cam kết"


class SiteConfig(models.Model):
    header_logo = models.FileField("Logo header", upload_to="brand/", blank=True)
    footer_logo = models.FileField("Logo footer", upload_to="brand/", blank=True)
    hotline = models.CharField(max_length=20, default="0901 360 360")
    email = models.EmailField(default="datlich@360autodetailing.vn")
    zalo_url = models.URLField(blank=True)
    messenger_url = models.URLField(blank=True)
    bank_name = models.CharField(max_length=80, default="Ngân hàng Demo")
    bank_account = models.CharField(max_length=30, default="0123456789")
    bank_holder = models.CharField(max_length=80, default="360 AUTO DETAILING")
    install_fee = models.PositiveIntegerField(default=150000)
    transfer_hold_hours = models.PositiveIntegerField(default=24)
    gateway = models.CharField(max_length=12, default="vnpay")

    class Meta:
        verbose_name = "cấu hình site"

    def __str__(self):
        return "Cấu hình"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class StaffProfile(models.Model):
    ROLES = [
        ("editor", "Biên tập"),
        ("sales", "Tư vấn"),
        ("warehouse", "Thủ kho"),
        ("manager", "Quản lý showroom"),
        ("admin", "Quản trị hệ thống"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLES)
    showroom = models.ForeignKey(Showroom, null=True, blank=True, on_delete=models.SET_NULL)
    ready = models.BooleanField(default=False)
    last_assigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "nhân viên"

    def __str__(self):
        return f"{self.user.username} · {self.get_role_display()}"


class Customer(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=128)
    promo_opt_in = models.BooleanField(default=False)
    delete_requested_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "khách hàng"

    def __str__(self):
        return f"{self.name} · {self.phone}"


class AddressBook(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    line = models.CharField(max_length=200)
    district = models.CharField(max_length=40)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "địa chỉ"


class GarageCar(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cars")
    label = models.CharField(max_length=120)

    class Meta:
        verbose_name = "xe trong garage"


class PhoneCode(models.Model):
    phone = models.CharField(max_length=20)
    purpose = models.CharField(max_length=16)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class OtpGate(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    fail_count = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)


class CouponRedemption(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name="redemptions")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="redemption")
    phone = models.CharField(max_length=20)
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    gateway = models.CharField(max_length=12)
    amount = models.PositiveIntegerField()
    gateway_txn = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "giao dịch cổng"


class Receipt(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="receipt")
    amount = models.PositiveIntegerField()
    gateway_txn = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "phiếu thu"


class Reconciliation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reconciliations")
    gateway_txn = models.CharField(max_length=64)
    reported_amount = models.PositiveIntegerField()
    expected_amount = models.PositiveIntegerField()
    note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "đối soát"


class Review(models.Model):
    STATUS = [("cho_duyet", "Chờ duyệt"), ("da_duyet", "Đã duyệt"), ("tu_choi", "Từ chối")]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reviews")
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews")
    stars = models.PositiveSmallIntegerField()
    body = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS, default="cho_duyet")
    reject_reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("order", "variant")]
        verbose_name = "đánh giá"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to="reviews/")


class ArticleCategory(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "chuyên mục bài viết"

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS = [("draft", "Nháp"), ("published", "Đã đăng")]
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=160)
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT, related_name="articles")
    summary = models.TextField(blank=True)
    body = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS, default="draft")
    publish_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-publish_at"]
        verbose_name = "bài viết"

    def __str__(self):
        return self.title


class StaticPage(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=160)
    body = models.TextField()
    status = models.CharField(max_length=16, default="published")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "trang tĩnh"

    def save(self, *args, **kwargs):
        old_slug = ""
        if self.pk:
            old_slug = StaticPage.objects.filter(pk=self.pk).values_list("slug", flat=True).first() or ""
        super().save(*args, **kwargs)
        if old_slug and old_slug != self.slug:
            PathRedirect.objects.create(
                old_path=f"/trang/{old_slug}/",
                new_path=f"/trang/{self.slug}/",
                until=timezone.localdate() + timedelta(days=180),
            )
            PageVersion.objects.create(page=self, title=self.title, body=self.body)


class PageVersion(models.Model):
    page = models.ForeignKey(StaticPage, on_delete=models.CASCADE, related_name="versions")
    title = models.CharField(max_length=160)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class PathRedirect(models.Model):
    old_path = models.CharField(max_length=200, unique=True)
    new_path = models.CharField(max_length=200)
    until = models.DateField()


class Conversation(models.Model):
    STATUS = [("moi", "Mới"), ("dang_xu_ly", "Đang xử lý"), ("cho_khach", "Chờ khách"), ("da_xong", "Đã xong")]
    session_key = models.CharField(max_length=64, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    showroom = models.ForeignKey(Showroom, null=True, blank=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=16, choices=STATUS, default="moi")
    channel = models.CharField(max_length=12, default="web")
    external_id = models.CharField(max_length=80, blank=True)
    overdue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "hội thoại"


class ChatMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=12)
    body = models.TextField(blank=True)
    image = models.FileField(upload_to="chat/", blank=True)
    internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class CannedReply(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()

    class Meta:
        verbose_name = "câu trả lời mẫu"


class ReturnRequest(models.Model):
    STATUS = [("cho_duyet", "Chờ duyệt"), ("cho_hang", "Chờ hàng về"), ("da_hoan", "Đã hoàn tiền"), ("tu_choi", "Từ chối")]
    code = models.CharField(max_length=20, unique=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="returns")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="returns")
    reason = models.TextField()
    resolution = models.CharField(max_length=16, default="")
    status = models.CharField(max_length=16, choices=STATUS, default="cho_duyet")
    customer_note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "phiếu đổi trả"


class ReturnLine(models.Model):
    request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name="lines")
    order_line = models.ForeignKey(OrderLine, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()


class Refund(models.Model):
    request = models.OneToOneField(ReturnRequest, on_delete=models.CASCADE, related_name="refund")
    amount = models.PositiveIntegerField()
    gateway_refund_id = models.CharField(max_length=64, blank=True)
    transfer_receipt = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MailTemplate(models.Model):
    code = models.CharField(max_length=40, unique=True)
    subject = models.CharField(max_length=160)
    body = models.TextField()

    class Meta:
        verbose_name = "mẫu thư"


class NoticeLog(models.Model):
    channel = models.CharField(max_length=16)
    target = models.CharField(max_length=120)
    subject = models.CharField(max_length=160)
    body = models.TextField()
    ok = models.BooleanField(default=True)
    error = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ChannelLink(models.Model):
    CHANNELS = [("zalo", "Zalo OA"), ("messenger", "Messenger")]
    channel = models.CharField(max_length=12, choices=CHANNELS, unique=True)
    label = models.CharField(max_length=40)
    connected = models.BooleanField(default=True)

    class Meta:
        verbose_name = "kênh chat"

    def __str__(self):
        return self.label


class StockTransfer(models.Model):
    STATUS = [
        ("cho_xuat", "Chờ xuất"),
        ("dang_di", "Đang trên đường"),
        ("da_nhan", "Đã nhận"),
        ("da_huy", "Đã hủy"),
    ]
    code = models.CharField(max_length=20, unique=True)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    source = models.CharField(max_length=40)
    destination = models.CharField(max_length=40)
    status = models.CharField(max_length=16, choices=STATUS, default="cho_xuat")
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "phiếu điều chuyển"

    def __str__(self):
        return self.code
