import os

# class ConfigClass:
#     class ProductionConfig:
#         MYSQL_HOST = 'localhost'         # MySQL server host
#         MYSQL_DATABASE = 'mailerjobs'  # Your MySQL database name
#         MYSQL_USER = 'root'              # MySQL username
#         MYSQL_PASSWORD = 'Chandra_121'   # MySQL password (change it to your actual password)
#         SECRET_KEY = "d9a6d1f1f5dab18e3659868484ccc85a"

#     class TestingConfig:
#         TESTING = True
#         MYSQL_HOST = "localhost"
#         MYSQL_DATABASE = 'mailerjobs_test'
#         MYSQL_USER = 'root'              # MySQL username
#         MYSQL_PASSWORD = 'Chandra_121' 

# class Config():
#     MYSQL_HOST = 'mailerjobs-rds.c3gksico46df.ap-south-1.rds.amazonaws.com'         # MySQL server host
#     MYSQL_DATABASE = 'mailerjobs'  # Your MySQL database name
#     MYSQL_USER = 'adminMailerjobs'# MySQL username
#     MYSQL_PASSWORD = 'mailerjobs1211'   # MySQL password (change it to your actual password)
#     SECRET_KEY = "d9a6d1f1f5dab18e3659868484ccc85a"

class Config():

    # MYSQL_HOST = 'localhost'             # MySQL server host
    # MYSQL_DATABASE = 'mailerjobs'        # Your MySQL database name
    # MYSQL_USER = 'root'                  # MySQL username
    # MYSQL_PASSWORD = 'db_pass'       # MySQL password (change it to your actual password)
    MYSQL_HOST = '147.79.68.252'       # MySQL server host
    MYSQL_DATABASE = 'new_mj_db'       # Your MySQL database name
    MYSQL_USER = 'new_mj_user'         # MySQL username
    MYSQL_PASSWORD = 'Nextlearn@123'   # MySQL password (change it to your actual password)
    SECRET_KEY = "d9a6d1f1f5dab18e3659868484ccc85a"
    FRONTEND = os.path.join(os.getcwd(), 'mailerweb')
    PUBLIC_FOLDER = os.path.join(FRONTEND, 'public')
    DEPLOY_UPLOAD = '/var/www/react-app/'
    UPLOAD_FOLDER = os.path.join(DEPLOY_UPLOAD, 'uploads')
    COMPANY_LOGO = os.path.join(UPLOAD_FOLDER, 'company_logo')
    PROFILE_FOLDER = os.path.join(UPLOAD_FOLDER, 'profile_pic')
    RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resume')
    COLLEGE_RESUME_FOLDER = os.path.join(RESUME_FOLDER, 'college')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    ALLOWED_RESUME_EXTENSIONS = {'pdf'}

os.makedirs(Config.COMPANY_LOGO, exist_ok=True)
os.makedirs(Config.PROFILE_FOLDER, exist_ok=True)
os.makedirs(Config.RESUME_FOLDER,exist_ok=True)
os.makedirs(Config.COLLEGE_RESUME_FOLDER,exist_ok=True)

class TestingConfig:
    TESTING = True
    MYSQL_HOST = "localhost"
    MYSQL_DATABASE = 'mailerjobs_test'
    MYSQL_USER = 'root'              # MySQL username
    MYSQL_PASSWORD = 'Chandra_121' 

    # C:\Users\visha\OneDrive\Documents\dumps\Dump20241211

