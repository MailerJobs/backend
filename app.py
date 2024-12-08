from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from extension import login_manager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
app.secret_key = "d9a6d1f1f5dab18e3659868484ccc85a"
api = Api(app)
login_manager.init_app(app)

from Resources.Latest_Jobs_Resources import LatestListResource, LatestResource
from Resources.Jobs_Resources import JobsListResource, JobResource, JobFilterResource, JobSectorResource, JobSearchResource, JobSearchBarResource
from Resources.Skills_Resources import SkillsListResource,SkillsResource
from Resources.CandidatesResource import CandidateListResource, CandidateRegisterResource,CandidateLoginResource,CandidateLogoutResource,CandidateProtectedResource

login_manager.login_view = 'candidateloginresource'

@login_manager.unauthorized_handler
def unauthorized():
    return {"message": "Unauthorized access, please log in."}, 401

# Below are the api endpoints
api.add_resource(LatestListResource, '/latest_jobs')
api.add_resource(LatestResource, '/latest_jobs/<int:job_id>')
api.add_resource(JobsListResource, '/jobs')
api.add_resource(JobResource, '/job/<int:job_id>')
api.add_resource(SkillsListResource, '/skills')
api.add_resource(SkillsResource, '/skill/<int:id>')
api.add_resource(JobFilterResource, '/filterjobs')
api.add_resource(JobSectorResource, '/jobsector/<string:sector>')
api.add_resource(JobSearchResource, '/searchjobs')
api.add_resource(JobSearchBarResource, '/searchbarjobs')
api.add_resource(CandidateListResource, '/candidates')
api.add_resource(CandidateRegisterResource  , '/registercandidate')
api.add_resource(CandidateLoginResource, '/login')
api.add_resource(CandidateLogoutResource, '/logout')
api.add_resource(CandidateProtectedResource, '/protected')

if __name__ == '__main__':
    app.run(debug=True)