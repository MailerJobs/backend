from flask_restful import Resource, reqparse
import jwt
from Models.Candidate import Candidate
from Models.Jobs import Jobs
from flask import jsonify, make_response, request, send_from_directory
import bcrypt
from werkzeug.utils import secure_filename
from tokenManager import generate_token, decode_token, blacklist_token
from config import Config
import os


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


def allowed_resume_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_RESUME_EXTENSIONS
    )


class CandidateListResource(Resource):

    def get(self):
        candidates = Candidate.get_all_candidate()
        if not candidates:
            return {"message": "No Candidate found"}, 404
        return candidates, 200


class CandidateRegisterResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_name")
        parser.add_argument("last_name")
        parser.add_argument("username")
        parser.add_argument("email")
        parser.add_argument("password")
        parser.add_argument("confirm_password")
        parser.add_argument("phone")
        parser.add_argument("pincode")
        args = parser.parse_args()

        if (
            not args["email"]
            or not args["password"]
            or not args["confirm_password"]
            or not args["first_name"]
            or not args["last_name"]
            or not args["username"]
            or not args["phone"]
            or not args["pincode"]
        ):
            return make_response(jsonify({"message": "All fields are required"}), 422)

        existing_user = Candidate.already_registered(args["email"])

        if existing_user:
            return {"message": "Candidate already registered"}, 409

        if args["password"] != args["confirm_password"]:
            return {"message": "Password not same"}

        Candidate.register_candidate(
            args["first_name"],
            args["last_name"],
            args["username"],
            args["email"],
            args["password"],
            args["phone"],
            args["pincode"],
        )
        return {"message": "Candidate Registered Successfully"}, 200


class CandidateLoginResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("password")
        args = parser.parse_args()
        email = args["email"]
        password = args["password"]

        if not email or not password:
            return make_response(
                jsonify({"message": "Email and password are required"}), 422
            )

        user = Candidate.already_registered(email)

        if user is None:
            return make_response(jsonify({"message": "user not found"}), 400)
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            token = generate_token(user.id)
            # print(current_user)
            print(f"User {email} logged in.")
            response = make_response(
                jsonify(
                    {
                        "message": "Logged in successfully",
                        "token": token,
                        "candidate_id": user.id,
                    }
                ),
                200,
            )
            response.set_cookie(
                key="token_user",
                value=token,
                max_age=3600,
                httponly=False,
                secure=True,
                samesite="None",
            )
            print(response.headers)
            print(token)
            return response
        print(f"Login failed for {email}.")
        return make_response(jsonify({"message": "Invalid credentials"}), 401)


class CandidateLogoutResource(Resource):

    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return make_response(
                jsonify({"message": "Missing Authorization header"}), 401
            )

        token = auth_header.split(" ")[1]
        blacklist_token(token)
        response = make_response(jsonify({"message": "Logged out successfully"}), 200)

        # Remove the token by setting it to an empty string and expiration time in the past
        response.set_cookie(
            "token_user",
            "",
            # expires=0,  # Expire immediately
            max_age=0,
            httponly=False,
            secure=True,
            samesite="None",
        )
        # response.delete_cookie(
        #     "token_user",
        #     httponly=False,
        #     secure=True,
        #     samesite="None"
        # )
        return response


class CandidateResource(Resource):

    def post(self, id):
        # parser = reqparse.RequestParser()
        # parser.add_argument('id')
        # args = parser.parse_args()
        candidates = Candidate.get_candidate_by_id(id)
        if not candidates:
            return jsonify({"message": "No Candidate found"}), 404
        print(candidates)
        return candidates, 200


class CandidateProfilePicUploadResource(Resource):
    def post(self):
        print("GOT POST REQ")
        file = request.files["file"]
        user_id = request.form.get("candidate_id")
        print(user_id)

        if not user_id:
            print("UIDIR")
            return {"error": "User ID is required"}, 400

        if file.filename == "":
            print("NSF")
            return {"error": "No selected file"}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.PROFILE_FOLDER, filename)
            file_path = str(file_path)
            # print(type(file_path))
            print(filename)
            print(file_path)
            file.save(file_path)

            if Candidate.uppload_profile_pic(filename, user_id):
                print("FUS")
                return {
                    "message": "File Uploaded successfully",
                    "file_path": file_path,
                }, 200
            else:
                print("FTUD")
                return {"error": "Failed to update database"}, 500

        else:
            print("IFT")
            return {"error": "Invalid file type"}, 400


