from flask import Flask
from flask_restful import Api, Resource
from Resources.Latest_Jobs_Resources import LatestListResource, LatestResource
from flask_cors import CORS
from Resources.Jobs_Resources import JobsListResource, JobResource, JobViewResource

app = Flask(__name__)
CORS(app)
api = Api(app)



api.add_resource(LatestListResource, '/latest_jobs')
api.add_resource(LatestResource, '/latest_jobs/<int:job_id>')
api.add_resource(JobsListResource, '/jobs')
api.add_resource(JobResource, '/job/<int:job_id>')
api.add_resource(JobViewResource, '/view/<int:job_id>/<int:new_view>')


if __name__ == '__main__':
    app.run(debug=True)