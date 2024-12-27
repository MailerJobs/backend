import pytest
from unittest import mock
from Models.Jobs import Jobs 
from datetime import datetime

@pytest.fixture
def mock_db_connection():
    with mock.patch("server.Models.Jobs.get_db_connection") as mock_conn:
        yield mock_conn

def test_get_all_jobs(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {"job_id": 1, "job_title": "Software Engineer", "Posted_Date": datetime(2022, 12, 1, 10, 0)},
        {"job_id": 2, "job_title": "Data Scientist", "Posted_Date": datetime(2023, 1, 10, 12, 0)},
    ]

    jobs = Jobs.get_all_jobs()

    assert len(jobs) == 2
    assert jobs[0]["job_title"] == "Software Engineer"
    assert jobs[1]["job_title"] == "Data Scientist"
    assert jobs[0]["Posted_Date"] == "2022-12-01 10:00:00"
    assert jobs[1]["Posted_Date"] == "2023-01-10 12:00:00"

def test_get_jobs_by_filters_with_skills(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {"job_id": 1, "job_title": "Software Engineer", "Posted_Date": datetime(2022, 12, 1, 10, 0)},
        {"job_id": 2, "job_title": "Data Scientist", "Posted_Date": datetime(2023, 1, 10, 12, 0)},
    ]
    
    filtered_jobs = Jobs.get_jobs_by_filters(
        location="San Francisco",
        date_posted="Last 24 Hours",
        experience="3-5 years",
        sector="Technology",
        jobType="Full-time",
        skills="Python"
    )

    # Assert that the query has been executed with the appropriate filters
    mock_cursor.execute.assert_called_with(
        mock.ANY,  # You can refine this further to match the exact query executed
        mock.ANY  # Similarly, refine the expected parameters if needed
    )
    
    assert len(filtered_jobs) == 2
    assert filtered_jobs[0]["job_title"] == "Software Engineer"

def test_get_job_by_id(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"job_id": 1, "job_title": "Software Engineer", "Posted_Date": datetime(2022, 12, 1, 10, 0)}

    job = Jobs.get_job_by_id(1)
    expected_datetime = datetime(2022, 12, 1, 10, 0)
    job["Posted_Date"] =expected_datetime.strftime('%Y-%m-%d %H:%M:%S')

    assert job["job_id"] == 1
    assert job["job_title"] == "Software Engineer"
    assert job["Posted_Date"] == "2022-12-01 10:00:00"

def test_create_job(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None  # Simulate the execution without errors
    mock_db_connection.return_value.commit.return_value = None  # Simulate commit success

    # Assuming we call the create_job function with the appropriate arguments
    Jobs.create_job(
        job_id=1,
        job_title="Software Engineer",
        salary=100000,
        experience="3-5 years",
        education="Bachelors",
        date_posted=datetime(2023, 1, 1),
        job_org="Company XYZ",
        location="San Francisco",
        image_url="image_url",
        job_description="A job description",
        sector="Technology"
    )

    # Check if the execute method was called with the expected query and parameters
    mock_cursor.execute.assert_called_with(
        "INSERT INTO jobs (job_id, job_title, salary, experience, education, date_posted, job_org, location, image_url, job_description, sector) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (1, "Software Engineer", 100000, "3-5 years", "Bachelors", datetime(2023, 1, 1), "Company XYZ", "San Francisco", "image_url", "A job description", "Technology")
    )

    # Check if commit was called
    mock_db_connection.return_value.commit.assert_called_once()

def test_delete_job(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None  # Simulate the execution without errors
    mock_db_connection.return_value.commit.return_value = None  # Simulate commit success

    Jobs.delete_job(1)

    mock_cursor.execute.assert_called_with("DELETE FROM jobs WHERE job_id = %s", (1,))
    mock_db_connection.return_value.commit.assert_called_once()