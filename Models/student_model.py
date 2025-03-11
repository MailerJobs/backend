import uuid
import mysql.connector
from config import Config
import urllib.parse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
        )
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to the database: {err}")
        raise

def register_student(name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
                     english_proficiency, hindi_proficiency, backlog_status, transaction_id):
    """Registers a student and generates a unique ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        student_id = str(uuid.uuid4())[:8]  # Generate a unique 8-character student ID

        query = """
        INSERT INTO students 
        (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
         english_proficiency, hindi_proficiency, backlog_status, transaction_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
                  english_proficiency, hindi_proficiency, backlog_status, transaction_id)

        cursor.execute(query, values)
        conn.commit()
        return student_id  # Return the generated Student ID

    except mysql.connector.Error as err:
        logger.error(f"Error registering student: {err}")
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_students():
    """Fetches all registered student data."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
               english_proficiency, hindi_proficiency, backlog_status, transaction_id
        FROM students
        """
        cursor.execute(query)
        students = cursor.fetchall()
        return students

    except mysql.connector.Error as err:
        logger.error(f"Error fetching all students: {err}")
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_students_by_college(college_name):
    """Fetches all registered student data for a specific college."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        decoded_college_name = urllib.parse.unquote(college_name).strip()  # Strip spaces
        logger.info(f"Decoded College Name: '{decoded_college_name}'")

        query = """
        SELECT student_id, name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name, 
               english_proficiency, hindi_proficiency, backlog_status, transaction_id
        FROM students
        WHERE institution = %s
        """
        cursor.execute(query, (decoded_college_name,))
        students = cursor.fetchall()
        return students

    except mysql.connector.Error as err:
        logger.error(f"Error fetching students by college: {err}")
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()