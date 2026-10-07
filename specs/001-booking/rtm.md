# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:33 | test: 10 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | backend/tests/test_AC_BKG_05.py:test_AC_BKG_05 (ผ่าน) | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | ไม่มีโค้ดที่ตรวจจับคิววันเดียวกัน | ไม่มี test ในโค้ด (ยังไม่ถึง) | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ไม่มีโค้ดแสดง 3 ตัวเลือกและแนะนำช่วงใกล้สุด | ไม่มี test ในโค้ด (ยังไม่ถึง) | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/service.py: create_booking, next_queue_no; backend/app/booking/router.py: create_booking | backend/tests/test_AC_BKG_01.py:test_AC_BKG_01 และ 6 test (ผ่าน) | รอ Q-xx |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มีคิวส่งซ้ำหรือการ retry แจ้งเตือน | ไม่มี test ในโค้ด (ยังไม่ถึง) | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02, T-10 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | ไม่มี test ที่ตรวจเปลี่ยนแพ็กเกจแบบเต็ม (ยังไม่ถึง) | ยังไม่ถึง |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | backend/tests/test_AC_BKG_05.py:test_AC_BKG_05 (ผ่าน) | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มี TLS/HTTPS configuration ในโค้ด | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มี retry queue / resend logic | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี UX flow หรือการวัด 3 นาทีจริง | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL; backend/app/db/session.py: get_db | ไม่มี test ตรวจ PostgreSQL จริง (เคยใช้ SQLite ใน test) | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 | backend/app/db/models.py: AuditLog แต่ไม่มีบันทึกจริงใน middleware หรือ endpoint | ไม่มี test | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC แต่สอดคล้อง FR-BKG-04 | T-03 | backend/app/auth/idp.py: get_verified_hn | backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_3_unverified_user (ผ่าน) | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | ไม่มีแบบจำลอง HIS client หรือการค้น HN | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | ไม่มี AC | T-07 | ไม่มี queue/notify implementation | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | hardcoded `DAYS_AHEAD = 14` แทน 30 วันตาม spec และไม่มีการคำนวณช่วงเวลาที่ยังคงว่างตามแพ็กเกจที่ใช้อย่างสมบูรณ์ |
| backend/app/booking/service.py: next_queue_no | FR-BKG-04, Q-02 | ไม่ครบ | เลือกรูปแบบ `A001` และนับต่อวันโดยอิงแค่ booking_date แม้ spec ยังมี Q-02 ที่ยังไม่ได้ตอบ |
| backend/app/booking/router.py: create_booking | FR-BKG-04, IF-IDP-01 | ครบบางส่วน | ตรวจสิทธิ์ยืนยันตัวตนและบันทึก booking ได้ แต่ยังไม่มี logic สำหรับคิวไม่ซ้ำวันเดียวกันหรือคิวส่งข้อความซ้ำ |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ครบ | ตรวจ `Authorization` header และปฏิเสธเมื่อยังไม่ได้ยืนยันตัวตน ตาม spec |
| backend/app/config.py: DATABASE_URL | CON-TECH-01 | ครบบางส่วน | ใช้ `DATABASE_URL` สำหรับ PostgreSQL ตาม spec แต่ fallback เป็น SQLite ทำให้ local test ผ่านได้ โดยไม่บังคับ PostgreSQL จริง |
| backend/app/db/models.py: AuditLog | DOM-PDPA-01 | ไม่ครบ | มีตาราง `audit_logs` แต่ไม่มีบันทึกเหตุการณ์จริง เมื่อเข้าถึงข้อมูลการจอง |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | เดา Q-xx | backend/app/booking/service.py: next_queue_no | FR-BKG-04, Q-02 | โค้ดกำหนดรูปแบบคิวเป็น `A001` และนับต่อวันจาก `booking_date` แม้ Q-02 ยังไม่ได้คำตอบจากเจ้าหน้าที่เวชระเบียน จึงเป็นการตัดสินใจแทนทีม | เพิ่ม Q-02 |
| F-002 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py: list_available_slots | FR-BKG-01 | `DAYS_AHEAD = 14` แทนค่าที่ spec ระบุ "ภายใน 30 วันข้างหน้า" และ API ส่งกลับเฉพาะ 14 วันเท่านั้น | แก้โค้ด |
| F-003 | โค้ดไม่มี FR | backend/app/db/models.py: AuditLog | DOM-PDPA-01 | ตาราง `audit_logs` มีอยู่แล้ว แต่ไม่พบการเรียกเขียน log ใน routing หรือ middleware เมื่อมีการเข้าถึงข้อมูลผู้รับบริการ จึงไม่สามารถยืนยันว่า requirement นี้เป็นจริง | แก้โค้ด |
| F-004 | test อ่อน | backend/tests/test_AC_BKG_01.py:test_AC_BKG_01 | AC-BKG-01 | test ตรวจเพียง `status_code == 201` และไม่ assert ว่าค่าที่นั่งจริงลดลงพอดี 0 หรือ queue_no ถูกบันทึกผิด/ถูกต้อง แม้โค้ดมีการตัดที่นั่งจริง | แก้ test |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| ไม่มี | ยังไม่มีข้อค้นพบที่ได้รับการแก้ไขในรอบนี้ | ตรวจจาก code และ test ปัจจุบัน |
