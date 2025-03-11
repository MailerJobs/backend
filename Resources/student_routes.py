from flask import Blueprint, request, jsonify
from Models.student_model import register_student, get_all_students, get_all_students_by_college
import os
from config import Config

student_routes = Blueprint("student_routes", __name__)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for student registration
@student_routes.route("/api/jobfair/register", methods=["POST"])
def register():
    """Handles student registration."""
    try:
        # Get new fields from the form data
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
        english_proficiency = request.form.get("english_proficiency")
        hindi_proficiency = request.form.get("hindi_proficiency")
        backlog_status = request.form.get("backlog_status")
        transaction_id = request.form.get("transaction_id")  # User-provided transaction ID

        if not all([name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume, english_proficiency, hindi_proficiency, backlog_status, transaction_id]):
            return jsonify({"error": "All required fields must be filled"}), 400

        jobfair_folder = os.path.join(Config.RESUME_FOLDER, "JobFair")
        os.makedirs(jobfair_folder, exist_ok=True)

        # Save resume file
        resume_name = f"{transaction_id}_{resume.filename}"  # Ensuring unique file names
        resume_path = os.path.join(jobfair_folder, resume_name)
        resume.save(resume_path)

        # Register student and get student ID
        student_id = register_student(
            name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name,
            english_proficiency, hindi_proficiency, backlog_status, transaction_id
        )

        # Send response
        return jsonify({"message": "Registration successful", "student_id": student_id, "transaction_id": transaction_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to fetch all registered student data
@student_routes.route("/api/jobfair/data", methods=["GET"])
def get_job_fair_data():
    """Fetches all registered student data."""
    try:
        students = get_all_students()
        result = [
            {
                "student_id": student['student_id'],
                "name": student['name'],
                "dob": student['dob'],
                "gender": student['gender'],
                "phone": student['phone'],
                "email": student['email'],
                "institution": student['institution'],
                "degree": student['degree'],
                "graduation_year": student['graduation_year'],
                "reg_no": student['reg_no'],
                "resume_url": student['resume_name'],
                "english_proficiency": student['english_proficiency'],
                "hindi_proficiency": student['hindi_proficiency'],
                "backlog_status": student['backlog_status'],
                "transaction_id": student['transaction_id']
            } for student in students
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to fetch student data by college name
@student_routes.route("/api/jobfair/<string:college_name>", methods=["GET"])
def get_job_fair_data_by_college_name(college_name):
    try:
        # Fetch student data by college name
        students = get_all_students_by_college(college_name.strip())

        # Prepare the response
        filtered_students = [
            {
                "student_id": student["student_id"],
                "name": student["name"],
                "dob": student["dob"],
                "gender": student["gender"],
                "phone": student["phone"],
                "email": student["email"],
                "institution": student["institution"],
                "degree": student["degree"],
                "graduation_year": student["graduation_year"],
                "reg_no": student["reg_no"],
                "resume_url": student["resume_name"],
                "english_proficiency": student["english_proficiency"],
                "hindi_proficiency": student["hindi_proficiency"],
                "backlog_status": student["backlog_status"],
                "transaction_id": student["transaction_id"]
            }
            for student in students
        ]
        
        return jsonify({"students": filtered_students}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
