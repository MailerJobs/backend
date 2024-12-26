import pytest
from unittest import mock
from server.Models.Required_Skills import Skills 
from datetime import datetime

@pytest.fixture
def mock_db_connection():
    with mock.patch("server.Models.Required_Skills.get_db_connection") as mock_conn:
        yield mock_conn

def test_get_all_skills(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {"skill_name": "Python"},
        {"skill_name": "JS"},
        {"skill_name": "SQL"}
    ]

    skills = Skills.get_all_skills()

    assert len(skills) == 3
    assert skills[0]["skill_name"] == "Python"
    assert skills[1]["skill_name"] == "JS"
    assert skills[2]["skill_name"] == "SQL"

    mock_cursor.execute.assert_called_once_with(
        "SELECT skill_name FROM jobs j JOIN job_skills js on j.id = js.id JOIN skills s on js.skill_id = s.skill_id ORDER BY j.id "
    )

def test_get_skills_id(mock_db_connection):
    mock_cursor = mock.MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    # Arrange: mock the skills data for a specific job ID
    job_id = 1
    mock_cursor.fetchall.return_value = [
        {"id": 1, "job_title": "Software Engineer", "skill_name": "Python"},
        {"id": 1, "job_title": "Software Engineer", "skill_name": "Django"}
    ]
    
    # Act
    skills = Skills.get_skills_id(job_id)
    
    # Assert
    assert len(skills) == 2
    assert skills[0]["job_title"] == "Software Engineer"
    assert skills[0]["skill_name"] == "Python"
    assert skills[1]["skill_name"] == "Django"
    
    # Verify that the correct SQL query was executed
    mock_cursor.execute.assert_called_once_with(
        "SELECT j.id, j.job_title, skill_name FROM jobs j JOIN job_skills js ON j.id = js.id JOIN skills s ON js.skill_id = s.skill_id WHERE j.id = %s", 
        (job_id,)
    )
