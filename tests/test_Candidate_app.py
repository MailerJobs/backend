import pytest
from unittest.mock import patch, MagicMock
from server.Models.Candidate import Candidate 
import bcrypt

# Mocking database connection
@pytest.fixture
def mock_db_connection(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('server.Models.Candidate.get_db_connection', return_value=mock_connection)
    return mock_connection, mock_cursor

# Mock bcrypt hashpw to return a predictable value
@pytest.fixture
def mock_bcrypt_hashpw(mocker):
    # mock_hash = b'$2b$12$mockedhashmockedhashmockedhashmockedhashmockedhashmockedhashmockedhash'
    # mocker.patch('bcrypt.hashpw', return_value=mock_hash)
    return mocker.patch("bcrypt.hashpw", return_value=b"fakehashedpassword")

# Test candidate registration with mocked bcrypt
def test_register_candidate(mock_db_connection, mocker, mock_bcrypt_hashpw):
    mock_connection, mock_cursor = mock_db_connection
    # Simulate successful insertion
    mock_cursor.execute.return_value = None
    mock_connection.commit.return_value = None
    
    # Test candidate registration
    email = "johndoe@example.com"
    first_name = "John"
    last_name = "Doe"
    username = "johndoe"
    password = "password123"  # The plain text password to be hashed
    phone = "1234567890"
    pincode = "123456"
    
    # Register the candidate (password will be hashed by the mock)
    Candidate.register_candidate(first_name, last_name, username, email, password, phone, pincode)
    
    # Assert that bcrypt.hashpw was called with the correct parameters
    bcrypt.hashpw.assert_called_once_with(password.encode('utf-8'), mocker.ANY)
    
    # Ensure the SQL query is executed correctly
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO candidate (email,first_name, last_name, username, password, phone_no, pincode) VALUE(%s, %s, %s, %s, %s, %s, %s)",
        (email, first_name, last_name, username, mock_bcrypt_hashpw.return_value, phone, pincode)
    )
    mock_connection.commit.assert_called_once()