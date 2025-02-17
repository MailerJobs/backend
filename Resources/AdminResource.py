from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from Models.admin import AdminModel  # Ensure the correct import

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")

admin_model = AdminModel()

@admin_bp.route("/register", methods=["POST"])
def register_admin():
    """Registers a new admin."""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if admin already exists
    existing_admin = admin_model.get_admin_by_email(email)
    if existing_admin:
        return jsonify({"error": "Admin already exists"}), 400

    return admin_model.register_admin(username, email, password)

@admin_bp.route("/login", methods=["POST"])
def login_admin():
    """Authenticates admin and returns JWT token."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    admin = admin_model.get_admin_by_email(email)
    if not admin or not admin_model.verify_password(admin["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(admin["id"]))  # Convert to string

    return jsonify({"message": "Login successful", "token": access_token}), 200
