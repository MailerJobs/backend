import mysql.connector
from config import Config

class BlogModel:
    def __init__(self):
        """Initialize MySQL connection"""
        self.conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def create_blog_table(self):
        """Creates the blog table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS blogs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            author VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_blog(self, title, content, author):
        """Adds a new blog post."""
        query = "INSERT INTO blogs (title, content, author) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(query, (title, content, author))
            self.conn.commit()
            return {"message": "Blog added successfully!"}, 201
        except mysql.connector.Error as err:
            return {"error": str(err)}, 400

    def get_all_blogs(self):
        """Fetch all blogs."""
        self.cursor.execute("SELECT * FROM blogs ORDER BY created_at DESC")
        return self.cursor.fetchall()

    def get_blog_by_id(self, blog_id):
        """Fetch a single blog by ID."""
        query = "SELECT * FROM blogs WHERE id = %s"
        self.cursor.execute(query, (blog_id,))
        return self.cursor.fetchone()

    def update_blog(self, blog_id, title, content):
        """Update an existing blog post."""
        query = "UPDATE blogs SET title = %s, content = %s WHERE id = %s"
        self.cursor.execute(query, (title, content, blog_id))
        self.conn.commit()

        if self.cursor.rowcount == 0:
            return {"error": "Blog not found"}, 404
        return {"message": "Blog updated successfully!"}, 200

    def delete_blog(self, blog_id):
        """Delete a blog post."""
        query = "DELETE FROM blogs WHERE id = %s"
        self.cursor.execute(query, (blog_id,))
        self.conn.commit()

        if self.cursor.rowcount == 0:
            return {"error": "Blog not found"}, 404
        return {"message": "Blog deleted successfully!"}, 200
