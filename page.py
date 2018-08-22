from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal,abort
from sql import *
from datetime import datetime
from result import *
#from flask_jwt import jwt_required

page_fields = {
    'Id':fields.Integer,
    'page_id': fields.Integer,
    'page_name': fields.String,
    'page_detail': fields.String,
    'func_id': fields.Integer,
    'flag': fields.Boolean
}

func_fields = {
    'func_id':fields.Integer,
    'func_name':fields.String
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
#对某个page的操作
class SinglePage(Resource):
    #@marshal_with(page_fields)
    #查询一个page
    def get(self,page_Id):       
        page=Page.query.filter_by(page_id=page_Id,flag = 1).first()      
        if (page is None):
            raise InvalidAPIUsage(2001, 'this page_id and flag has no message')
        else:
            return Common.returnTrueJson(Common,marshal(page,page_fields))

    #删除一个实际存在的page
    def delete(self,page_Id):
        deleteRow=Page.query.filter_by(page_id=page_Id,flag = 1).delete()
        db.session.commit()
        if (deleteRow):
            return PageList.get(PageList)
        else:
            raise InvalidAPIUsage(2001,'this page_id and flag has no message')
    #修改一个实际存在的page
    def put(self,page_Id):
        parser=reqparse.RequestParser()
        parser.add_argument('page_name',required=True)
        parser.add_argument('page_detail',required=True)
        args=parser.parse_args()
        page_name=args['page_name']
        page_detail=args['page_detail']
        try:
            page=Page.query.filter_by(page_id = page_Id,flag = 1).first()
            page.page_name = page_name
            page.page_detail = page_detail
            db.session.commit()
            data=Page.query.filter_by(page_id=page_Id,flag = 1).first()
            return Common.returnTrueJson(Common,marshal(data,page_fields))
        except:
            db.session.rollback()
            db.session.flush()
            raise InvalidAPIUsage(2002,"update the page message failed")

#对pagelist的操作
class PageList(Resource):
    #查询所有的page
    def get(self):
        return Common.returnTrueJson(Common,marshal(Page.query.filter_by(flag = 1).all(),page_fields))
    
    #添加一个实际的page
    def post(self,Flag):
        parser.add_argument('page_id',required = True)
        parser.add_argument('page_name',required = True)
        parser.add_argument('page_detail',required = True)
        args=parser.parse_args()
        page_id=args['page_id']
        page_name=args['page_name']
        page_detail=args['page_detail']
        page=Page(page_id=page_id,page_name=page_name,page_detail=page_detail,flag = 1)    
        try:
            db.session.add(page)
            db.session.commit()
        except:
            db.session.rollback()   
            db.session.flush()
        data = Page.query.filter_by(page_id = page_id,flag = 1).first()
        if (data is None):           
            raise InvalidAPIUsage(2003,"add the page message failed")
        else:
            return SinglePage.get(Page,page.page_id)  

#对flag为0的page添加function,先查询出除已有页面之外的其他页面
class AddFuncToPage(Resource):
    def get(self,page_Id):
        page_datas1 = Page.query.filter_by(page_id = page_Id,flag = 1).all()
        page_datas2 = Page.query.filter_by(page_id = page_Id,flag = 0).all()
        functions = Function.query.filter_by(flag = 1).all()
        if len(page_datas1)<=0:
            raise InvalidAPIUsage(2001,"this page_id and flag=1 has no message")
        else:
            if len(page_datas2)<=0:
                return Common.returnTrueJson(Common,marshal(functions,func_fields))
            else:       
                page_datas = []
                for page in page_datas2:
                    page_datas.append({"func_ID":page.func_id})
                if len(functions) <= 0:
                    raise InvalidAPIUsage(2004,"there are no the flag=1 funcions's message")
                else:
                    function_datas = []
                    for function in functions:
                        function_datas.append({"func_ID":function.func_id})
                    func_names = []
                    for i in range(len(page_datas)):
                        for j in range(len(function_datas)):
                            if page_datas[i]['func_ID'] != function_datas[j]['func_ID']:
                                func_name_s = Function.query.filter_by(func_id = function_datas[j]['func_ID'],flag = 1).all()
                                for funcname in func_name_s:
                                    func_names.append({'func_id':funcname.func_id,'func_name':funcname.func_name})
                    return jsonify(func_names)

#将用户所选择的functions进行保存
class SaveFuncToPage(Resource):
    def post(self):
        parser.add_argument('page_id')
        parser.add_argument('func_id')
        args = parser.parse_args()
        page_id = args['page_id']
        func_id = args['func_id']
        func_ids = func_id.split(',')
        datas = []
        page = Page.query.filter_by(page_id = page_id,flag = 1).first()
        try:
            for i in func_ids:
                data = Page(page_id = page_id,page_name = page.page_name,page_detail = page.page_detail,func_id = i,flag = 0)
                db.session.add(data)
                db.session.commit()
            pages = Page.query.filter_by(page_id = page_id,flag = 0).all()
            return Common.returnTrueJson(Common,marshal(pages,page_fields))
        except:
            raise InvalidAPIUsage(2005,"add the page's functions message faield,save failed")

#将用户所选择的functions进行删除并保存
    def delete(self):
        parser.add_argument('page_id')
        parser.add_argument('func_id')
        args = parser.parse_args()
        page_id = args['page_id']
        func_id = args['func_id']
        func_ids = func_id.split(',')
        #datas = []
        for func_id in func_ids:
            deletedata = Page.query.filter_by(page_id = page_id,func_id = func_id,flag = 0).delete()
            db.session.commit()
        pagedata = Page.query.filter_by(page_id = page_id,flag = 0).all()
        if (deletedata):
            return Common.returnTrueJson(Common,marshal(pagedata,page_fields))
        else:
            raise InvalidAPIUsage(2006,"delete the page's functions message faield,save faield")

