import mysql.connector
from config import Config
from datetime import datetime, timedelta


def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    return connection


class Students:

    @staticmethod
    def add_student_details(college_name,full_name,username,email,phone,pincode,city,usn,course,resume):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM college_students WHERE username = %s OR email = %s OR phone = %s OR usn = %s",
            (username, email, phone, usn),
        )
        existing_student = cursor.fetchone()

        if existing_student:
            cursor.close()
            conn.close()
            return {"status": 409, "message": "Username, Email, Phone, or Register Number already exists!"}
        cursor.execute(
            "INSERT INTO college_students (college_name, full_name, username, email, phone, pincode, city, usn, course, resume_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                college_name,
                full_name,
                username,
                email,
                phone,
                pincode,
                city,
                usn,
                course,
                resume
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
    
    from urllib.parse import unquote

    @staticmethod
    def get_students_by_college(college_name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

    # Decode URL-encoded characters (e.g., %20 to space)
        college_name = unquote(college_name)

        cursor.execute("SELECT * FROM college_students WHERE college_name = %s", (college_name,))
        students = cursor.fetchall()
    
        cursor.close()
        conn.close()

    


    

