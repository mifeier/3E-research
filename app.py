from flask import Flask, jsonify, request
# from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal
from ping import *
from factory import create_app
import os

app = Flask(__name__)
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app=create_app(app)
api = Api(app)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_AUTH_URL_RULE'] = '/api/v1/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'userId'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_resource(ApiPing, '/api/v1/ping')






if __name__ == '__main__':
    app.run(host='0.0.0.0')
