from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Models.blog import BlogModel

blog_bp = Blueprint("blog_bp", __name__)

blog_model = BlogModel()
blog_model.create_blog_table()  # Ensure the table exists

@blog_bp.route("/blogs", methods=["GET"])
def get_all_blogs():
    """Fetch all blog posts."""
    blogs = blog_model.get_all_blogs()
    return jsonify(blogs), 200

@blog_bp.route("/blogs/<int:blog_id>", methods=["GET"])
def get_blog(blog_id):
    """Fetch a single blog post by ID."""
    blog = blog_model.get_blog_by_id(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), 404
    return jsonify(blog), 200

@blog_bp.route("/blogs", methods=["POST"])
@jwt_required()  # Only logged-in admins can create blogs
def create_blog():
    """Create a new blog post."""
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    author = data.get("author")

    if not title or not content or not author:
        return jsonify({"error": "Title, content, and author are required"}), 400

    return blog_model.add_blog(title, content, author)

@blog_bp.route("/blogs/<int:blog_id>", methods=["PUT"])
@jwt_required()  # Only admins can update blogs
def update_blog(blog_id):
    """Update an existing blog post."""
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    return blog_model.update_blog(blog_id, title, content)

@blog_bp.route("/blogs/<int:blog_id>", methods=["DELETE"])
@jwt_required()  # Only admins can delete blogs
def delete_blog(blog_id):
    """Delete a blog post."""
    return blog_model.delete_blog(blog_id)
