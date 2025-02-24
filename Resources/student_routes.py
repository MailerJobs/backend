from flask import Blueprint, request, jsonify
from Models.student_model import register_student
import os
from config import Config;

student_routes = Blueprint("student_routes", __name__)

UPLOAD_FOLDER = "uploads/"  # Folder to store resumes
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@student_routes.route("/api/jobfair/register", methods=["POST"])
def register():
    """Handles student registration."""
    try:
        name = request.form.get("name")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        email = request.form.get("email")
        institution = request.form.get("institution")
        degree = request.form.get("degree")
        graduation_year = request.form.get("graduation_year")
        reg_no = request.form.get("reg_no")
        resume = request.files.get("resume")

        if not all([name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume]):
            return jsonify({"error": "All required fields must be filled"}), 400
       
       # Create the JobFair directory inside the RESUME_FOLDER
        jobfair_folder = os.path.join(Config.RESUME_FOLDER, "JobFair")
        os.makedirs(jobfair_folder, exist_ok=True)

        # Save resume file
        resume_path = os.path.join(jobfair_folder, resume.filename)
        resume.save(resume_path)

        # Register student and get student ID
        student_id = register_student(name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_path)

        # Send response
        return jsonify({"message": "Registration successful", "student_id": student_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
