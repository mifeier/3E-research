from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal
from ping import *
from factory import create_app
import os
from project import *
from page import *

app = Flask(__name__)
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app=create_app(app)

api = Api(app,catch_all_404s=True,errors=errors)

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_AUTH_URL_RULE'] = '/api/v1/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'userId'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSON_AS_ASCII'] = False

api.add_resource(SingleProject, '/project/<int:pro_Id>')
api.add_resource(ProjectList,'/projects')
api.add_resource(AddPageToProject,'/project/addpage/<int:pro_Id>')
api.add_resource(SinglePage,'/page/<int:page_Id>')
api.add_resource(PageList,'/pages')




if __name__ == '__main__':
    app.run(host='0.0.0.0')
