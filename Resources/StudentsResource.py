import os
from flask_restful import Resource, reqparse
from Models.students import Students
from flask import  jsonify, make_response, request
from config import Config
from werkzeug.utils import secure_filename
import logging

def allowed_resume_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_RESUME_EXTENSIONS
    )

import logging

class StudentResource(Resource):
    def post(self):
        try:
            logging.info("Received request to add student")
            college_name = request.form.get('college_name')
            full_name = request.form.get('full_name')
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone_no')
            pincode = request.form.get('pincode')
            city = request.form.get('city')
            usn = request.form.get('usn')
            course = request.form.get('course')
            print(request.form)
            logging.info(f"Received data: {request.form}")

            resume = request.files.get('resume')
            if resume and allowed_resume_file(resume.filename):
                filename = secure_filename(resume.filename)
                file_path = os.path.join(Config.COLLEGE_RESUME_FOLDER, filename)
                resume.save(file_path)
                logging.info(f"Resume saved at: {file_path}")

                updated = Students.add_student_details(college_name, full_name, username, email, phone, pincode, city, usn, course, filename)

                if updated:
                    return {"message": "Registration successful!"}, 200
                return {"error": "Error adding student to database"}, 400
            else:
                return {"error": "Invalid file type or no file uploaded"}, 400
        except Exception as e:
            logging.error(f"Error in StudentResource: {str(e)}")
            return {"error": "Internal Server Error"}, 500
            

class StudentsByCollegeResource(Resource):
    def get(self,college_name):
        students = Students.get_students_by_college(college_name)
        if students:
            return students, 200
        return {"error": "Students Not Found"}, 400

class CheckUniqueFieldsResource(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.json
        username = data.get('username')
        email = data.get('email')
        phone_no = data.get('phone_no')
        usn = data.get('usn')

        # Check for conflicts in the database
        conflicts = Students.check_unique_fields(username, email, phone_no, usn)
        
        if conflicts:
            return jsonify({"exists": True, "conflicts": conflicts}), 200
        else:
            return jsonify({"exists": False}), 200