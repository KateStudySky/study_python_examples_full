import pytest
from db_client import StudentTable


db = StudentTable("postgresql+psycopg2://kate_nikonova:12345@localhost:5432/postgres")
TEST_USER_ID = 99999


@pytest.fixture(autouse=True)
def cleanup():
    yield
    db.delete(TEST_USER_ID)


def test_add_student():
    students_before = db.get_all()
    len_before = len(students_before)

    db.create(user_id=TEST_USER_ID,
              level="Middle",
              education_form="Part-time",
              subject_id=2)

    students_after = db.get_all()
    len_after = len(students_after)

    assert len_after - len_before == 1

    created = db.get_by_id(TEST_USER_ID)
    assert len(created) == 1
    assert created[0]["level"] == "Middle"
    assert created[0]["education_form"] == "Part-time"


def test_edit_student():
    db.create(user_id=TEST_USER_ID,
              level="Beginner",
              education_form="Full-time",
              subject_id=1)

    db.update(user_id=TEST_USER_ID,
              level="Senior",
              education_form="Online")

    updated = db.get_by_id(TEST_USER_ID)
    assert len(updated) == 1
    assert updated[0]["level"] == "Senior"
    assert updated[0]["education_form"] == "Online"


def test_delete_student():
    db.create(user_id=TEST_USER_ID,
              level="Beginner",
              education_form="Full-time",
              subject_id=1)
    assert len(db.get_by_id(TEST_USER_ID)) == 1

    db.delete(TEST_USER_ID)
    deleted = db.get_by_id(TEST_USER_ID)
    assert len(deleted) == 0
