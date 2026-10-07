from django import forms

from .models import Service, Showroom
from .services import SLOTS

DISTRICTS = ["Quận 7", "Quận 1", "Thủ Đức", "Khác"]


class CheckoutForm(forms.Form):
    name = forms.CharField(label="Họ tên", max_length=120)
    phone = forms.RegexField(label="Số điện thoại", regex=r"^0\d{9}$", error_messages={"invalid": "Nhập đủ 10 số, bắt đầu bằng 0."})
    email = forms.EmailField(label="Email", required=False)
    district = forms.ChoiceField(label="Khu vực", required=False, choices=[("", "Chọn")] + [(item, item) for item in DISTRICTS])
    address = forms.CharField(label="Địa chỉ", required=False, max_length=200)
    appointment_date = forms.DateField(label="Ngày", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    appointment_time = forms.ChoiceField(label="Khung giờ", required=False, choices=[(item, item) for item in SLOTS])
    car = forms.CharField(label="Xe", required=False, max_length=120)
    coupon = forms.CharField(label="Mã giảm giá", required=False)
    payment = forms.ChoiceField(choices=[("cash", "Tiền mặt tại showroom"), ("transfer", "Chuyển khoản"), ("gateway", "Cổng thanh toán")])
    agree = forms.BooleanField(label="Tôi đồng ý điều kiện mua hàng", required=False)


class BookingForm(forms.Form):
    name = forms.CharField(label="Họ tên", max_length=120)
    phone = forms.RegexField(label="Số điện thoại", regex=r"^0\d{9}$", error_messages={"invalid": "Nhập đủ 10 số, bắt đầu bằng 0."})
    showroom = forms.ModelChoiceField(label="Showroom", queryset=Showroom.objects.none())
    date = forms.DateField(label="Ngày", widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.ChoiceField(label="Giờ", choices=[(item, item) for item in SLOTS])
    car = forms.CharField(label="Dòng xe", max_length=120)

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        if service is not None:
            self.fields["showroom"].queryset = service.showrooms.all()


class LookupForm(forms.Form):
    ma = forms.CharField(label="Mã đơn")
    phone = forms.CharField(label="Số điện thoại đặt hàng")
