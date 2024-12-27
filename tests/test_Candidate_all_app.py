import bcrypt
import pytest
from unittest import mock
from Models.Candidate import Candidate
from datetime import datetime

@pytest.fixture
def mock_db_connection():
    with mock.patch("server.Models.Candidate.get_db_connection") as mock_conn:
        yield mock_conn

def test_get_all_latest_jobs(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {"id": 1, "email": "vishal@gmail.com", "username":"VishalS", "password":"1234"},
        {"id": 2, "email": "allen@gmail.com", "username": "Allen", "password":"1234"},
    ]

    candidate = Candidate.get_all_candidate()

    assert len(candidate) == 2
    assert candidate[0]["email"] == "vishal@gmail.com"
    assert candidate[1]["email"] == "allen@gmail.com"
    assert candidate[0]["username"] == "VishalS"
    assert candidate[1]["username"] == "Allen"
    assert candidate[0]["password"] == "1234"
    assert candidate[1]["password"] == "1234"
    mock_cursor.execute.assert_called_once_with("SELECT * FROM candidate")


def test_already_registered(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor

    email = "existinguser@example.com"
    mock_cursor.fetchone.return_value = {
        'id': 1,
        'username': 'existinguser',
        'password': 'hashedpassword'
    }

    candidate = Candidate.already_registered(email)

    assert candidate is not None
    assert candidate.username == 'existinguser'
    assert candidate.password == 'hashedpassword'
    mock_cursor.execute.assert_called_once_with("SELECT * FROM candidate WHERE email = %s", (email,))
