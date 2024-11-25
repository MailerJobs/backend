from flask_restful import Resource, reqparse
from Models.Jobs import Jobs
from flask import jsonify, make_response

class JobsListResource(Resource):
    def get(self):
        jobs = Jobs.get_all_jobs()
        if not jobs:
            return {"message": "No jobs found"}, 404
        return jobs, 200
    
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
        parser.add_argument('image_url')
        parser.add_argument('job_description')
        args = parser.parse_args()
        Jobs.create_job(args['job_id'], args['job_title'], args['salary'], args['experience'], args['education'], args['date_posted'], args['job_org'], args['location'], args['image_url'], args['job_description'])
        return make_response(jsonify({"message": "Job Created Successfully!"}), 201)

class JobResource(Resource):

    def get(self, job_id):
        job = Jobs.get_job_by_id(job_id)
        if job:
            return job, 200
        return {"message": "Job Not Found"}, 400

    def delete(self,job_id):
        delete = Jobs.delete_job(job_id)
        if not delete:
            return make_response(jsonify({"message": "Job not found"}), 400)
        return make_response(jsonify({"message": f"Job {job_id} deleted successfully!"}), 200)
    
class JobViewResource(Resource):

    def patch(self, job_id, new_view):
        view = Jobs.update_views_by_id(job_id, new_view)
        if view:
            return make_response(jsonify({"message": "View Not Found"}), 400)
        return make_response(jsonify({"message": f"View {job_id} updated successfully!"}), 200)