import pytest
from unittest import mock
from server.Models.Latest_Jobs import Latest_Jobs 
from datetime import datetime

@pytest.fixture
def mock_db_connection():
    with mock.patch("server.Models.Latest_Jobs.get_db_connection") as mock_conn:
        yield mock_conn

def test_get_all_latest_jobs(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {"job_id": 1, "job_title": "Banking Process Associate", "date_posted":"2022-01-01 10:00:00"},
        {"job_id": 2, "job_title": "Medical Gastroenterologist", "date_posted": "2022-01-02 12:00:00"},
    ]

    latest_jobs = Latest_Jobs.get_all_latest_jobs()

    assert len(latest_jobs) == 2
    assert latest_jobs[0]["job_title"] == "Banking Process Associate"
    assert latest_jobs[1]["job_title"] == "Medical Gastroenterologist"
    assert latest_jobs[0]["date_posted"] == "2022-01-01 10:00:00"
    assert latest_jobs[1]["date_posted"] == "2022-01-02 12:00:00"
    mock_cursor.execute.assert_called_once_with("SELECT * FROM latest_jobs")

def test_create_latest_job(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None
    mock_db_connection.return_value.commit.return_value = None

    Latest_Jobs.create_latest_job(
        job_id=1,
        job_title="Software Engineer",
        salary=100000,
        experience="3-5 years",
        education="Bachelors",
        date_posted=datetime(2023, 1, 1),
        job_org="Company XYZ",
        location="San Francisco",
    )

    mock_cursor.execute.assert_called_with(
        "INSERT INTO latest_jobs (job_id, job_title, salary, experience, education, date_posted, job_org, location) VALUE(%s, %s, %s, %s, %s, %s, %s, %s)",
        (1, "Software Engineer", 100000, "3-5 years", "Bachelors", datetime(2023, 1, 1), "Company XYZ", "San Francisco")
    )

    mock_db_connection.return_value.commit.assert_called_once()

def test_delete_lastest_job(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None  # Simulate the execution without errors
    mock_db_connection.return_value.commit.return_value = None  # Simulate commit success

    Latest_Jobs.delete_latest_job(1)

    mock_cursor.execute.assert_called_with("DELETE FROM latest_jobs WHERE job_id = %s", (1,))
    mock_db_connection.return_value.commit.assert_called_once()