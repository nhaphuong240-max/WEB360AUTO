from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from store.management.commands.seed import Command
from store.models import Order, Payment, Receipt, Reconciliation, Review
from store.phase2 import check_otp, issue_otp, record_customer_message, settle_gateway, shop_open
from store.models import Conversation


class Phase2Tests(TestCase):
    def setUp(self):
        Command().handle()

    def test_otp_locks_after_five_bad_codes(self):
        code, err = issue_otp("0909000001", "register")
        self.assertEqual(err, "")
        for _ in range(4):
            ok, _message = check_otp("0909000001", "register", "000000")
            self.assertFalse(ok)
        ok, message = check_otp("0909000001", "register", "000000")
        self.assertFalse(ok)
        self.assertIn("khóa", message)
        self.assertNotEqual(code, "123456")

    def test_gateway_success_twice_is_one_receipt(self):
        order = Order.objects.get(code="DH2026000012")
        order.payment = "gateway"
        order.paid = False
        order.status = "cho_thanh_toan"
        order.total = 219000
        order.save()
        settle_gateway(order, "PAY-TEST", 219000, True)
        settle_gateway(order, "PAY-TEST", 219000, True)
        order.refresh_from_db()
        self.assertTrue(order.paid)
        self.assertEqual(Receipt.objects.filter(order=order).count(), 1)
        self.assertEqual(Payment.objects.filter(gateway_txn="PAY-TEST", status="success").count(), 1)

    def test_amount_mismatch_stays_unpaid(self):
        order = Order.objects.get(code="DH2026000012")
        order.paid = False
        order.status = "cho_thanh_toan"
        order.total = 219000
        order.save()
        settle_gateway(order, "PAY-LECH", 1000, True)
        order.refresh_from_db()
        self.assertFalse(order.paid)
        self.assertTrue(Reconciliation.objects.filter(order=order, gateway_txn="PAY-LECH").exists())

    def test_review_requires_completed_order(self):
        self.assertFalse(Review.objects.filter(status="da_duyet").exists())

    def test_after_hours_auto_message(self):
        closed = timezone.localtime().replace(hour=21, minute=30, second=0, microsecond=0)
        open_now, _showroom = shop_open(closed)
        self.assertFalse(open_now)
        talk = Conversation.objects.create(channel="web")
        record_customer_message(talk, "Còn lịch không?", moment=closed)
        self.assertTrue(talk.messages.filter(sender="he_thong").exists())
