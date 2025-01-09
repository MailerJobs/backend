import mysql.connector
from config import Config
from datetime import datetime
import bcrypt


def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    return connection


class Client:
    @staticmethod
    def get_all_client():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM client")
        clients = cursor.fetchall()
        for row in clients:
            if "created_date" in row and isinstance(row["created_date"], datetime):
                row["created_date"] = row["created_date"].strftime("%Y-%m-%d %H:%M:%S")
        cursor.close()
        conn.close()
        return clients

    @staticmethod
    def already_registered(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM client WHERE email = %s", (email,))
        existing_candidate = cursor.fetchone()
        cursor.close()
        conn.close()

        if existing_candidate:
            return existing_candidate
        return None

    @staticmethod
    def register_client(
        first_name, last_name, username, email, password, phone, pincode, company_name
    ):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO client (first_name, last_name, username, email, password, phone_no, pincode, company_name) VALUE(%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                first_name,
                last_name,
                username,
                email,
                hash_password,
                phone,
                pincode,
                company_name,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_client_by_id(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id,first_name,last_name,email,company_name,company_url,about,state,city,pincode,facebook,twitter,linkedin,logo_url,sector from client WHERE id = %s",
            (id,),
        )
        client = cursor.fetchone()
        cursor.close()
        conn.close
        return client

    @staticmethod
    def upload_company_logo(logo_url, id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE client SET logo_url = %s WHERE id = %s", (logo_url, id))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_jobs_client(client_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT j.id AS job_id, j.job_title AS job_title,j.Posted_Date AS job_date , j.sector AS job_sector, j.status AS job_status, j.applied AS job_applied FROM jobs j JOIN client c ON j.job_org = c.company_name WHERE c.id = %s",
            (client_id,),
        )
        client_jobs = cursor.fetchall()
        for row in client_jobs:
            if 'job_date' in row and isinstance(row['job_date'], datetime):
                row['job_date'] = row['job_date'].strftime('%d-%m-%Y')
        cursor.close()
        conn.close()
        return client_jobs
    
    @staticmethod
    def get_logo_name(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT logo_url FROM client where id = %s", (id,))
        image_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return image_name
    
    @staticmethod
    def update_client_details(data, client_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "UPDATE client SET "
        params = []
        # print(data["linkedin"])

        if data:
            if data["first_name"] != "":
                query += " first_name = %s,"
                params.append(data["first_name"])

            if data["last_name"] != "":
                query += " last_name = %s,"
                params.append(data["last_name"])

            if data["email"] != "":
                query += " email = %s,"
                params.append(data["email"])

            if data["phone_no"] != "":
                query += " phone_no = %s,"
                params.append(data["phone_no"])

            if data["pincode"] != "":
                query += " pincode = %s,"
                params.append(data["pincode"])

            if data["sector"] != "":
                query += " sector = %s,"
                params.append(data["sector"])

            if data["company_name"] != "":
                query += " company_name = %s,"
                params.append(data["company_name"])

            if data["company_url"] != "":
                query += " company_url = %s,"
                params.append(data["company_url"])

            if data["linkedin"] != "":
                query += " linkedin = %s,"
                params.append(data["linkedin"])

            if data["facebook"] != "":
                query += " facebook = %s,"
                params.append(data["facebook"])

            if data["twitter"] != "":
                query += " twitter = %s,"
                params.append(data["twitter"])

            if data["state"] != "":
                query += " state = %s,"
                params.append(data["state"])

            if data["city"] != "":
                query += " city = %s,"
                params.append(data["city"])

            query += " id = %s WHERE id = %s"
            params.append(client_id)
            params.append(client_id)

        print("Query = ", query)
        print("Params =", params)
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    
    @staticmethod
    def update_job_details(data, job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "UPDATE jobs SET"
        params = []

        if data:
            if data["job_title"] != "":
                query += " job_title = %s,"
                params.append(data["job_title"])
            
            if data["job_description"] != "":
                query += " job_description = %s,"
                params.append(data["job_description"])

            if data["job_sector"] != "":
                query += " sector = %s,"
                params.append(data["job_sector"])

            if data["job_type"] != "":
                query += " job_type = %s,"
                params.append(data["job_type"])

            if data["job_exp"] != "":
                query += " experience = %s,"
                params.append(data["job_exp"])
            
            if data["job_salary"] != "":
                query += " salary = %s,"
                params.append(data["job_salary"])

            if data["job_education"] != "":
                query += " education = %s,"
                params.append(data["job_education"])

            if data["city"] != "":
                query += " city = %s,"
                params.append(data["city"])

            if data["state"] != "":
                query += " state = %s,"
                params.append(data["state"])

            if data["job_pincode"] != "":
                query += " pincode = %s,"
                params.append(data["job_pincode"])

            query += " id = %s WHERE id = %s"
            params.append(job_id)
            params.append(job_id)
            print(query)
            print(params)
            
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def get_candiates_by_job(job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT aj.id AS application_id, c.first_name AS candidate_name, c.email AS candidate_email, c.phone_no AS candidate_phone, c.profile_url AS candidate_profile_pic, c.resume_name AS candidate_resume, aj.application_date, aj.status FROM applied_jobs aj JOIN candidate c ON aj.candidate_id = c.id WHERE aj.job_id = %s", (job_id,))
        candidates = cursor.fetchall()
        for row in candidates:
            if 'application_date' in row and isinstance(row['application_date'], datetime):
                row['application_date'] = row['application_date'].strftime('%d-%m-%Y')
        cursor.close()
        conn.close()
        return candidates
    
    @staticmethod
    def change_password(client_id,new_password):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hash_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        print(hash_password)
        print(client_id)
        cursor.execute("UPDATE client SET password = %s WHERE id = %s", (hash_password,client_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def client_name_list():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT company_name FROM client")
        client_name = cursor.fetchall()
        cursor.close()
        conn.close()
        return client_name
    
    @staticmethod
    def get_jobs_client_by_comapny_name(company_name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT j.id AS job_id,j.job_org AS company_name,j.job_type AS job_type,j.city AS city, j.job_title AS job_title,j.Posted_Date AS job_date , j.sector AS job_sector, j.status AS job_status, j.applied AS job_applied FROM jobs j JOIN client c ON j.job_org = c.company_name WHERE c.company_name = %s",
            (company_name,),
        )
        client_jobs = cursor.fetchall()
        for row in client_jobs:
            if 'job_date' in row and isinstance(row['job_date'], datetime):
                row['job_date'] = row['job_date'].strftime('%d-%m-%Y')
        cursor.close()
        conn.close()
        return client_jobs