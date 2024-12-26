from flask_restful import Api
from conftest import create_app, seed_data


def test_get_all_jobs(client,seed_data):
    response = client.get('/jobs')
    # seed_data()  # Replace with your API endpoint
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) > 0
    assert data[0]['job_title'] == 'Software Engineer'

def test_get_job_by_id(client, seed_data):
    response = client.get('/job/1')  # Replace with your API endpoint for fetching by ID
    assert response.status_code == 200

    job = response.get_json()
    assert job['job_title'] == 'Software Engineer'
    assert job['location'] == 'New York'
