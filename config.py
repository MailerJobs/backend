

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

class Config():
    MYSQL_HOST = 'mailerjobs-rds.c3gksico46df.ap-south-1.rds.amazonaws.com'         # MySQL server host
    MYSQL_DATABASE = 'mailerjobs'  # Your MySQL database name
    MYSQL_USER = 'adminMailerjobs'# MySQL username
    MYSQL_PASSWORD = 'mailerjobs1211'   # MySQL password (change it to your actual password)
    SECRET_KEY = "d9a6d1f1f5dab18e3659868484ccc85a"

class TestingConfig:
    TESTING = True
    MYSQL_HOST = "localhost"
    MYSQL_DATABASE = 'mailerjobs_test'
    MYSQL_USER = 'root'              # MySQL username
    MYSQL_PASSWORD = 'Chandra_121' 

    # C:\Users\visha\OneDrive\Documents\dumps\Dump20241211