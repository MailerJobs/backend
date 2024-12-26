import mysql.connector
from server.config import Config
from datetime import datetime, timedelta


def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    return connection


def get_time_filter(interval):
    now = datetime.now()

    if interval == "Last Hour":
        return now - timedelta(hours=1)
    elif interval == "Last 24 Hours":
        return now - timedelta(days=1)
    elif interval == "Last Week":
        return now - timedelta(weeks=1)
    elif interval == "Last 2 Weeks":
        return now - timedelta(weeks=2)
    elif interval == "Last Month":
        return now - timedelta(days=30)
    else:
        return None


class Jobs:

    @staticmethod
    def get_all_jobs():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        for row in jobs:
            if "Posted_Date" in row and isinstance(row["Posted_Date"], datetime):
                row["Posted_Date"] = row["Posted_Date"].strftime("%Y-%m-%d %H:%M:%S")
        cursor.close()
        conn.close()
        return jobs

    @staticmethod
    def get_jobs_by_filters(location, date_posted, experience, sector, jobType, skills):
        # print("Location before conn = "+location)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        querywithoutskills = "SELECT j.* FROM jobs j WHERE 1=1"
        querywithskills = "SELECT j.* FROM jobs j "
        # print("Query after q = "+query)
        params = []

        if skills:
            querywithskills += "JOIN job_skills js ON j.id = js.id JOIN skills s ON js.skill_id = s.skill_id WHERE s.skill_name = %s"
            params.append(skills)

            if location:
                print("Location in if = " + location)
                querywithskills += " AND city = %s"
                params.append(location)

            if experience:
                querywithskills += " AND experience = %s"
                params.append(experience)

            if sector:
                querywithskills += " AND sector = %s"
                params.append(sector)

            if jobType:
                querywithskills += " AND job_type = %s"
                params.append(jobType)

            if date_posted:
                filter_date = get_time_filter(date_posted)
                querywithskills += " AND Posted_Date >= %s"
                params.append(filter_date.strftime("%Y-%m-%d %H:%M:%S"))

            cursor.execute(querywithskills, params)

        else:

            if location:
                print("Location in if = " + location)
                querywithoutskills += " AND city = %s"
                params.append(location)

            if experience:
                querywithoutskills += " AND experience = %s"
                params.append(experience)

            if sector:
                querywithoutskills += " AND sector = %s"
                params.append(sector)

            if jobType:
                querywithoutskills += " AND job_type = %s"
                params.append(jobType)

            if date_posted:
                filter_date = get_time_filter(date_posted)
                querywithoutskills += " AND Posted_Date >= %s"
                params.append(filter_date.strftime("%Y-%m-%d %H:%M:%S"))

            cursor.execute(querywithoutskills, params)

        filteredjobs = cursor.fetchall()
        for row in filteredjobs:
            if "Posted_Date" in row and isinstance(row["Posted_Date"], datetime):
                row["Posted_Date"] = row["Posted_Date"].strftime("%Y-%m-%d %H:%M:%S")
        conn.close()
        # print (filteredjobs)
        # query = "SELECT * FROM jobs WHERE 1=1"
        return filteredjobs

    @staticmethod
    def get_job_by_id(job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, job_title, salary, experience, job_description, sector, city, job_type,  education, state, pincode  FROM jobs where id = %s", (job_id,))
        job = cursor.fetchone()
        conn.close()

        return job

    @staticmethod
    def get_jobs_by_sector(sector):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM jobs where sector = %s", (sector,))
        sector_jobs = cursor.fetchall()
        for row in sector_jobs:
            if "Posted_Date" in row and isinstance(row["Posted_Date"], datetime):
                row["Posted_Date"] = row["Posted_Date"].strftime("%Y-%m-%d %H:%M:%S")
        cursor.close()
        conn.close()

        return sector_jobs

    @staticmethod
    def get_jobs_for_search():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT job_title, job_org FROM jobs")
        search_jobs = cursor.fetchall()
        cursor.close()
        conn.close()

        return search_jobs

    @staticmethod
    def get_job_by_search(searchQuery, experience, location):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if searchQuery:
            query += " AND job_title LIKE  %s OR job_org LIKE %s"
            searchpattern = f"%{searchQuery}%"
            params.append(searchpattern)
            params.append(searchpattern)
            print("search Pattern = ", searchpattern)

        if experience:
            query += " AND experience LIKE %s"
            experiencePattern = f"%{experience}%"
            params.append(experiencePattern)
            print("experience pattern = ", experiencePattern)

        if location:
            query += " AND city LIKE %s"
            locationPattern = f"%{location}%"
            params.append(locationPattern)
            print("location pattern = ", locationPattern)

        print(query)

        cursor.execute(query, params)

        results = cursor.fetchall()
        for row in results:
            if "Posted_Date" in row and isinstance(row["Posted_Date"], datetime):
                row["Posted_Date"] = row["Posted_Date"].strftime("%Y-%m-%d %H:%M:%S")
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def create_job(
        job_title,
        salary,
        experience,
        education,
        job_org,
        image_url,
        job_description,
        sector,
        city,
        state,
        pincode,
        job_type
    ):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO jobs ( job_title, salary, experience, education,  job_org, image_url, job_description, sector, city, state, pincode, job_type) VALUE( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                job_title,
                salary,
                experience,
                education,
                job_org,
                image_url,
                job_description,
                sector,
                city,
                state,
                pincode,
                job_type
            ),
        )
        conn.commit()
        job_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return job_id

    @staticmethod
    def delete_job(job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_applied(job_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT applied FROM jobs where id = %s", (job_id,))
        applied = cursor.fetchone()
        cursor.close()
        conn.close()
        return applied

    @staticmethod
    def update_applied(job_id, applied_count):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE jobs SET applied = %s WHERE id = %s", (applied_count, job_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
