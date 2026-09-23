from sqlalchemy import inspect

from app.db.models import Base
from app.db.session import engine


def test_T01_database_schema_has_booking_tables():
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    assert {"slots", "bookings", "audit_logs"}.issubset(tables)

    slot_columns = {column["name"] for column in inspector.get_columns("slots")}
    booking_columns = {column["name"] for column in inspector.get_columns("bookings")}
    audit_columns = {column["name"] for column in inspector.get_columns("audit_logs")}

    assert {"slot_date", "start_time", "package_code", "capacity", "remaining"}.issubset(slot_columns)
    assert {"hn", "slot_id", "booking_date", "queue_no", "status", "created_at"}.issubset(booking_columns)
    assert "national_id" not in booking_columns
    assert {"actor_id", "action", "hn", "accessed_at"}.issubset(audit_columns)
