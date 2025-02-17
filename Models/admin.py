import mysql.connector
from config import Config
import bcrypt

class AdminModel:
    def __init__(self):
        """Initialize MySQL connection"""
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.create_admin_table()  # Ensure table exists

    def create_admin_table(self):
        """Creates the admin table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def register_admin(self, username, email, password):
        """Registers a new admin with a hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = "INSERT INTO admin (username, email, password) VALUES (%s, %s, %s)"
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (username, email, hashed_password))
                self.conn.commit()
            return {"message": "Admin registered successfully!"}, 201
        except mysql.connector.IntegrityError:
            return {"error": "Username or Email already exists."}, 400
        except mysql.connector.Error as err:
            return {"error": str(err)}, 400

    def get_admin_by_email(self, email):
        """Fetches admin details by email."""
        query = "SELECT * FROM admin WHERE email = %s"
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (email,))
            return cursor.fetchone()

    def verify_password(self, stored_password, provided_password):
        """Verifies hashed password."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
