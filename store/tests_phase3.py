from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase

from store.management.commands.seed import Command
from store.models import Booking, ChannelLink, Inventory, NoticeLog, Variant
from store.phase3 import (
    appointment_at,
    create_transfer,
    ingest_channel_message,
    push_channel_reply,
    receive_transfer,
    send_due_reminders,
    ship_transfer,
)


class Phase3Tests(TestCase):
    def setUp(self):
        Command().handle()

    def test_channel_reply_locks_when_disconnected(self):
        talk = ingest_channel_message("zalo", "z1", "Lan", "0912345678", "Xin chào")
        ok, _err = push_channel_reply(talk, "Em nghe")
        self.assertTrue(ok)
        ChannelLink.objects.filter(channel="zalo").update(connected=False)
        ok, err = push_channel_reply(talk, "Gửi tiếp")
        self.assertFalse(ok)
        self.assertEqual(err, "Kênh đang ngắt")
        self.assertEqual(talk.messages.count(), 2)

    def test_transfer_stock_moves_only_when_received(self):
        variant = Variant.objects.get(sku="LUG-20")
        source = Inventory.objects.get(variant=variant, location="ship").on_hand
        dest = Inventory.objects.get(variant=variant, location="q7").on_hand
        ticket, err = create_transfer(variant, 1, "ship", "q7")
        self.assertEqual(err, "")
        self.assertEqual(Inventory.objects.get(variant=variant, location="q7").on_hand, dest)
        self.assertEqual(ship_transfer(ticket), "")
        self.assertEqual(Inventory.objects.get(variant=variant, location="ship").on_hand, source - 1)
        self.assertEqual(Inventory.objects.get(variant=variant, location="q7").on_hand, dest)
        self.assertEqual(receive_transfer(ticket), "")
        self.assertEqual(Inventory.objects.get(variant=variant, location="q7").on_hand, dest + 1)

    def test_reminder_failure_does_not_cancel_booking(self):
        booking = Booking.objects.get(code="LH2026NHAC")
        start = appointment_at(booking)
        with patch("store.phase3.notify", side_effect=RuntimeError("nha mang")):
            send_due_reminders(start - timedelta(minutes=30))
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cho_xac_nhan")
        self.assertIsNone(booking.reminded_at)
        self.assertTrue(NoticeLog.objects.filter(ok=False, target=booking.phone).exists())

    def test_invoice_export_is_not_a_tax_invoice(self):
        client = Client()
        client.force_login(User.objects.get(username="quantri"))
        response = client.get("/hoa-don/?xuat=1", HTTP_HOST="127.0.0.1")
        text = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("không phát hành", text)
        self.assertIn("khong", text)
        self.assertIn("DH2026000012", text)
