from flask_restful import Resource, reqparse
from Models.Client import Client
from flask import jsonify, make_response, request
import bcrypt
from werkzeug.utils import secure_filename
from tokenManager import generate_token, decode_token, blacklist_token
from config import Config
import os
from Models.Jobs import Jobs
from Models.Required_Skills import Skills


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


class ClientListResource(Resource):

    def get(self):
        clients = Client.get_all_client()
        if not clients:
            return {"message": "No Clients found"}, 404
        return clients, 200


class ClientRegisterResource(Resource):

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
        parser.add_argument("company_name")
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
            or not args["company_name"]
        ):
            return {"message": "All fields are required"}, 422

        existing_user = Client.already_registered(args["email"])

        if existing_user:
            return {"message": "Client already registered"}, 409

        if args["password"] != args["confirm_password"]:
            return {"message": "Password not same"}

        Client.register_client(
            args["first_name"],
            args["last_name"],
            args["username"],
            args["email"],
            args["password"],
            args["phone"],
            args["pincode"],
            args["company_name"],
        )
        return {"message": "Client Registered Successfully"}, 200


class ClientLoginResource(Resource):

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

        user = Client.already_registered(email)

        if user is None:
            return make_response(jsonify({"message": "user not found"}), 400)
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            token = generate_token(user["id"])
            # print(current_user)
            print(f"User {email} logged in.")
            response = make_response(
                jsonify(
                    {
                        "message": "Logged in successfully",
                        "token": token,
                        "client_id": user["id"],
                    }
                ),
                200,
            )
            response.set_cookie(
                key="token_client",
                value=token,
                max_age=3600,
                httponly=False,
                secure=True,
                samesite="None",
            )
            print(token)
            return response

        print(f"Login failed for {email}.")
        return make_response(jsonify({"message": "Invalid credentials"}), 401)


class ClientLogoutResource(Resource):

    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "Missing Authorization header"}, 401

        token = auth_header.split(" ")[1]
        blacklist_token(token)
        response = make_response({"message": "Logged out successfully"})

        response.set_cookie(
            "token_client",
            "",
            expires=0,  # Expire immediately
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return {"message": "Logged out successfully"}, 200


class ClientResource(Resource):
    def post(self, id):
        client = Client.get_client_by_id(id)
        if not client:
            return {"message": "No Client Found"}, 404
        return client, 200


class ClientLogoUploadResource(Resource):
    def post(self):
        print("GOT POST REQ")
        file = request.files["file"]
        user_id = request.form.get("client_id")
        print(user_id)

        if not user_id:
            print("CIDIR")
            return {"error": "Client ID is required"}, 400

        if file.filename == "":
            print("NSF")
            return {"error": "No selected file"}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.COMPANY_LOGO, filename)
            file_path = str(file_path)
            file.save(file_path)

            if Client.upload_company_logo(filename, user_id):
                return {
                    "message": "File Uploaded successfully",
                    "file_path": file_path,
                }, 200
            else:
                return {"error": "Invalid file type"}, 400


class ClientJobsResource(Resource):
    def get(self, client_id):
        client_jobs = Client.get_jobs_client(client_id)
        if not client_jobs:
            return {"mesage": "No Jobs There"}, 400
        return client_jobs, 200


