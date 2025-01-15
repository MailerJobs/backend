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
        cursor.execute("SELECT skill_name FROM skills")
        skills = cursor.fetchall()
        cursor.close()
        return skills

    @staticmethod
    def get_all_skills_by_job():
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
    
    @staticmethod
    def get_or_put_skills(skills_names, job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        skill_ids = []
        print(skills_names)
        for skill_name in skills_names:
            cursor.execute("SELECT skill_id FROM skills WHERE skill_name = %s", (skill_name,))
            result = cursor.fetchall()
            print(result)
            if result:
                skill_ids.append(result[0]["skill_id"])
            else:
                cursor.execute("INSERT INTO skills (skill_name) VALUES (%s)", (skill_name,))
                conn.commit()
                skill_ids.append(cursor.lastrowid)
            print(skill_ids)
        cursor.close()
        print(job_id)
        job_skills_query = "INSERT INTO job_skills (id, skill_id) VALUES(%s,%s)"
        job_skill_data = [(job_id, skill_id) for skill_id in skill_ids]
        cursor = conn.cursor(dictionary=True)
        # for skill_id in skill_ids:
        #     cursor.execute(job_skills_query, (job_id, skill_id))
        cursor.executemany(job_skills_query, job_skill_data)
        conn.commit()
        print("skills added")
        return True

    