# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Booking, Slot
from tests.conftest import AUTH


def test_AC_BKG_01(client, db, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ และที่นั่งว่างของช่วงนั้นเป็น 0
    assert res.status_code == 201
    assert res.json()["slot_id"] == slot.id
    assert db.get(Slot, slot.id).remaining == 0
    assert db.query(Booking).count() == 1


def test_TC_BKG_01_4_remaining_decrements(client, db, make_slot):
    """TC-BKG-01-4: เมื่อมีที่นั่งว่างหลายที่ การจองควรลดจำนวนที่นั่งคงเหลือ"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 3 ที่
    slot = make_slot(start="09:00", remaining=3)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ และจำนวนที่นั่งคงเหลือลดจาก 3 เหลือ 2
    assert res.status_code == 201
    assert db.get(Slot, slot.id).remaining == 2
    assert db.query(Booking).count() == 1


def test_TC_BKG_01_5_queue_no_generated(client, db, make_slot):
    """TC-BKG-01-5: หลังจองสำเร็จ ระบบต้องส่งกลับ queue_no ที่ถูกสร้าง"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 2 ที่
    slot = make_slot(start="09:00", remaining=2)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: response ต้องมี queue_no และข้อมูลการจองต้องถูกบันทึกพร้อมค่านี้
    assert res.status_code == 201
    payload = res.json()
    assert payload["queue_no"]
    booking = db.query(Booking).filter_by(slot_id=slot.id).first()
    assert booking is not None
    assert booking.queue_no == payload["queue_no"]


def test_TC_BKG_01_2_last_seat_booking(client, db, make_slot):
    """TC-BKG-01-2: จองครั้งสุดท้ายของช่วงเวลาต้องทำให้ remaining เป็น 0"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่ และเป็นการจองครั้งสุดท้าย
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; แสดงหมายเลขคิว; และ remaining เป็น 0
    assert res.status_code == 201
    assert db.get(Slot, slot.id).remaining == 0
    assert res.json()["queue_no"]


def test_TC_BKG_01_3_unverified_user(client, db, make_slot):
    """TC-BKG-01-3: ยังไม่ได้ยืนยันตัวตน ต้องปฏิเสธการจองและไม่บันทึกคิวใหม่"""
    # Given: ผู้ใช้ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: พยายามยืนยันการจองโดยไม่มี Authorization header
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ระบบต้องปฏิเสธการจอง ไม่บันทึกการจองใหม่ และยังคงที่นั่งว่างเหมือนเดิม
    assert res.status_code == 401
    assert res.json()["detail"] == "ยังไม่ได้ยืนยันตัวตน"
    assert db.query(Booking).count() == 0
    assert db.get(Slot, slot.id).remaining == 1


def test_TC_BKG_01_6_missing_slot(client, db, make_slot):
    """TC-BKG-01-6: slot_id ที่ไม่พบต้องตอบ 404 และไม่สร้างการจอง"""
    # Given: ยืนยันตัวตนแล้ว แต่ slot_id ที่ส่งไม่มีอยู่จริง
    nonexistent_slot_id = 999999

    # When: พยายามยืนยันการจองด้วย slot_id ที่ไม่มี
    res = client.post("/bookings", json={"slot_id": nonexistent_slot_id}, headers=AUTH)

    # Then: ต้องปฏิเสธการจองด้วย 404 และไม่บันทึกการจองใหม่
    assert res.status_code == 404
    assert db.query(Booking).count() == 0
