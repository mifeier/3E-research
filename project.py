from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal,abort
from sql import *
from datetime import datetime
from sqlalchemy import or_
#from flask_jwt import jwt_required
import json

project_fields = {
    'Id':fields.Integer,
    'pro_id': fields.Integer,
    'pro_name': fields.String,
    'pro_detail': fields.String,
    'page_id': fields.Integer
}

page_id_fields = {
    'page_id': fields.Integer
}

page_fields = {
    'page_name':fields.String
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
parser.add_argument('pro_id',required=True)
parser.add_argument('pro_name',required=True)
parser.add_argument('pro_detail',required=True)

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

class Obj:
    def returnTrueJson(self,data):
        return jsonify({
            "data":data
        })


#对某个project的操作
class SingleProject(Resource):
    #@marshal_with(project_fields)
    #查询一个project
    def get(self,pro_Id):       
        project=Project.query.filter_by(pro_id=pro_Id).first()      
        if (project is None):
            abort(410,msg="找不到数据",data=None,status=0)
        else:
            return Common.returnTrueJson(Common,marshal(project,project_fields))
           
    #删除一个project
    def delete(self,pro_Id):
        deleteRow=Project.query.filter_by(pro_id=pro_Id).delete()
        db.session.commit()
        if (deleteRow):
            return ProjectList.get(ProjectList)
        else:
            return Common.returnFalseJson(Common)
    #修改一个project
    def put(self,pro_Id):
        args=parser.parse_args()
        pro_id=args['pro_id']
        pro_name=args['pro_name']
        pro_detail=args['pro_detail']
        try:
            project=Project.query.filter_by(pro_id=pro_Id).first()
            project.pro_name=pro_name
            project.pro_detail=pro_detail
            db.session.commit()
            pro_Id=project.pro_id
            data=Project.query.filter_by(pro_id=pro_Id).first()
            return Common.returnTrueJson(Common,marshal(data,project_fields))
        except:
            db.session.rollback()
            db.session.flush()
            abort(409,msg="修改失败",data=None,status=0)
#对project列表的操作
class ProjectList(Resource):
    #查询所有的project
    def get(self):
        return Common.returnTrueJson(Common,marshal(Project.query.all(),project_fields))
    #添加一个project
    def post(self):
        args=parser.parse_args()
        pro_id=args['pro_id']
        pro_name=args['pro_name']
        pro_detail=args['pro_detail']
        project=Project(pro_id=pro_id,pro_name=pro_name,pro_detail=pro_detail)    
        try:
            db.session.add(project)
            db.session.commit()
        except:
            db.session.rollback()   
            db.session.flush()
        if (project.pro_id is None):           
            return Common.returnFalseJson(Common,msg="添加失败")
        else:
            return SingleProject.get(Project,project.pro_id)  

#对project添加页面
class AddPageToProject(Resource):
    def get(self,pro_Id):

        projects = db.session.query(Project.pro_name).all()
        #project=projects[0]
        #pro=project.page_id  

        return Obj.returnTrueJson(Obj,marshal(projects,project_fields))
        # print (type(projects_page_id))
        # return projects_page_id
       


        # return Obj.returnTrueJson(Obj,marshal(project_page,page_fields))
        # pagename=Page.query.filter(Page.page_id not in project_page)
        # pageobj=Obj.returnTrueJson(Obj,marshal(pagename,page_fields))
        #return Common.returnTrueJson(Common,marshal(page,page_fields))  
        
              
        # page_list=[]

        # for pages in page:
        #     if pages.page_id != project.page_id:
        #         page_list.append(pages.page_name)
        #     print (page_list)
        #     return page_list

        # return jsonify({
        #     'page_id':page_list.page_id,
        #     'page_name':page_list.page_name
        # })



            
    



