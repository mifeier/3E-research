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
        'messages':"A page with that pagename already exists.",
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
#parser.add_argument('func_id',required=True)

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
    #@marshal_with(page_fields)
    #查询一个page
    def get(self,page_Id):       
        page=Page.query.filter_by(page_id=page_Id).first()      
        if (page is None):
            abort(410,msg="找不到数据",data=None,status=0)
        else:
            return Common.returnTrueJson(Common,marshal(page,page_fields))

    #删除一个page
    def delete(self,page_Id):
        deleteRow=Page.query.filter_by(page_id=page_Id).delete()
        db.session.commit()
        if (deleteRow):
            return PageList.get(PageList)
        else:
            return Common.returnFalseJson(Common)
    #修改一个page
    def put(self,page_Id):
        args=parser.parse_args()
        page_id=args['page_id']
        page_name=args['page_name']
        page_detail=args['page_detail']
        #func_id=args['func_id']
        try:
            page=Page.query.filter_by(page_id=page_Id).first()
            page.page_id=page_id
            page.page_name=page_name
            page.page_detail=page_detail
            #page.func_id=func_id
            db.session.commit()
            page_Id=page.page_id
            data=Page.query.filter_by(page_id=page_Id).first()
            return Common.returnTrueJson(Common,marshal(data,page_fields))
        except:
            db.session.rollback()
            db.session.flush()
            abort(409,msg="修改失败",data=None,status=0)


#对pagelist的操作
class PageList(Resource):
    #查询所有的page
    def get(self):
        return Common.returnTrueJson(Common,marshal(Page.query.all(),page_fields))
    
    #添加一个page
    def post(self):
        args=parser.parse_args()
        page_id=args['page_id']
        page_name=args['page_name']
        page_detail=args['page_detail']
        page=Page(page_id=page_id,page_name=page_name,page_detail=page_detail)    
        try:
            db.session.add(page)
            db.session.commit()
        except:
            db.session.rollback()   
            db.session.flush()
        if (page.page_id is None):           
            return Common.returnFalseJson(Common,msg="添加失败")
        else:
            return SinglePage.get(Page,page.page_id)  

#对page添加function
class AddFuncToPage(Resource):
    def get(self,page_Id):
        
