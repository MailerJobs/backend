from flask_restful import Resource, reqparse,request
from flask import jsonify, make_response
from Models.Required_Skills import Skills

class SkillsListOfJobResource(Resource):
    def get(self):
        skills = Skills.get_all_skills_by_job()
        if not skills:
            return {"message": "No skills found"}, 404
        return skills, 200
    
class SkillsListResource(Resource):
    def get(self):
        skills = Skills.get_all_skills()
        if not skills:
            return {"message": "No skills found"}, 404
        return skills, 200
    

class SkillsResource(Resource):
    def get(self):

        id = request.args.get('id')
        # print ("id= "+id)
        skill = Skills.get_skills_id(id)
        # print("skill = "+str(skill))
        if not skill:
            return {"message": "No skills found"}, 404 
        return skill, 200
    
    def post(self,id):
        skill = Skills.get_skills_id(id)
        return skill