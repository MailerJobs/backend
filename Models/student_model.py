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

def register_student(name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name):
    """Registers a student and generates a unique ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    student_id = str(uuid.uuid4())[:8]  # Generate a unique 8-character student ID

    query = """
    INSERT INTO students 
    (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return student_id # Return the generated Student ID

def get_all_students():
    """Fetches all registered student data."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name
    FROM students
    """
    cursor.execute(query)
    students = cursor.fetchall()
    conn.close()

    return students

def get_all_students_by_college(college_name, id=0):
    """Fetches all registered student data for a specific college and student_id is greater than id."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    decoded_college_name = urllib.parse.unquote(college_name).strip()  # Strip spaces
    print(f"Decoded College Name: '{decoded_college_name}'")
    print(f"Student ID: {id}")
    
    # Debug query without student_id condition
    query = """
    SELECT student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name
    FROM students
    WHERE institution = %s AND student_id > %s
    """
    
    cursor.execute(query, (decoded_college_name, id))
    students = cursor.fetchall()
    
    print(f"Fetched {len(students)} students.")  # Debug line
    
    conn.close()
    return students

    
