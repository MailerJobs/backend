from flask import Flask
import pytest
from config import TestingConfig
import mysql.connector
from flask_restful import Api
# from Resources.Jobs_Resources from JobsListResource
from Resources.Jobs_Resources import JobsListResource, JobResource


def get_db_test_connection():
    connection = mysql.connector.connect(
        host=TestingConfig.MYSQL_HOST,
        user=TestingConfig.MYSQL_USER,
        password=TestingConfig.MYSQL_PASSWORD,
        database=TestingConfig.MYSQL_DATABASE
    )
    return connection

def create_app(testing = True):
    app = Flask(__name__)
    if testing:
        app.config.from_object(TestingConfig)
    api = Api(app)
    api.add_resource(JobsListResource, '/jobs')
    api.add_resource(JobResource, '/job/<int:job_id>')
    return app

app_test = create_app()

@pytest.fixture
def app():
    app_test = create_app()
    with app_test.app_context():
        conn = get_db_test_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS jobs (id INT AUTO_INCREMENT PRIMARY KEY, job_title VARCHAR(255), salary FLOAT, experience VARCHAR(50), education VARCHAR(100), date_posted DATETIME, job_org VARCHAR(255), location VARCHAR(255), image_url TEXT, job_description TEXT, sector VARCHAR(255), city VARCHAR(255))")
        conn.commit()
        yield app_test
        # cursor.execute("INSERT INTO jobs (job_title, salary, experience, education, date_posted, job_org, location, image_url, job_description, sector, city) VALUES ('Software Engineer', 120000, '3 years', 'Graduate', NOW(), 'Tech Corp', 'New York', 'https://example.com/image.jpg', 'Develop software.', 'IT', 'New York')")
        conn.commit()
        conn.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seed_data():
    conn = get_db_test_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (job_title, salary, experience, education, date_posted, job_org, location, image_url, job_description, sector, city) VALUES ('Software Engineer', 120000, '3 years', 'Graduate', NOW(), 'Tech Corp', 'New York', 'https://example.com/image.jpg', 'Develop software.', 'IT', 'New York')")
    conn.commit()
    yield
    # cursor.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()