from flask import Flask,send_from_directory
from flask_restful import Api
from flask_cors import CORS
from config import Config
from flask_mail import Mail, Message
import os
import jwt
print("file : ",jwt.__file__)
from flask_jwt_extended import JWTManager
from flask_compress import Compress

from Resources.student_routes import student_routes
app = Flask(__name__,static_folder='dist',static_url_path='')
Compress(app) 
@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    # Check if the file exists in the dist folder
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Serve the index.html for any unmatched routes
        return send_from_directory(app.static_folder, 'index.html')

app.secret_key = "d9a6d1f1f5dab18e3659868484ccc85a"
app.config["JWT_SECRET_KEY"] = "your_secret_key"
app.config.from_object(Config)
jwt = JWTManager(app)
mail = Mail(app)



CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": [
                "https://mailerjobs.com/",
                "https://api.mailerjobs.com/",
                "http://localhost:5173",
                "http://localhost:5174",
                "http://localhost:4173",
                "https://nextlearn.co.in",
                "https://api.nextlearn.co.in",
            ]   
        }
    },
)

api = Api(app)

from Resources.Latest_Jobs_Resources import LatestListResource, LatestResource
from Resources.Jobs_Resources import (
    JobsListResource,
    JobResource,
    JobFilterResource,
    JobSectorResource,
    JobSearchResource,
    JobSearchBarResource,
    JobViewResource,
)
from Resources.Skills_Resources import (
    SkillsListOfJobResource,
    SkillsResource,
    SkillsListResource,
)
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
    CandidateChangePasswordResource,
    CandidateEmailListResource,
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
    ClientChangePasswordResource,
    ClientNameListResource,
    ClientJobsByComapnyNameResource,
)

from Resources.CollegeResource import (
    CollegesListReosurce,
    CollegeResource,
    CollegeNamesListResource,
)

from Resources.StudentsResource import StudentResource, StudentsByCollegeResource
from Resources.AdminResource import register_admin
from Resources.Maiil import MailResource
from Resources.blogRoutes import blog_bp
from Resources.AdminResource import admin_bp

### Below are the api endpoints
app.register_blueprint(student_routes)
## Jobs, Latest Jobs api endpoints
# Start
api.add_resource(LatestListResource, "/api/latest_jobs")
api.add_resource(LatestResource, "/api/latest_jobs/<int:job_id>")
api.add_resource(JobsListResource, "/api/jobs")
api.add_resource(JobResource, "/api/job/<int:job_id>")
api.add_resource(JobFilterResource, "/api/filterjobs")
api.add_resource(JobSectorResource, "/api/jobsector/<string:sector>")
api.add_resource(JobSearchResource, "/api/searchjobs")
api.add_resource(JobSearchBarResource, "/api/searchbarjobs")
api.add_resource(JobViewResource, "/api/jobview/<int:job_id>")
# End

## Skills api endpoints
# Start
api.add_resource(SkillsListResource, "/api/skills")
api.add_resource(SkillsResource, "/api/skill/<int:id>")
# End
## Candidate api endpoints
# Start
api.add_resource(CandidateListResource, "/api/candidates")
api.add_resource(CandidateRegisterResource, "/api/registercandidate")
api.add_resource(CandidateLoginResource, "/api/login")
api.add_resource(CandidateLogoutResource, "/api/logout")
api.add_resource(CandidateResource, "/api/candidate/<int:id>")
api.add_resource(CandidateProfilePicUploadResource, "/api/upload-profile-pic")
api.add_resource(CandidateResumeUploadResource, "/api/upload-resume")
api.add_resource(
    CandidateResumeDeleteResource, "/api/remove-resume/<string:filename>/<int:id>"
)
api.add_resource(CandidateLikedJobsResource, "/api/job-liked")
api.add_resource(CandidateGetLikedJobsResource, "/api/liked-job/<int:can_id>")
api.add_resource(CandiateUpdateDetailsResource, "/api/update/<int:candidate_id>")
api.add_resource(CandidateApplyJobResource, "/api/apply-job")
api.add_resource(CandiateAppliedJobsResource, "/api/applied-jobs/<int:can_id>")
api.add_resource(
    CandidateChangePasswordResource, "/api/candidate-pass-change/<int:can_id>"
)
api.add_resource(CandidateEmailListResource, "/api/candidate-email-list")
# End

## Client api endpoints
# Start
api.add_resource(ClientListResource, "/api/clients")
api.add_resource(ClientRegisterResource, "/api/registerclient")
api.add_resource(ClientLoginResource, "/api/client-login")
api.add_resource(ClientLogoutResource, "/api/client-logout")
api.add_resource(ClientResource, "/api/client/<int:id>")
api.add_resource(ClientLogoUploadResource, "/api/upload_comapny_logo")
api.add_resource(ClientJobsResource, "/api/client-jobs/<int:client_id>")
api.add_resource(ClientPostJobResource, "/api/post-job")
api.add_resource(ClientUpdateDetailsResource, "/api/client-update/<int:client_id>")
api.add_resource(ClientUpdateJobDetailsResource, "/api/client-update-job/<int:job_id>")
api.add_resource(ClientCandidatesByJobsResource, "/api/client-candidates/<int:job_id>")
api.add_resource(
    ClientChangePasswordResource, "/api/client-pass-change/<int:client_id>"
)
api.add_resource(ClientNameListResource, "/api/client-name-list")
api.add_resource(ClientJobsByComapnyNameResource, "/api/client-jobs-by-name")
# End


## College api endpoints
# Start
api.add_resource(CollegesListReosurce, "/api/colleges")
api.add_resource(CollegeResource, "/api/college/<string:college_name>")
api.add_resource(CollegeNamesListResource, "/api/college-names")

# End

## College_Student api endpoints
# Start
api.add_resource(StudentResource, "/api/student-add")
api.add_resource(
    StudentsByCollegeResource, "/api/student-college/<string:college_name>"
)
# End
  

app.register_blueprint(blog_bp, url_prefix='/api')

app.register_blueprint(admin_bp)  # Now admin routes will be under /api/admin



api.add_resource(MailResource, "/api/sendmail",resource_class_kwargs={'mail': mail})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

