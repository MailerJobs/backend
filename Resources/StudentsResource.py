import os
from flask_restful import Resource, reqparse
from Models.students import Students
from flask import  jsonify, make_response, request
from config import Config
from werkzeug.utils import secure_filename


def allowed_resume_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_RESUME_EXTENSIONS
    )

class StudentResource(Resource):
    def post(self):
        print("GOT REQ")
        college_name = request.form['college_name']
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone_no']
        pincode = request.form['pincode']
        city = request.form['city']
        usn = request.form['usn']
        course = request.form['course']

        resume = request.files['resume']
        print(resume)
        if resume and allowed_resume_file(resume.filename):
            filename = secure_filename(resume.filename)
            file_path = os.path.join(Config.COLLEGE_RESUME_FOLDER, filename)
            resume.save(file_path)
            updated = Students.add_student_details(college_name,full_name,username,email,phone,pincode,city,usn,course,filename)

            if updated:
                return {"message": "Registration successful!"}, 200
            return {"error": "Error"}, 400
            

class StudentsByCollegeResource(Resource):
    def get(self,college_name):
        students = Students.get_students_by_college(college_name)
        if students:
            return students, 200
        return {"error": "Students Not Found"}, 400
