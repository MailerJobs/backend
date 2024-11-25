# resources.py
from flask_restful import Resource, reqparse
from models import User, Jobs

class UserListResource(Resource):
    def get(self):
        users = User.get_all_users()
        return {'users': users}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('email', required=True, help="Email is required")
        parser.add_argument('password', required=True, help="Password is required")
        args = parser.parse_args()

        # Create a new user
        User.create_user(args['username'], args['email'], args['password'])
        return {'message': 'User created successfully'}, 201

class UserResource(Resource):
    def get(self, id):
        user = User.get_user_by_id(id)
        if user:
            return {'user': user}, 200
        return {'message': 'User not found'}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('email', required=True, help="Email is required")
        parser.add_argument('password', required=True, help="Password is required")
        args = parser.parse_args()

        user = User.get_user_by_id(id)
        if user:
            # Update user information
            User.update_user(id, args['username'], args['email'], args['password'])
            return {'message': 'User updated successfully'}, 200
        return {'message': 'User not found'}, 404

    def delete(self, id):
        user = User.get_user_by_id(id)
        if user:
            # Delete the user
            User.delete_user(id)
            return {'message': 'User deleted successfully'}, 200
        return {'message': 'User not found'}, 404
    





class JobsListResource(Resource):
    def get(self):
        jobs = Jobs.get_all_jobs()
        return {'jobs': jobs}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job_name', required=True, help="Job Name is required")
        parser.add_argument('org_name', required=True, help="Org Name is required")
        parser.add_argument('location', required=True, help="Location is required")
        parser.add_argument('salary_range', required=True, help="Salary Range is required")
        args = parser.parse_args()

        # Create a new user
        Jobs.create_job(args['job_name'], args['org_name'], args['location'], args['salary_range'])
        return {'message': 'Job Posted successfully'}, 201
    
class JobResource(Resource):
    def get(self, id):
        job = Jobs.get_job_by_id(id)
        if job:
            return {'job': job}, 200
        return {'message': 'User not found'}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('job_name', required=True, help="Job Name is required")
        parser.add_argument('org_name', required=True, help="Org Name is required")
        parser.add_argument('location', required=True, help="Location is required")
        parser.add_argument('salary_range', required=True, help="Salary Range is required")
        args = parser.parse_args()

        job = Jobs.get_job_by_id(id)
        if job:
            # Update user information
            Jobs.update_job(id, args['job_name'], args['org_name'], args['location'], args['salary_range'])
            return {'message': 'Job updated successfully'}, 200
        return {'message': 'Job not found'}, 404

    def delete(self, id):
        job = Jobs.get_user_by_id(id)
        if job:
            # Delete the user
            Jobs.delete_job(id)
            return {'message': 'Job deleted successfully'}, 200
        return {'message': 'Job not found'}, 404