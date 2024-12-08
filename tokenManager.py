from config import Config
import jwt
from datetime import datetime, timedelta

import mysql

SECRET_KEY = "d9a6d1f1f5dab18e3659868484ccc85a"

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )
    return connection

def generate_token(user_id):
    """Generate a JWT token for a user."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    if is_token_blacklisted(token):
        return {"error": "Token has been invalidated"}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
def blacklist_token(token):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO blacklisted_tokens (token) VALUES (%s)", (token,))
    connection.commit()
    connection.close()
    
def is_token_blacklisted(token):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blacklisted_tokens WHERE token = %s", (token,))
    blacklisted = cursor.fetchone()
    connection.close()
    return blacklisted is not None