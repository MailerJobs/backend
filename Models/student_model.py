import uuid
import mysql.connector
from config import Config

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    return connection

def register_student(name, dob, gender, phone, email, institution, degree, graduation_year, gpa, resume_path):
    """Registers a student and generates a unique ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    student_id = str(uuid.uuid4())[:8]  # Generate a unique 8-character student ID

    query = """
    INSERT INTO students 
    (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, gpa, resume_path) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, gpa, resume_path)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return student_id  # Return the generated Student ID
