import sqlite3

import pytest

from taskmanager.models import Task, User
from taskmanager import queries


@pytest.fixture
def manager(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    monkeypatch.setattr(queries, "get_connection", lambda: conn)
    qm = queries.QueryManager()
    yield qm
    conn.close()


def _user(**overrides):
    data = {
        "first_name": "Raghuram",
        "second_name": "Pentela",
        "email": "raghuram@example.com",
        "password_hash": "hashed-secret",
    }
    data.update(overrides)
    return User(**data)


def _task(user_id, **overrides):
    data = {
        "user_id": user_id,
        "task_name": "exam",
        "task_status": "incomplete",
        "priority": 3,
        "difficulty": "LOW",
        "created_date": None,
        "deadline": "2026-09-12",
    }
    data.update(overrides)
    return Task(**data)


def test_init_creates_users_and_tasks_tables(manager):
    cursor = manager.conn.cursor()
    tables = {
        row[0]
        for row in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    assert "USERS" in tables
    assert "TASKS" in tables


def test_create_new_user_returns_id_and_persists_row(manager):
    user_id = manager.createNewUser(_user())

    assert isinstance(user_id, int)
    assert user_id > 0

    row = manager.conn.execute(
        "SELECT USER_ID, FIRST_NAME, SECOND_NAME, EMAIL FROM USERS WHERE USER_ID=?",
        (user_id,),
    ).fetchone()
    assert tuple(row) == (user_id, "Raghuram", "Pentela", "raghuram@example.com")


def test_create_new_user_rejects_duplicate_email(manager):
    manager.createNewUser(_user())

    with pytest.raises(sqlite3.IntegrityError):
        manager.createNewUser(_user(first_name="Other", second_name="Person"))


def test_update_user_changes_requested_column(manager):
    user_id = manager.createNewUser(_user())

    manager.updateUser(user_id, "FIRST_NAME", "Ram")

    first_name = manager.conn.execute(
        "SELECT FIRST_NAME FROM USERS WHERE USER_ID=?",
        (user_id,),
    ).fetchone()[0]
    assert first_name == "Ram"


def test_delete_user_removes_row(manager):
    user_id = manager.createNewUser(_user())

    manager.deleteUser(user_id)

    remaining = manager.conn.execute("SELECT COUNT(*) FROM USERS").fetchone()[0]
    assert remaining == 0


def test_create_task_returns_id_and_persists_row(manager):
    user_id = manager.createNewUser(_user())
    task_id = manager.createTask(_task(user_id))

    assert isinstance(task_id, int)
    assert task_id > 0

    row = manager.conn.execute(
        "SELECT TASK_ID, USER_ID, TASK_NAME, TASK_STATUS, PRIORITY, DIFFICULTY, DEADLINE "
        "FROM TASKS WHERE TASK_ID=?",
        (task_id,),
    ).fetchone()
    assert tuple(row) == (task_id, user_id, "exam", "incomplete", 3, "LOW", "2026-09-12")


def test_create_task_requires_existing_user(manager):
    with pytest.raises(sqlite3.IntegrityError):
        manager.createTask(_task(user_id=999))


def test_get_task_status_returns_status_for_task(manager):
    user_id = manager.createNewUser(_user())
    task_id = manager.createTask(_task(user_id, task_status="incomplete"))
    status = manager.getTaskStatus(task_id)
    assert status == [("incomplete",)]


def test_get_task_status_returns_empty_for_missing_task(manager):
    assert manager.getTaskStatus(999) == []


def test_complete_task_sets_status_to_completed(manager):
    user_id = manager.createNewUser(_user())
    task_id = manager.createTask(_task(user_id))

    manager.completeTask(task_id)

    status = manager.conn.execute(
        "SELECT TASK_STATUS FROM TASKS WHERE TASK_ID=?",
        (task_id,),
    ).fetchone()[0]
    assert status == "COMPLETED"


def test_get_id_by_name_returns_matching_task_ids(manager):
    user_id = manager.createNewUser(_user())
    task_id = manager.createTask(_task(user_id, task_name="exam"))
    manager.createTask(_task(user_id, task_name="homework"))

    result = manager.getIdByName("exam", user_id)

    assert result == [(task_id,)]


def test_get_id_by_name_does_not_match_other_users(manager):
    user_a = manager.createNewUser(_user())
    user_b = manager.createNewUser(_user(email="other@example.com"))
    manager.createTask(_task(user_a, task_name="exam"))

    assert manager.getIdByName("exam", user_b) == []


def test_update_task_updates_listed_columns(manager):
    user_id = manager.createNewUser(_user())
    task_id = manager.createTask(_task(user_id))

    manager.updateTask(task_id, ["TASK_NAME", "PRIORITY"], ["revision", 5])

    row = manager.conn.execute(
        "SELECT TASK_NAME, PRIORITY FROM TASKS WHERE TASK_ID=?",
        (task_id,),
    ).fetchone()
    assert tuple(row) == ("revision", 5)


def test_delete_task_removes_row(manager):
    user_id = manager.createNewUser(_user())
    task_id = manager.createTask(_task(user_id))

    manager.deleteTask(task_id)
    remaining = manager.conn.execute("SELECT COUNT(*) FROM TASKS").fetchone()[0]

    assert remaining == 0


def test_get_user_by_email_and_list_tasks(manager):
    user_id = manager.createNewUser(_user())
    other_id = manager.createNewUser(_user(email="other@example.com"))
    task_id = manager.createTask(_task(user_id))
    manager.createTask(_task(other_id, task_name="other"))

    found = manager.getUserByEmail("raghuram@example.com")
    assert found is not None
    assert found.user_id == user_id
    assert found.password_hash == "hashed-secret"

    tasks = manager.listTasks(user_id)
    assert [task.task_id for task in tasks] == [task_id]
