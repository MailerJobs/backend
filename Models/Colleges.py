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

class Colleges:

    @staticmethod
    def get_all_colleges():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM colleges")
        colleges = cursor.fetchall()
        cursor.close()
        conn.close()
        return colleges
    
    @staticmethod
    def get_college_by_name(college_name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM colleges WHERE name = %s", (college_name,))
        college = cursor.fetchone()
        cursor.close()
        conn.close()
        return college
    
    @staticmethod
    def get_college_names():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name FROM colleges")
        colleges = cursor.fetchall()
        cursor.close()
        conn.close()
        return colleges