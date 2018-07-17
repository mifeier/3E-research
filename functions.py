from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal,abort
from sql import *
from datetime import datetime
#from flask_jwt import jwt_required

functions_fields = {
    'Id':fields.Integer,
    'func_id': fields.Integer,
    'func_name': fields.String,
    'func_detail': fields.String,
    'designer_id': fields.Integer
}

errors={
    'ProjectAlreadyExistsError':{
        'messages':"A functions with that functionsname already exists.",
        'status':409,
    },
    'ResourceDoesNotEsist':{
        'message':"A resource with that ID no longer exists.",
        'status':410,
        'extra':"Any extra information you want."
    }
}

parser=reqparse.RequestParser()
parser.add_argument('func_id',required=True)
parser.add_argument('func_name',required=True)
parser.add_argument('func_detail',required=True)
#parser.add_argument('designer_id',required=True)

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
#对某个function的操作
class SingleFunctions(Resource):
    #@marshal_with(functions_fields)
    #查询一个function
    def get(self,func_Id):       
        func=Function.query.filter_by(func_id=func_Id).first()      
        if (func is None):
            abort(410,msg="找不到数据",data=None,status=0)
        else:
            return Common.returnTrueJson(Common,marshal(func,functions_fields))

    #删除一个function
    def delete(self,func_Id):
        deleteRow=Function.query.filter_by(func_id=func_Id).delete()
        db.session.commit()
        if (deleteRow):
            return FunctionsList.get(FunctionsList)
        else:
            return Common.returnFalseJson(Common)
    #修改一个function
    def put(self,func_Id):
        args=parser.parse_args()
        func_id=args['func_id']
        func_name=args['func_name']
        func_detail=args['func_detail']
        #designer_id=args['designer_id']
        try:
            func=Function.query.filter_by(func_id=func_Id).first()
            func.func_id=func_id
            func.func_name=func_name
            func.func_detail=func_detail
            #func.designer_id=designer_id
            db.session.commit()
            func_Id=func.func_id
            data=Function.query.filter_by(func_id=func_Id).first()
            return Common.returnTrueJson(Common,marshal(data,functions_fields))
        except:
            db.session.rollback()
            db.session.flush()
            abort(409,msg="修改失败",data=None,status=0)


#对functionslist的操作
class FunctionsList(Resource):
    #查询所有的functions
    def get(self):
        return Common.returnTrueJson(Common,marshal(Function.query.all(),functions_fields))
    
    #添加一个functions
    def post(self):
        args=parser.parse_args()
        func_id=args['func_id']
        func_name=args['func_name']
        func_detail=args['func_detail']
        func=Function(func_id=func_id,func_name=func_name,func_detail=func_detail)    
        try:
            db.session.add(func)
            db.session.commit()
        except:
            db.session.rollback()   
            db.session.flush()
        if (func.func_id is None):           
            return Common.returnFalseJson(Common,msg="添加失败")
        else:
            return SingleFunctions.get(Function,func.func_id)  


