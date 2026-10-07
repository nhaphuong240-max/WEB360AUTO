from django.test import TestCase

from store.management.commands.seed import Command
from store.models import Variant
from store.services import coupon_result, excl_from_incl, gross, variant_price


class PricingTests(TestCase):
    def test_seed_prices_match_vat_inclusive_tags(self):
        Command().handle()
        expected = {"COP-DEN": 890000, "SCENT-GO": 219000, "CAM-4K": 1890000, "LASER-2": 8900000}
        for sku, price in expected.items():
            variant = Variant.objects.get(sku=sku)
            self.assertEqual(variant_price(variant), price)
            self.assertEqual(excl_from_incl(price), variant.price_excl)

    def test_coupon_messages(self):
        Command().handle()
        self.assertIn("hết hạn", coupon_result("HETHAN", 900000, "ship")["message"])
        self.assertIn("tối thiểu", coupon_result("THIEU", 900000, "ship")["message"])
        self.assertEqual(coupon_result("GIAM10", 890000, "ship")["amount"], 89000)
        self.assertIn("giao hàng", coupon_result("FREESHIP", 890000, "install")["message"])
