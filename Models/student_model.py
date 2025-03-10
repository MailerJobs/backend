import uuid
import mysql.connector
from config import Config
import urllib.parse

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    return connection

def register_student(name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
                     english_proficiency, hindi_proficiency, backlog_status):
    """Registers a student and generates a unique ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    student_id = str(uuid.uuid4())[:8]  # Generate a unique 8-character student ID

    query = """
    INSERT INTO students 
    (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
     english_proficiency, hindi_proficiency, backlog_status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
              english_proficiency, hindi_proficiency, backlog_status)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return student_id  # Return the generated Student ID

def get_all_students():
    """Fetches all registered student data."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
           english_proficiency, hindi_proficiency, backlog_status
    FROM students
    """
    cursor.execute(query)
    students = cursor.fetchall()
    conn.close()

    return students

def get_all_students_by_college(college_name):
    """Fetches all registered student data for a specific college."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    decoded_college_name = urllib.parse.unquote(college_name).strip()  # Strip spaces
    print(f"Decoded College Name: '{decoded_college_name}'")
    
    query = """
    SELECT student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
           english_proficiency, hindi_proficiency, backlog_status
    FROM students
    WHERE institution = %s
    """
    
    cursor.execute(query, (decoded_college_name,))
    students = cursor.fetchall()
    
    conn.close()
    return students
