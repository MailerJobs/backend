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

class Skills:

    @staticmethod
    def get_all_skills():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT skill_name FROM jobs j JOIN job_skills js on j.id = js.id JOIN skills s on js.skill_id = s.skill_id ORDER BY j.id ")
        skills = cursor.fetchall()
        cursor.close()
        return skills
    
    @staticmethod 
    def get_skills_id(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT j.id, j.job_title, skill_name FROM jobs j JOIN job_skills js ON j.id = js.id JOIN skills s ON js.skill_id = s.skill_id WHERE j.id = %s", (id,))
        skill = cursor.fetchall()
        conn.close()
        return skill
    