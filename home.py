import flask
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class Users(Resource):
    @cross_origin()
    def get(self):
        return {'data':'1'}   
    pass

api.add_resource(Users, '/users')

app.run()