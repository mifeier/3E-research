from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal
from ping import *
from factory import create_app
import os
from project import *
from page import *
from functions import *
from result import InvalidAPIUsage

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

api.add_resource(SingleProject, '/project/<pro_Id>')
api.add_resource(ProjectList,'/projects')
api.add_resource(AddPageToProject,'/project/addpage/<pro_Id>')
api.add_resource(SavePageToProject,'/project/savepage')
api.add_resource(SinglePage,'/page/<page_Id>')
api.add_resource(PageList,'/pages')
api.add_resource(AddFuncToPage,'/page/addfunc/<page_Id>')
api.add_resource(SaveFuncToPage,'/page/savefunc')
api.add_resource(SingleFunc,'/func/<func_Id>')
api.add_resource(FuncList,'/funcs')
api.add_resource(SearchDesingerforFunc,'/func/searchdesigner/<func_Id>')
api.add_resource(SaveDesignerforFunc,'/func/savedesigner')


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
