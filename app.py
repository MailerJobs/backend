from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config

# from server import create_app

app = Flask(__name__)

app.config.from_object(Config)
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "http://localhost:5174"}},
)
app.secret_key = "d9a6d1f1f5dab18e3659868484ccc85a"
api = Api(app)

from Resources.Latest_Jobs_Resources import LatestListResource, LatestResource
from Resources.Jobs_Resources import (
    JobsListResource,
    JobResource,
    JobFilterResource,
    JobSectorResource,
    JobSearchResource,
    JobSearchBarResource,
)
from Resources.Skills_Resources import SkillsListResource, SkillsResource
from Resources.CandidatesResource import (
    CandidateListResource,
    CandidateRegisterResource,
    CandidateLoginResource,
    CandidateLogoutResource,
    CandidateResource,
    CandidateProfilePicUploadResource,
    CandidateResumeUploadResource,
    CandidateResumeDeleteResource,
    CandidateLikedJobsResource,
    CandidateGetLikedJobsResource,
    CandiateUpdateDetailsResource,
    CandidateApplyJobResource,
    CandiateAppliedJobsResource,
    CandidateChangePasswordResource
)
from Resources.ClientResource import (
    ClientListResource,
    ClientRegisterResource,
    ClientLoginResource,
    ClientLogoutResource,
    ClientResource,
    ClientLogoUploadResource,
    ClientJobsResource,
    ClientPostJobResource,
    ClientUpdateDetailsResource,
    ClientUpdateJobDetailsResource,
    ClientCandidatesByJobsResource,
    ClientChangePasswordResource
)

from Resources.CollegeResource import CollegesListReosurce

from Resources.StudentsResource import StudentResource, StudentsByCollegeResource

### Below are the api endpoints

## Jobs, Latest Jobs api endpoints
# Start
api.add_resource(LatestListResource, "/latest_jobs")
api.add_resource(LatestResource, "/latest_jobs/<int:job_id>")
api.add_resource(JobsListResource, "/jobs")
api.add_resource(JobResource, "/job/<int:job_id>")
api.add_resource(JobFilterResource, "/filterjobs")
api.add_resource(JobSectorResource, "/jobsector/<string:sector>")
api.add_resource(JobSearchResource, "/searchjobs")
api.add_resource(JobSearchBarResource, "/searchbarjobs")
# End

## Skills api endpoints
# Start
api.add_resource(SkillsListResource, "/skills")
api.add_resource(SkillsResource, "/skill/<int:id>")
# End

## Candidate api endpoints
# Start
api.add_resource(CandidateListResource, "/candidates")
api.add_resource(CandidateRegisterResource, "/registercandidate")
api.add_resource(CandidateLoginResource, "/login")
api.add_resource(CandidateLogoutResource, "/logout")
api.add_resource(CandidateResource, "/candidate/<int:id>")
api.add_resource(CandidateProfilePicUploadResource, "/upload-profile-pic")
api.add_resource(CandidateResumeUploadResource, "/upload-resume")
api.add_resource(
    CandidateResumeDeleteResource, "/remove-resume/<string:filename>/<int:id>"
)
api.add_resource(CandidateLikedJobsResource, "/job-liked")
api.add_resource(CandidateGetLikedJobsResource, "/liked-job/<int:can_id>")
api.add_resource(CandiateUpdateDetailsResource, "/update/<int:candidate_id>")
api.add_resource(CandidateApplyJobResource, "/apply-job")
api.add_resource(CandiateAppliedJobsResource, "/applied-jobs/<int:can_id>")
api.add_resource(CandidateChangePasswordResource, "/candidate-pass-change/<int:can_id>")
# End
    
## Client api endpoints
# Start
api.add_resource(ClientListResource, "/clients")
api.add_resource(ClientRegisterResource, "/registerclient")
api.add_resource(ClientLoginResource, "/client-login")
api.add_resource(ClientLogoutResource, "/client-logout")
api.add_resource(ClientResource, "/client/<int:id>")
api.add_resource(ClientLogoUploadResource, "/upload_comapny_logo")
api.add_resource(ClientJobsResource, "/client-jobs/<int:client_id>")
api.add_resource(ClientPostJobResource, "/post-job")
api.add_resource(ClientUpdateDetailsResource, "/client-update/<int:client_id>")
api.add_resource(ClientUpdateJobDetailsResource, "/client-update-job/<int:job_id>")
api.add_resource(ClientCandidatesByJobsResource, "/client-candidates/<int:job_id>")
api.add_resource(ClientChangePasswordResource, "/client-pass-change/<int:client_id>")
# End


## College api endpoints
# Start
api.add_resource(CollegesListReosurce, "/colleges")
# End

## College_Student api endpoints
# Start
api.add_resource(StudentResource, "/student-add")
api.add_resource(StudentsByCollegeResource,"/student-college/<string:college_name>")

if __name__ == "__main__":
    app.run(debug=True)
