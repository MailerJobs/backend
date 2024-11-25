import mysql.connector
from config import Config

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )
    return connection

class Jobs:
    
    @staticmethod
    def get_all_jobs():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jobs
    
    @staticmethod
    def get_job_by_id(job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs where job_id = %s", (job_id,))
        job = cursor.fetchone()
        conn.close()

        return job
    
    @staticmethod
    def create_job(job_id, job_title, salary, experience, education, date_posted, job_org, location, image_url,
                    job_description):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO jobs (job_id, job_title, salary, experience, education, date_posted, job_org, location, image_url, job_description) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (job_id, job_title, salary, experience, education, date_posted, job_org, location, image_url, job_description))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_job(job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_views_by_id(job_id, new_view):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE jobs set views = %s WHERE job_id = %s", (new_view, job_id,))
        conn.commit()
        cursor.close()
        conn.close()
