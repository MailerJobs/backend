from flask import Blueprint, request, jsonify
from Models.student_model import register_student
from Models.student_model import get_all_students
from Models.student_model import get_all_students_by_college
import os
from config import Config;
import urllib.parse


student_routes = Blueprint("student_routes", __name__)

UPLOAD_FOLDER = "uploads/"
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

        jobfair_folder = os.path.join(Config.RESUME_FOLDER, "JobFair")
        os.makedirs(jobfair_folder, exist_ok=True)

        # Save resume file
        resume_name = resume.filename
        resume_path = os.path.join(jobfair_folder, resume_name)
        resume.save(resume_path)

        # Register student and get student ID
        student_id = register_student(
            name, dob, gender, phone, email, institution, degree, graduation_year, reg_no, resume_name
        )

        # Send response
        return jsonify({"message": "Registration successful", "student_id": student_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@student_routes.route("/api/jobfair/data", methods=["GET"])
def get_job_fair_data():
    """Fetches all registered student data."""
    try:
        students = get_all_students()
        print(students)
        print()  # Debug: print the fetched data
        result = [
            {
                "name": student['name'],
                "dob": student['dob'],
                "gender": student['gender'],
                "phone": student['phone'],
                "email": student['email'],
                "institution": student['institution'],
                "degree": student['degree'],
                "graduation_year": student['graduation_year'],
                "reg_no": student['reg_no'],
                "resume_url": student['resume_name']
            } for student in students
        ]
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching job fair data: {e}")
        return jsonify({"error": str(e)}), 500
    


@app.route("/api/jobfair/<string:college_name>", methods=["GET"])
def get_job_fair_data_by_college_name(college_name):
    try:
        # Fetch student data by college name
        students = get_all_students_by_college(college_name.strip())
        print(f"Fetched {len(students)} students.")

        # Prepare the response
        filtered_students = [  
            {
                "name": student["name"],
                "dob": student["dob"],
                "gender": student["gender"],
                "phone": student["phone"],
                "email": student["email"],
                "institution": student["institution"],
                "degree": student["degree"],
                "graduation_year": student["graduation_year"],
                "reg_no": student["reg_no"],
                "resume_url": student["resume_name"]
            }
            for student in students
        ]
        
        return jsonify({"students": filtered_students}), 200
    except Exception as e:
        print(f"Error fetching job fair data: {e}")
        return jsonify({"error": str(e)}), 500

