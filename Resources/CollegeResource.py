from flask_restful import Resource, reqparse
from Models.Colleges import Colleges
from flask import jsonify, make_response

class CollegesListReosurce(Resource):
    def get(self):
        colleges = Colleges.get_all_colleges()
        if not colleges:
            return {"message": "No Colleges Found"}
        return colleges, 200
    
class CollegeResource(Resource):
    def get(self, college_name):
        college = Colleges.get_college_by_name(college_name)
        if not college:
            return {"message": "College Not Found"}, 404
        return college, 200
    
class CollegeNamesListResource(Resource):
    def get(self):
        colleges = Colleges.get_college_names()
        if not colleges:
            return {"message": "No Colleges Found"}
        return colleges, 200