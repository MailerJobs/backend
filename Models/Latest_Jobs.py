import mysql.connector
from flask import current_app
from config import Config



def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )
    return connection

class Latest_Jobs:
    @staticmethod
    def get_all_latest_jobs():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM latest_jobs")
        latest_jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return latest_jobs
    
    @staticmethod
    def create_latest_job(job_id, job_title, salary, experience, education, date_posted, job_org, location):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO latest_jobs (job_id, job_title, salary, experience, education, date_posted, job_org, location) VALUE(%s, %s, %s, %s, %s, %s, %s, %s)",
                       (job_id,job_title,salary,experience,education,date_posted,job_org,location))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def delete_latest_job(job_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM latest_jobs WHERE job_id = %s", (job_id,))
        conn.commit()
        cursor.close()
        conn.close()