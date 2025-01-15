import mysql.connector
from config import Config
from datetime import datetime, timedelta
import bcrypt
from flask import jsonify
import os


def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    return connection


# def generate_update_query(table, update_fields, where_clause):
#     set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
#     where_part = " AND ".join([f"{key} = %s" for key in where_clause.keys()])
#     query = f"UPDATE {table} SET {set_clause} WHERE {where_part}"
#     params = tuple(update_fields.values()) + tuple(where_clause.values())
#     return query, params


class Candidate:

    def __init__(self, id, username, password, is_active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = is_active

    @property
    def is_active(self):
        return self.active

    @staticmethod
    def get_all_candidate():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM candidate")
        candidates = cursor.fetchall()
        for row in candidates:
            if "created_date" in row and isinstance(row["created_date"], datetime):
                row["created_date"] = row["created_date"].strftime("%Y-%m-%d %H:%M:%S")
        cursor.close()
        conn.close()
        return candidates

    @staticmethod
    def already_registered(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM candidate WHERE email = %s", (email,))
        existing_candidate = cursor.fetchone()
        cursor.close()
        conn.close()

        if existing_candidate:
            return Candidate(
                existing_candidate["id"],
                existing_candidate["username"],
                existing_candidate["password"],
            )
        return None

    @staticmethod
    def register_candidate(
        first_name, last_name, username, email, password, phone, pincode
    ):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO candidate (email,first_name, last_name, username, password, phone_no, pincode) VALUE(%s, %s, %s, %s, %s, %s, %s)",
            (email, first_name, last_name, username, hash_password, phone, pincode),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_candidate_by_id(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id,first_name,last_name,email,DOB,phone_no,pincode,sector,college_name,linkedin,facebook,twitter,state,city,pincode,profile_url,resume_name FROM candidate WHERE id = %s",
            (id,),
        )
        candidates = cursor.fetchall()
        cursor.close()
        conn.close()
        return candidates

    @staticmethod
    def uppload_profile_pic(profile_url, id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE candidate SET profile_url = %s WHERE id = %s", (profile_url, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def uplaod_resume(resume_name, id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE candidate SET resume_name = %s WHERE id = %s", (resume_name, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def delete_resume(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE candidate SET resume_name = null WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def post_candidate_liked_job(candidate_id, job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO candidate_jobs (can_id,job_id) VALUE(%s,%s)",
            (candidate_id, job_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def verify_candidate_like_job(candidate_id, job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM candidate_jobs WHERE can_id = %s AND job_id = %s",
            (candidate_id, job_id),
        )
        liked_job = cursor.fetchall()
        cursor.close()
        conn.close()
        return liked_job

    @staticmethod
    def get_candidate_liked_jobs(candidate_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT jobs.* FROM jobs JOIN candidate_jobs ON jobs.id = candidate_jobs.job_id WHERE candidate_jobs.can_id = %s",
            (candidate_id,),
        )
        can_liked_jobs = cursor.fetchall()
        for row in can_liked_jobs:
            if "Posted_Date" in row and isinstance(row["Posted_Date"], datetime):
                row["Posted_Date"] = row["Posted_Date"].strftime("%Y-%m-%d %H:%M:%S")
        cursor.close()
        conn.close()
        return can_liked_jobs

    @staticmethod
    def update_candidate_details(data, candiate_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "UPDATE candidate SET"
        params = []
        print(data["linkedin"])

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

            if data["DOB"] != "":
                query += " DOB = %s,"
                params.append(data["DOB"])

            if data["phone_no"] != "":
                query += " phone_no = %s,"
                params.append(data["phone_no"])

            if data["pincode"] != "":
                query += " pincode = %s,"
                params.append(data["pincode"])

            if data["sector"] != "":
                query += " sector = %s,"
                params.append(data["sector"])

            if data["college_name"] != "":
                query += " college_name = %s,"
                params.append(data["college_name"])

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

            query += "id = %s WHERE id = %s"
            params.append(candiate_id)
            params.append(candiate_id)

        print("Query = ", query)
        print("Params =", params)
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def candidate_already_apply(can_id, job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM applied_jobs where candidate_id = %s and job_id = %s",
            (can_id, job_id),
        )
        already_apply = cursor.fetchall()
        cursor.close()
        conn.close()
        return already_apply

    @staticmethod
    def candiate_apply_job(can_id, job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO applied_jobs(candidate_id,job_id,status) VALUE(%s,%s,%s)",
            (can_id, job_id, "Applied"),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_candidate_job(can_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT aj.id AS application_id,j.id, j.Posted_Date, j.image_url,j.city, j.job_org, j.job_title, j.experience, j.education, j.sector, j.job_description, j.salary, aj.application_date, aj.status FROM applied_jobs aj JOIN candidate c ON aj.candidate_id = c.id JOIN jobs j ON aj.job_id = j.id WHERE aj.candidate_id = %s",
            (can_id,),
        )
        candidate_jobs = cursor.fetchall()
        for row in candidate_jobs:
            if "application_date" in row and isinstance(
                row["application_date"], datetime
            ):
                row["application_date"] = row["application_date"].strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
        for row in candidate_jobs:
            if "Posted_Date" in row and isinstance(
                row["Posted_Date"], datetime
            ):
                row["Posted_Date"] = row["Posted_Date"].strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
        cursor.close()
        conn.close()
        return candidate_jobs

    @staticmethod
    def change_candidate_password(can_id, new_password):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hash_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        print(hash_password)
        print(can_id)
        cursor.execute(
            "UPDATE candidate SET password = %s WHERE id = %s", (hash_password, can_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def get_candidates_email():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT email FROM candidate")
        candidates = cursor.fetchall()
        cursor.close()
        conn.close()
        return candidates
