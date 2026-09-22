import sqlite3

import pytest

from taskmanager.queries import QueryManager, query_manager_session
from taskmanager.schemas import TaskCreate, TaskUpdate, UserCreate, UserLogin
from taskmanager.services import (
    AuthError,
    NotFoundError,
    complete_task,
    create_task_for_user,
    delete_task,
    get_task,
    list_user_tasks,
    login_user,
    register_user,
    update_task,
)


@pytest.fixture
def manager(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    monkeypatch.setattr("taskmanager.queries.get_connection", lambda: conn)
    qm = QueryManager()
    yield qm
    conn.close()


def _register(manager, email="raghuram@example.com"):
    return register_user(
        manager,
        UserCreate(
            first_name="Raghuram",
            second_name="Pentela",
            email=email,
            password="secret123",
        ),
    )


def test_register_and_login_round_trip(manager):
    created = _register(manager)
    assert created.email == "raghuram@example.com"
    assert created.user_id > 0

    logged_in = login_user(
        manager,
        UserLogin(email="raghuram@example.com", password="secret123"),
    )
    assert logged_in.user_id == created.user_id


def test_register_rejects_duplicate_email(manager):
    _register(manager)
    with pytest.raises(AuthError):
        _register(manager)


def test_login_rejects_bad_password(manager):
    _register(manager)
    with pytest.raises(AuthError):
        login_user(
            manager,
            UserLogin(email="raghuram@example.com", password="wrongpass"),
        )


def test_task_lifecycle_for_user(manager):
    user = _register(manager)
    created = create_task_for_user(
        manager,
        user.user_id,
        TaskCreate(
            task_name="exam",
            priority=3,
            difficulty="LOW",
            deadline="2026-09-12",
        ),
    )
    assert created.user_id == user.user_id
    assert created.task_status == "NOT STARTED"

    listed = list_user_tasks(manager, user.user_id)
    assert len(listed) == 1
    assert listed[0].task_id == created.task_id

    updated = update_task(
        manager,
        created.task_id,
        TaskUpdate(task_name="revision", priority=5),
        user_id=user.user_id,
    )
    assert updated.task_name == "revision"
    assert updated.priority == 5

    completed = complete_task(manager, created.task_id, user_id=user.user_id)
    assert completed.task_status == "COMPLETED"

    delete_task(manager, created.task_id, user_id=user.user_id)
    with pytest.raises(NotFoundError):
        get_task(manager, created.task_id, user_id=user.user_id)


def test_query_manager_session_closes_owned_connection(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    monkeypatch.setattr("taskmanager.queries.get_connection", lambda: conn)

    with query_manager_session() as manager:
        assert manager.getUserById(1) is None
