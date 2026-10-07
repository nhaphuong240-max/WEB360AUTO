from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .phase2_views import image_ok

from .models import (
    Article,
    ArticleCategory,
    Banner,
    Booking,
    CannedReply,
    ChannelLink,
    Category,
    Conversation,
    Coupon,
    Customer,
    Inventory,
    Order,
    OrderLine,
    Payment,
    Product,
    ProductSpec,
    Receipt,
    Reconciliation,
    ReturnRequest,
    Review,
    Service,
    Showroom,
    SiteConfig,
    SlotCapacity,
    StaffProfile,
    StockTransfer,
    StaticPage,
    TrustItem,
    Variant,
    Vehicle,
)

admin_site = admin.AdminSite(name="a360admin")
admin_site.site_header = "360 Auto Detailing"
admin_site.site_title = "Vận hành"
admin_site.index_title = "Khu vận hành"
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


def _profile(request):
    return StaffProfile.objects.filter(user=request.user).first()


class ShowroomScoped(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        profile = _profile(request)
        if profile and profile.role in {"sales", "manager"} and profile.showroom_id:
            return qs.filter(showroom=profile.showroom)
        return qs


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


class SpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "category", "allow_ship", "allow_install", "featured")
    list_filter = ("status", "category", "fitment")
    inlines = [VariantInline, SpecInline]
    filter_horizontal = ("vehicles",)


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = ("name", "variant_name", "qty", "unit_price")


class OrderAdmin(ShowroomScoped):
    list_display = ("code", "name", "phone", "mode", "status", "total", "showroom", "created_at")
    list_filter = ("status", "mode", "payment")
    inlines = [OrderLineInline]
    actions = ["mark_paid", "mark_done"]

    @admin.action(description="Đánh dấu đã thu")
    def mark_paid(self, request, queryset):
        queryset.update(paid=True, status="cho_xac_nhan")

    @admin.action(description="Chuyển hoàn thành")
    def mark_done(self, request, queryset):
        from django.utils import timezone
        queryset.update(paid=True, status="hoan_thanh", completed_at=timezone.now())


class BookingAdmin(ShowroomScoped):
    list_display = ("code", "service", "showroom", "date", "time", "status", "phone")


admin_site.register(Showroom)
admin_site.register(Vehicle)
admin_site.register(Category)
admin_site.register(Product, ProductAdmin)
admin_site.register(Inventory)
admin_site.register(Service)
admin_site.register(SlotCapacity)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Coupon)
admin_site.register(Order, OrderAdmin)
class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = "__all__"

    def _clean_logo(self, name):
        uploaded = self.cleaned_data.get(name)
        if uploaded and hasattr(uploaded, "read") and not image_ok(uploaded):
            raise forms.ValidationError("Chỉ nhận PNG, JPG hoặc WebP, tối đa 5 MB.")
        return uploaded

    def clean_header_logo(self):
        return self._clean_logo("header_logo")

    def clean_footer_logo(self):
        return self._clean_logo("footer_logo")


class SiteConfigAdmin(admin.ModelAdmin):
    form = SiteConfigForm
    fieldsets = (
        ("Logo", {"fields": ("header_logo", "footer_logo"), "description": "PNG, JPG hoặc WebP. Để trống thì header và footer giữ huy hiệu chữ 360."}),
        ("Liên hệ", {"fields": ("hotline", "email", "zalo_url", "messenger_url")}),
        ("Thanh toán", {"fields": ("bank_name", "bank_account", "bank_holder", "install_fee", "transfer_hold_hours", "gateway")}),
    )


def banner_file_ok(uploaded):
    size = getattr(uploaded, "size", 0) or 0
    head = uploaded.read(16)
    uploaded.seek(0)
    if head[4:8] == b"ftyp" or head[:4] == b"\x1a\x45\xdf\xa3":
        return size <= 30 * 1024 * 1024
    if head.startswith(b"GIF87a") or head.startswith(b"GIF89a"):
        return size <= 5 * 1024 * 1024
    return image_ok(uploaded)


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        media = cleaned.get("media")
        poster = cleaned.get("poster")
        if media and hasattr(media, "read") and not banner_file_ok(media):
            self.add_error("media", "Chỉ nhận ảnh PNG, JPG, WebP, GIF hoặc video MP4, WebM. Ảnh tối đa 5 MB, video tối đa 30 MB.")
        if poster and hasattr(poster, "read") and not image_ok(poster):
            self.add_error("poster", "Ảnh dự phòng chỉ nhận PNG, JPG hoặc WebP, tối đa 5 MB.")
        if not media and not cleaned.get("image"):
            self.add_error("media", "Đính kèm ảnh hoặc video.")
        name = (getattr(media, "name", "") or "").lower()
        if name.endswith((".mp4", ".webm", ".mov")) and not poster and not cleaned.get("image"):
            self.add_error("poster", "Video cần ảnh dự phòng khi không phát được.")
        return cleaned


class BannerAdmin(admin.ModelAdmin):
    form = BannerForm
    list_display = ("title", "enabled", "sort", "attached")
    fieldsets = (
        ("Tệp", {"fields": ("media", "poster", "image"), "description": "Đính kèm ảnh hoặc video. Video không phát tiếng. Ảnh dự phòng hiện khi video lỗi. Để trống tệp thì dùng đường dẫn ảnh cũ."}),
        ("Nội dung", {"fields": ("eyebrow", "title", "subtitle", "cta_label", "cta_url")}),
        ("Lịch", {"fields": ("starts_at", "ends_at", "enabled", "sort")}),
    )

    @admin.display(description="Đính kèm")
    def attached(self, obj):
        if obj.media and obj.is_video:
            return "Video"
        if obj.media:
            return "Ảnh"
        if obj.image:
            return "Ảnh tĩnh"
        return "Chưa có"


admin_site.register(Banner, BannerAdmin)
admin_site.register(TrustItem)
admin_site.register(SiteConfig, SiteConfigAdmin)
admin_site.register(StaffProfile)
admin_site.register(Customer)
admin_site.register(Review)
admin_site.register(Article)
admin_site.register(ArticleCategory)
admin_site.register(StaticPage)
admin_site.register(Conversation)
admin_site.register(ChannelLink)
admin_site.register(StockTransfer)
admin_site.register(CannedReply)
admin_site.register(ReturnRequest)
admin_site.register(Payment)
admin_site.register(Receipt)
admin_site.register(Reconciliation)
