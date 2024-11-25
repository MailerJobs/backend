# from flask_mysql import MySQL
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

class User:
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        
        for user in users:
            if isinstance(user['createdTime'], datetime):
                user['createdTime'] = user['createdTime'].isoformat()  # Converts datetime to ISO string
        return users

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user and isinstance(user['createdTime'], datetime):
            user['createdTime'] = user['createdTime'].isoformat()  # Converts datetime to ISO string

        return user

    @staticmethod
    def create_user(username, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()
        conn.close()

    @staticmethod
    def update_user(user_id, username, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s",
                       (username, email, password, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        conn.close()



class Jobs:
    @staticmethod
    def get_all_jobs():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        conn.close()
        
        for user in jobs:
            if isinstance(user['dateposted'], datetime):
                user['dateposted'] = user['dateposted'].isoformat()  # Converts datetime to ISO string
        return jobs
    
    @staticmethod
    def get_job_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs WHERE id = %s", (user_id,))
        job = cursor.fetchone()
        conn.close()
        
        if job and isinstance(job['dateposted'], datetime):
            job['dateposted'] = job['dateposted'].isoformat()  # Converts datetime to ISO string

        return job
    
    @staticmethod
    def create_job(jobName, orgName, location, salaryRange):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (job_name, org_name, location, salary_range) VALUES (%s, %s, %s, %s)",
                       (jobName, orgName, location, salaryRange))
        conn.commit()
        conn.close()

    @staticmethod
    def update_job(job_id, jobName, orgName, location, salaryRange):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET job_name = %s, org_name = %s, location = %s, salary_range = %s WHERE id = %s",
                       (jobName, orgName, location, salaryRange, job_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_job(job_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
        conn.commit()
        conn.close()