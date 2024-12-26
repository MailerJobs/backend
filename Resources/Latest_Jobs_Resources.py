from flask_restful import Resource, reqparse
from server.Models.Latest_Jobs import Latest_Jobs
from flask import jsonify, make_response

class LatestListResource(Resource):
    def get(self):
        latest_jobs = Latest_Jobs.get_all_latest_jobs()
        if not latest_jobs:
            return {"message":"No jobs found"}, 404
        return latest_jobs, 200 
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job_id')
        parser.add_argument('job_title')
        parser.add_argument('salary')
        parser.add_argument('experience')
        parser.add_argument('education')
        parser.add_argument('date_posted')
        parser.add_argument('job_org')
        parser.add_argument('location')
        args = parser.parse_args()
        Latest_Jobs.create_latest_job(args['job_id'], args['job_title'], args['salary'], args['experience'], args['education'], args['date_posted'], args['job_org'], args['location'])
        return make_response(jsonify({"message": "Job created successfully!"}), 201)
    
class LatestResource(Resource):
    def delete(self, job_id):
        delete = Latest_Jobs.delete_latest_job(job_id)
        if not delete:
            return make_response(jsonify({"message": "Job not found"}), 404)
        return make_response(jsonify({"message": f"Job {job_id} deleted successfully!"}), 200)
