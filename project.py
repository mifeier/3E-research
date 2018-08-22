from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal,abort
from sql import *
from datetime import datetime
from sqlalchemy import or_
#from flask_jwt import jwt_required
import json
from result import *

project_fields = {
    'Id':fields.Integer,
    'pro_id': fields.Integer,
    'pro_name': fields.String,
    'pro_detail': fields.String,
    'page_id': fields.Integer,
    'flag':fields.Boolean
}
page_fields = {
    'page_id':fields.Integer,
    'page_name':fields.String
}
errors={
    'ProjectAlreadyExistsError':{
        'messages':"The pro_id not exists.",
        'status':409,
    },
    'ResourceDoesNotEsist':{
        'message':"there has no any page message.",
        'status':410,
        'extra':"Any extra information you want."
    }
}

parser=reqparse.RequestParser()
class Common:
    def returnTrueJson(self,data,msg="请求成功"):
        return jsonify({
            "status":1,
            "data":data,
            "msg":msg
        })
    def returnFalseJson(self,data,msg="请求失败"):
        return jsonify({
            "status":0,
            "data":data,
            "msg":msg
        })

#对某个project的操作
class SingleProject(Resource):
    #@marshal_with(project_fields)
    #查询一个project
    def get(self,pro_Id):  
        projects=Project.query.filter_by(pro_id=pro_Id,flag = 1).all()
        if len(projects) <= 0:
            raise InvalidAPIUsage(1001, 'this pro_id has no message')
        else:
            for project in projects:
                if (project.pro_detail is None):
                    raise InvalidAPIUsage(1003, 'project detail is null')
                else:
                    return Common.returnTrueJson(Common,marshal(projects,project_fields))
           
    #删除一个project
    def delete(self,pro_Id):
        deleteRow=Project.query.filter_by(pro_id = pro_Id,flag = 1).delete()
        db.session.commit()
        if (deleteRow):
            return ProjectList.get(Project)
        else:
            raise InvalidAPIUsage(1005,"delete the project failed")
    #修改一个project
    def put(self,pro_Id):  
        parser=reqparse.RequestParser()     
        parser.add_argument('pro_name',required = True)
        parser.add_argument('pro_detail',required = True) 
        args=parser.parse_args() 
        pro_Name = args['pro_name']
        pro_Detail = args['pro_detail']
        try:
            project = Project.query.filter_by(pro_id=pro_Id,flag = 1).first()
            project.pro_name=pro_Name
            project.pro_detail = pro_Detail
            db.session.commit()
            project = Project.query.filter_by(pro_id=pro_Id,flag = 1).first()
            return Common.returnTrueJson(Common,marshal(project,project_fields)) 

        except:
            db.session.rollback()
            db.session.flush()
            raise InvalidAPIUsage(1004,"update the project message failed")


#对ProjectList的操作
class ProjectList(Resource):
    def get(self):
        return Common.returnTrueJson(Common,marshal(Project.query.filter_by(flag = 1).all(),project_fields))

#添加一个project信息
    def post(self):
        parser=reqparse.RequestParser()     
        parser.add_argument('pro_id',required=True,type = int)
        parser.add_argument('pro_name',required=True,type=str)
        parser.add_argument('pro_detail',required=True,type = str)
        args = parser.parse_args()
        pro_id = args['pro_id']
        pro_name = args['pro_name']
        pro_detail = args['pro_detail']
        project = Project(pro_id = pro_id,pro_name = pro_name,pro_detail = pro_detail,flag = 1)
        try:
            db.session.add(project)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        if (project is None):
            return Common.returnFalseJson(Common,msg="添加失败")
        else:
            return SingleProject.get(Project,project.pro_id)

#查询除此project下已有的page的其他所有page名称
class AddPageToProject(Resource):
    def get(self,pro_Id):
        
        project_data1 = Project.query.filter_by(pro_id = pro_Id,flag = 1).all()
        project_data2 = Project.query.filter_by(pro_id = pro_Id,flag = 0).all()
        page_data=Page.query.filter_by(flag = 1).all()
        #data和page_data都为list类型
        if len(project_data1) <= 0:
            raise InvalidAPIUsage(1001, 'this pro_id and the flag=1 has no message')
        else:
            if len(project_data2)<=0:
                return Common.returnTrueJson(Common,marshal(page_data,page_fields))
            else:
                datas = []
                for project in project_data2:
                    #project为sql.Project
                    datas.append({'page_ID':project.page_id})
                if len(page_data) <= 0:
                    raise InvalidAPIUsage(1002, "there are no page's message")
                else:
                    page_datas = []
                    for page in page_data:
                        page_datas.append({'page_ID':page.page_id})
                    page_names=[]
                    #datas和page_datas为list类型，list嵌套字典
                    for i in range(len(datas)):          
                        for j in range(len(page_datas)):             
                            if datas[i]['page_ID'] != page_datas[j]['page_ID']:
                                page_name=Page.query.filter_by(page_id = page_datas[j]['page_ID'],flag = 1).all()
                                for pagename in page_name:
                                    page_names.append({'page_id':pagename.page_id,'page_name':pagename.page_name})
                    return jsonify(page_names)

#对选择的page进行保存
class SavePageToProject(Resource):    
    def post(self):
        parser=reqparse.RequestParser()       
        parser.add_argument('pro_id',required = True,type = int)
        parser.add_argument('page_id',required = True)
        args = parser.parse_args()
        pro_id = args['pro_id']
        page_id = args['page_id']
        page_ids = page_id.split(',')
        datas = []
        project = Project.query.filter_by(pro_id = pro_id,flag = 1).first()
        for i in page_ids:
            data = Project(pro_id=pro_id,pro_name = project.pro_name,pro_detail = project.pro_detail,page_id = i,flag = 0)
            db.session.add(data)
            db.session.commit()
        projects = Project.query.filter_by(pro_id = pro_id,flag = 0).all()
        return Common.returnTrueJson(Common,marshal(projects,project_fields))
        
#删除project下的某几个页面并保存
    def delete(self):
        parser.add_argument('pro_id',required = True,type = int)
        parser.add_argument('page_id',required = True)
        args = parser.parse_args()
        pro_id = args['pro_id']
        page_id = args['page_id']
        page_ids = page_id.split(',')
        datas = []
        for i in page_ids:
            deleteData = Project.query.filter_by(pro_id = pro_id,page_id = i,flag = 0).delete()
            db.session.commit()
        project = Project.query.filter_by(pro_id = pro_id,flag = 0).all()
        if (deleteData):
            return Common.returnTrueJson(Common,marshal(project,project_fields))
        else:
            raise InvalidAPIUsage(1006,"delete the project's pages faield")


            