from flask_restful import Resource, reqparse
from Models.Colleges import Colleges
from flask import jsonify, make_response

class CollegesListReosurce(Resource):
    def get(self):
        colleges = Colleges.get_all_colleges()
        if not colleges:
            return {"message": "No Colleges Found"}
        return colleges, 200