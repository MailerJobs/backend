from flask_restful import Resource, reqparse
from Models.Candidate import Candidate
from flask import jsonify, make_response, request
import bcrypt
from tokenManager import generate_token, decode_token, blacklist_token

class CandidateListResource(Resource):

    def get(self):
        candidates = Candidate.get_all_candidate()
        if not candidates:
            return {"message": "No jobs found"}, 404
        return candidates, 200
    
class CandidateRegisterResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('confirm_password')
        parser.add_argument('phone')
        parser.add_argument('pincode')
        args = parser.parse_args()

        existing_user = Candidate.already_registered(args['email'])

        if existing_user:
            return {"message":"Candidate already registered"}, 409
        
        if (args['password'] != args['confirm_password']):
            return {"message":"Password not same"}
        
        Candidate.register_candidate(args['first_name'],args['last_name'],args['username'],args['email'],args['password'],args['phone'],args['pincode'])
        return {"message": "Candidate Registered Successfully"}, 200
    
class CandidateLoginResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()
        email = args['email']
        password = args['password']

        if not email or not password:
            return make_response(jsonify({"message": "Email and password are required"}), 422)
        
        user = Candidate.already_registered(email)

        if user is None:
            return make_response(jsonify({"message":"user not found"}), 400)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = generate_token(user.id)
            # print(current_user)
            print(f"User {email} logged in.")
            response = make_response(jsonify({"message": "Logged in successfully", "token":token}), 200)
            response.set_cookie(
                key='token_user',
                value=token,
                httponly=True,
                secure=True,
                samesite='Strict'
            )
            return response
        print(f"Login failed for {email}.")
        return make_response(jsonify({"message": "Invalid credentials"}), 401)
    
class CandidateLogoutResource(Resource):

    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "Missing Authorization header"}, 401
        
        token = auth_header.split(" ")[1]
        blacklist_token(token)
        response = make_response({"message": "Logged out successfully"})

    # Remove the token by setting it to an empty string and expiration time in the past
        response.set_cookie(
            'token_user', 
            '', 
            expires=0,  # Expire immediately
            httponly=True, 
            secure=True, 
            samesite='Strict'
        )
        return {"message":"Logged out successfully"}, 200

class CandidateProtectedResource(Resource):

    def get(self):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"message": "Missing Authorization header"}, 401
        
        token = auth_header.split(" ")[1]  # Extract the token from "Bearer <token>"
        payload = decode_token(token)

        if "error" in payload:
            return {"message": payload["error"]}, 401
        user_id = payload["user_id"]
        return {"message": f"Welcome, user {user_id}. This is a protected route!"}, 200
