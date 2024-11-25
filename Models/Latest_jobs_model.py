from flask import current_app
import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE']
    )

class latest_jobs:
    @staticmethod
    def get_all_latest_jobs():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM latest_jobs")
        latestJobs = cursor.fetchall()
        conn.close()

        for jobs in latestJobs:
            if isinstance(jobs['date_posted'], datetime):
                jobs['date_posted'] = jobs['date_posted'].isoformat()  # Converts datetime to ISO string
        return latestJobs
    
    @staticmethod
    def create_latest_job(job_id, job_title, salary, experience, education, date_posted, job_org, location):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO latest_jobs (job_id, job_title, salary, experience, education, date_posted, job_org, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (job_id, job_title, salary, experience, education, date_posted, job_org, location))
        conn.commit()
        conn.close()

    @staticmethod
    def update_latest_job(id, job_id, job_title, salary, experience, education, date_posted, job_org, location):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE latest_job SET job_id = %s, job_title = %s, salary = %s, experience = %s, education = %s, date_posted = %s, job_org = %s, location = %s WHERE id = %s",
                       (job_id, job_title, salary, experience, education, date_posted, job_org, location, id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_user(id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM latest_jobs WHERE id = %s", (id,))
        conn.commit()
        conn.close() 
