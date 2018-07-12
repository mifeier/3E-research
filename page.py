from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal,abort
from sql import *
from datetime import datetime
#from flask_jwt import jwt_required

page_fields = {
    'Id':fields.Integer,
    'page_id': fields.Integer,
    'page_name': fields.String,
    'page_detail': fields.String,
    'func_id': fields.Integer
}

errors={
    'ProjectAlreadyExistsError':{
        'messages':"A user with that username already exists.",
        'status':409,
    },
    'ResourceDoesNotEsist':{
        'message':"A resource with that ID no longer exists.",
        'status':410,
        'extra':"Any extra information you want."
    }
}

parser=reqparse.RequestParser()
parser.add_argument('page_id',required=True)
parser.add_argument('page_name',required=True)
parser.add_argument('page_detail',required=True)

class Common:
    def returnTrueJson(self,data,msg="请求成功"):
        return jsonify({
            "status":1,
            "data":data,
            "msg":msg
        })
    def returnFalseJson(self,data=None,msg="请求失败"):
        return jsonify({
            "status":0,
            "data":data,
            "msg":msg
        })
#对某个project的操作
class SinglePage(Resource):
    #@marshal_with(project_fields)
    #查询一个project
    def get(self,page_Id):       
        page=Page.query.filter_by(page_id=page_Id).first()      
        if (page is None):
            abort(410,msg="找不到数据",data=None,status=0)
        else:
            return Common.returnTrueJson(Common,marshal(page,page_fields))



#对page list的操作
class PageList(Resource):
    #查询所有的project
    def get(self):
        return Common.returnTrueJson(Common,marshal(Page.query.all(),page_fields))