class CandidateResumeUploadResource(Resource):
    def post(self):
        file = request.files["file"]
        user_id = request.form.get("candidate_id")

        if not user_id:
            print("UIDIR")
            return {"error": "User ID is required"}, 400

        if file.filename == "":
            print("NSF")
            return {"error": "No selected file"}, 400

        if file and allowed_resume_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.RESUME_FOLDER, filename)
            file_path = str(file_path)
            # print(type(file_path))
            print(filename)
            print(file_path)
            file.save(file_path)

            if Candidate.uplaod_resume(filename, user_id):
                print("FUS")
                return {
                    "message": "File Uploaded successfully",
                    "file_path": file_path,
                }, 200
            else:
                print("FTUD")
                return {"error": "Failed to update database"}, 500

        else:
            print("IFT")
            return {"error": "Invalid file type"}, 400


class CandidateResumeDeleteResource(Resource):
    def delete(self, filename, id):
        print("GOT D")
        file_path = os.path.join(Config.RESUME_FOLDER, filename)
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            Candidate.delete_resume(id)
            return ({"message": "Resume deleted successfully"}), 200
        else:
            return ({"error": "File not found"}), 400


class CandidateLikedJobsResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("can_id")
        parser.add_argument("job_id")
        args = parser.parse_args()

        already_liked = Candidate.verify_candidate_like_job(
            args["can_id"], args["job_id"]
        )
        if already_liked:
            return {"message": "Job Already Liked"}, 409
        
        candidate_job = Candidate.post_candidate_liked_job(
            args["can_id"], args["job_id"]
        )

        if candidate_job:
            return {"message": "Job Liked"}, 200
        return {"error": "Job Not liked"}, 400


class CandidateGetLikedJobsResource(Resource):

    def get(self, can_id):
        candidate_liked_jobs = Candidate.get_candidate_liked_jobs(can_id)
        if candidate_liked_jobs:
            return candidate_liked_jobs
        return {"error": "No Jobs Liked"}, 400


class CandiateUpdateDetailsResource(Resource):
    def patch(self, candidate_id):
        auth_header = request.headers.get("Authorization")
        data = request.get_json()
        if not auth_header:
            print("MAH")
            return {"message": "Missing Authorization header"}, 401

        if not data:
            print("NDP")
            return {"error": "No data provided"}, 400

        token = auth_header.split(" ")[1]

        decoded_token = decode_token(token)
        updated = Candidate.update_candidate_details(data, candidate_id)
        if updated:
            print("S")
            return {"message": "success", "data": decoded_token}, 200


class CandidateApplyJobResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("can_id")
        parser.add_argument("job_id")
        args = parser.parse_args()
        already_applied = Candidate.candidate_already_apply(
            args["can_id"], args["job_id"]
        )
        if already_applied:
            return {"message": "Job Already Applied"}, 409

        applied_job = Candidate.candiate_apply_job(args["can_id"], args["job_id"])
        applies = Jobs.get_applied(args["job_id"])
        applies_count = applies["applied"]
        if applies_count == None:
            applies_count = 0
        applies_count += 1
        applied_count = Jobs.update_applied(args["job_id"], applies_count)
        if applied_job & applied_count:
            return {"message": "Job applied"}, 200
        return {"error": "Job not applied"}, 400


class CandiateAppliedJobsResource(Resource):
    def get(self, can_id):
        candidate_jobs = Candidate.get_candidate_job(can_id)
        if not candidate_jobs:
            return {"error": "No jobs"}, 400
        return candidate_jobs


class CandidateChangePasswordResource(Resource):
    def patch(self, can_id):
        auth_header = request.headers.get("Authorization")
        parser = reqparse.RequestParser()
        parser.add_argument("new_password")
        parser.add_argument("confirm_password")
        args = parser.parse_args()
        new_password = args["new_password"]
        confirm_password = args["confirm_password"]
        print(can_id)
        print(new_password)
        if not auth_header:
            print("MAH")
            return {"message": "Missing Authorization header"}, 401

        token = auth_header.split(" ")[1]

        decoded_token = decode_token(token)

        if new_password != confirm_password:
            return {"message": "password not same"}, 400
        pass_update = Candidate.change_candidate_password(can_id, new_password)
        if pass_update:
            return {
                "message": "password updated succefully",
                "token": decoded_token,
            }, 200


class CandidateEmailListResource(Resource):
    def get(self):
        candidate = Candidate.get_candidates_email()
        if not candidate:
            return {"message": "No Candidate found"}, 404
        return candidate, 200
