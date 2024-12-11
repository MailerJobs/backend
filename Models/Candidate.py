import mysql.connector
from config import Config
from datetime import datetime, timedelta
import bcrypt


def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )
    return connection

class Candidate():

    def __init__(self, id, username, password, is_active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = is_active

    @property
    def is_active(self):
        return self.active
    
    @staticmethod
    def get_all_candidate():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM candidate")
        candidates = cursor.fetchall()
        for row in candidates:
            if 'created_date' in row and isinstance(row['created_date'], datetime):
                row['created_date'] = row['created_date'].strftime('%Y-%m-%d %H:%M:%S')
        cursor.close()
        cursor.close()
        conn.close()
        return candidates
    
    @staticmethod
    def already_registered(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM candidate WHERE email = %s", (email,))
        existing_candidate = cursor.fetchone()
        cursor.close()
        conn.close()

        if existing_candidate:
            return Candidate(existing_candidate['id'], existing_candidate['username'], existing_candidate['password'])
        return None
        
    @staticmethod
    def register_candidate(first_name,last_name,username,email,password,phone,pincode):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO candidate (email,first_name, last_name, username, password, phone_no, pincode) VALUE(%s, %s, %s, %s, %s, %s, %s)",
                       (email, first_name, last_name, username, hash_password, phone, pincode))
        conn.commit()
        cursor.close()
        conn.close()
