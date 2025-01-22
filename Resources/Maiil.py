from flask import jsonify, make_response
from config import Config
from flask_restful import Resource, reqparse, request
from flask_mail import Mail, Message


class MailResource(Resource):

    def __init__(self, mail):
        self.mail = mail

    def post(self):
        data = request.json
        recipient = data.get("email")  # Email entered by user
        subject = data.get("subject", "Your Job Application")  # Default subject
        body = data.get("body", "Thank you for applying!")
        sender_email = Config.MAIL_USERNAME

        if not recipient:
            return make_response(jsonify({"error": "Recipient email is required"}), 400)

        try:
            msg = Message(subject,sender=sender_email, recipients=[recipient], body=body)
            self.mail.send(msg)
            return make_response(jsonify({"message": "Email sent successfully"}), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
