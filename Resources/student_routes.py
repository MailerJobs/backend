from flask import Blueprint, request, jsonify
from Models.student_model import register_student, get_all_students, get_all_students_by_college
import os
from config import Config
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

student_routes = Blueprint("student_routes", __name__)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for student registration
@student_routes.route("/api/jobfair/register", methods=["POST"])
def register():
    """Handles student registration."""
    try:
        # Get all fields from the form data
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
        transaction_id = request.form.get("transaction_id")  # New field

        # Validate required fields
        required_fields = [
            name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume,
            english_proficiency, hindi_proficiency, backlog_status, transaction_id
        ]
        if not all(required_fields):
            return jsonify({"error": "All required fields must be filled"}), 400

        # Validate email format
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email format"}), 400

        # Validate phone number (basic check)
        if not phone.isdigit() or len(phone) != 10:
            return jsonify({"error": "Invalid phone number"}), 400

        # Validate date of birth format
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date of birth format (expected YYYY-MM-DD)"}), 400

        # Create job fair folder if it doesn't exist
        jobfair_folder = os.path.join(Config.RESUME_FOLDER, "JobFair")
        os.makedirs(jobfair_folder, exist_ok=True)

        # Save resume file
        resume_name = resume.filename
        if not resume_name.lower().endswith(".pdf"):
            return jsonify({"error": "Resume must be a PDF file"}), 400

        # Handle duplicate filenames
        if os.path.exists(os.path.join(jobfair_folder, resume_name)):
            resume_name = f"{os.path.splitext(resume_name)[0]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

        resume_path = os.path.join(jobfair_folder, resume_name)
        resume.save(resume_path)

        # Register student and get student ID
        student_id = register_student(
            name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name,
            english_proficiency, hindi_proficiency, backlog_status, transaction_id  # Pass transaction_id
        )

        # Send response
        return jsonify({
            "message": "Registration successful",
            "student_id": student_id,
            "transaction_id": transaction_id  # Include transaction_id in the response
        }), 201

    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


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
                "resume_name": student['resume_name'],
                "english_proficiency": student['english_proficiency'],
                "hindi_proficiency": student['hindi_proficiency'],
                "backlog_status": student['backlog_status'],
                "transaction_id": student['transaction_id']  # Include transaction_id
            } for student in students
        ]
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error fetching job fair data: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500


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
                "resume_name": student["resume_name"],
                "english_proficiency": student["english_proficiency"],
                "hindi_proficiency": student["hindi_proficiency"],
                "backlog_status": student["backlog_status"],
                "transaction_id": student["transaction_id"]  # Include transaction_id
            }
            for student in students
        ]

        return jsonify({"students": filtered_students}), 200
    except Exception as e:
        logger.error(f"Error fetching job fair data: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500