class ClientPostJobResource(Resource):
    def post(self):
        print("GOT REQ")
        data = request.get_json()
        parser = reqparse.RequestParser()
        parser.add_argument("job_title")
        parser.add_argument("job_salary")
        parser.add_argument("job_education")
        parser.add_argument("job_org")
        parser.add_argument("job_description")
        parser.add_argument("job_sector")
        parser.add_argument("job_pincode")
        parser.add_argument("job_type")
        parser.add_argument("client_id")
        args = parser.parse_args()
        experiences = data.get("job_exp")
        experience = ", ".join(experiences)
        cities = data.get("city")
        city = ", ".join(cities)
        states = data.get("state")
        state = ", ".join(states)
        image_logo_name = Client.get_logo_name(args["client_id"])
        image = image_logo_name["logo_url"]
        print(image_logo_name["logo_url"])
        image_upload = "uploads"
        image_com_logo = os.path.join(image_upload, "company_logo")
        image_logo = os.path.join(image_com_logo, image)
        job_skill = data.get("job_skill")
        print(image_logo)
        # print(args["job_title"])
        # print(args["job_salary"])
        # print(args["job_exp"])
        # print(args["job_education"])
        # print(args["job_org"])
        # print(args["job_description"])
        # print(args["job_sector"])
        # print(args["city"])
        # print(args["state"])
        # print(args["job_pincode"])
        # print(args["job_type"])
        # print(args["client_id"])
        print(job_skill)
        # print(image_logo['logo_url'])

        post_job_id = Jobs.create_job(
            args["job_title"],
            args["job_salary"],
            experience,
            args["job_education"],
            args["job_org"],
            image_logo,
            args["job_description"],
            args["job_sector"],
            city,
            state,
            args["job_pincode"],
            args["job_type"],
        )
        print(post_job_id)
        process = Skills.get_or_put_skills(job_skill, post_job_id)
        if process:
            return {"message": "Job and Skills added"}, 200
        return {"error": "Not Added"}, 400


class ClientUpdateDetailsResource(Resource):
    def patch(self, client_id):
        print("GOT REQ")
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
        updated = Client.update_client_details(data, client_id)
        if updated:
            print("S")
            return {"message": "success", "data": decoded_token}, 200


class ClientUpdateJobDetailsResource(Resource):
    def patch(self, job_id):
        print("GOT REQ")
        auth_header = request.headers.get("Authorization")
        data = request.get_json()
        skills = data.get("job_skill")
        if not auth_header:
            print("MAH")
            return {"message": "Missing Authorization header"}, 401

        if not data:
            print("NDP")
            return {"error": "No data provided"}, 400

        token = auth_header.split(" ")[1]

        decoded_token = decode_token(token)
        update_job = Client.update_job_details(data, job_id)
        if update_job:
            print("UP JOB DONE")
            if skills:
                add_skill = Skills.get_or_put_skills(skills, job_id)
                if add_skill:
                    print("UPDATE SKILLS DONE")
                    return {"message": "Added Skills and details"}, 200
            return {"message": "success", "data": decoded_token}, 200


class ClientCandidatesByJobsResource(Resource):
    def get(self, job_id):
        candidates = Client.get_candiates_by_job(job_id)
        if candidates:
            return candidates, 200
        return {"error": "No Candidates found"}, 400


class ClientChangePasswordResource(Resource):
    def patch(self, client_id):
        auth_header = request.headers.get("Authorization")
        parser = reqparse.RequestParser()
        parser.add_argument("new_password")
        parser.add_argument("confirm_password")
        args = parser.parse_args()
        new_password = args["new_password"]
        confirm_password = args["confirm_password"]
        print(client_id)
        print(new_password)
        if not auth_header:
            print("MAH")
            return {"message": "Missing Authorization header"}, 401

        token = auth_header.split(" ")[1]

        decoded_token = decode_token(token)

        if new_password != confirm_password:
            return {"message": "password not same"}, 400
        pass_update = Client.change_password(client_id, new_password)
        if pass_update:
            return {
                "message": "password updated succefully",
                "token": decoded_token,
            }, 200


class ClientNameListResource(Resource):
    def get(self):
        client_names = Client.client_name_list()
        if client_names:
            return client_names
        return {"message": "No Clients found"}, 404


class ClientJobsByComapnyNameResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("company_name")
        args = parser.parse_args()
        company_name = args["company_name"]
        jobs = Client.get_jobs_client_by_comapny_name(company_name)
        if jobs:
            return jobs, 200
        return {"message": "No Jobs found"}, 404
