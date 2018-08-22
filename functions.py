from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, fields, Api, marshal, marshal_with, abort
from sql import * 
from result import *

func_fields = {
    'Id':fields.Integer,
    'func_id':fields.Integer,
    'func_name':fields.String,
    'func_detail':fields.String,
    'designer_id':fields.Integer,
    'flag':fields.Boolean
}

designer_fields = {
    'designer_id':fields.Integer,
    'content':fields.String
}
parser = reqparse.RequestParser()

class Commom:
    def returnTrueJosn(self, data, msg="请求成功"):
        return jsonify({
            'status':1,
            'data':data,
            'msg':msg,
        })
    def returnFalseJson(self, data, msg = '请求失败'):
        return jsonify({
            'status':1,
            'data':data,
            'msg':msg
        })

#对某个function进行的操作
class SingleFunc(Resource):
    def get(self,func_Id):
        func = Function.query.filter_by(func_id= func_Id,flag = 1).first()
        if func is None:
            raise InvalidAPIUsage(3001,"this func_id and flag has no message")
        else:
            return Commom.returnTrueJosn(Commom,marshal(func,func_fields))
    #删除某个指定的function
    def delete(self,func_Id):
        func = Function.query.filter_by(func_id = func_Id,flag = 1).delete()
        if func is None:
            raise InvalidAPIUsage(3001,"this func_id and flag has no message")
        else:
            try:
                db.session.commit()
                return FuncList.get(FuncList)
            except:
                raise InvalidAPIUsage(3003,"delete the functions and flag=1 failed")

    #修改某个指定的function
    def put(self,func_Id):
        parser = reqparse.RequestParser()
        parser.add_argument('func_name',required = True)
        parser.add_argument('func_detail',required = True)
        args = parser.parse_args()
        func_name = args['func_name']
        func_detail = args['func_detail']
        try:
            func = Function.query.filter_by(func_id = func_Id,flag = 1).first()
            func.func_name = func_name
            func.func_detail = func_detail
            db.session.commit()
            data = Function.query.filter_by(func_id = func_Id,flag = 1).first()
            return Commom.returnTrueJosn(Commom,marshal(data,func_fields))
        except:
            db.session.rollback()
            db.session.flush()
            raise InvalidAPIUsage(3002,"update the function's message failed")

#对FunctionList的操作
class FuncList(Resource):
    #查询所有flag=1的function
    def get(self):
        func = Function.query.filter_by(flag = 1).all()
        return Commom.returnTrueJosn(Commom,marshal(func,func_fields))
        #添加一个function
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('func_id')
        parser.add_argument('func_name')
        parser.add_argument('func_detail')
        args = parser.parse_args()
        func_id = args['func_id']
        func_name = args['func_name']
        func_detail = args['func_detail']
        data = Function(func_id = func_id,func_name = func_name,func_detail = func_detail,flag = 1)
        try:          
            db.session.add(data)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        func = Function.query.filter_by(func_id = func_id,flag = 1).first()
        if (func):
            return Commom.returnTrueJosn(Commom,marshal(func,func_fields))
        else:
            raise InvalidAPIUsage()

#查询出除该function下其他的desiger信息
class SearchDesingerforFunc(Resource):
    def get(self,func_Id):
        func_data1 = Function.query.filter_by(func_id = func_Id,flag = 1).all()
        func_data2 = Function.query.filter_by(func_id = func_Id,flag = 0).all()
        designers = Designer.query.all()
        if len(func_data1)<=0:
            raise InvalidAPIUsage(3001,"this func_id and flag has no message")
        else:
            if len(func_data2)<=0:
                return Commom.returnTrueJosn(Commom,marshal(designers,designer_fields))
            else:
                func_datas=[]
                for func_data in func_data2:
                    func_datas.append({'designer_Id':func_data.designer_id})
                if len(designers) <= 0:
                    raise InvalidAPIUsage(3004,"there are no the flag=1 desinger's message")
                else:
                    designer_datas = []
                    for designer in designers:
                        designer_datas.append({"designer_ID":designer.designer_id})
                    designer_names = []
                    for i in range(len(func_datas)):
                        for j in range(len(designer_datas)):
                            if func_datas[i]['designer_Id'] != designer_datas[j]['designer_ID']:
                                designer_name_s = Designer.query.filter_by(designer_id = designer_datas[j]['designer_ID']).all()
                                for designername in designer_name_s:
                                    designer_names.append({'designer_id':designername.design_id,'content':designername.content})
                    if jsonify(designer_names) is None:
                        return jsonify(designer_names)
                    else:
                        raise InvalidAPIUsage(3006,"this func_id and flag=1 have all designers message")

#对选择的designers进行保存和删除
class SaveDesignerforFunc(Resource):
    #对选择的designers进行保存
    def post(self):
        parser.add_argument('func_id')
        parser.add_argument('designer_id')
        args = parser.parse_args()
        func_id = args['func_id']
        designer_id = args['designer_id']
        designer_ids = designer_id.split(',')
        datas = []
        function = Function.query.filter_by(func_id = func_id,flag = 1).first()
        try:
            for i in designer_ids:
                data = Function(func_id = func_id,func_name = function.func_name,func_detail = function.func_detail,designer_id = i,flag = 0)
                db.session.add(data)
                db.session.commit()
            funcs = Function.query.filter_by(func_id = func_id,flag = 0).all()
            return Commom.returnTrueJosn(Commom,marshal(funcs,func_fields))
        except:
            raise InvalidAPIUsage(3005,"add the functions and flag=1 faield,save faield")

    #对选择的designers进行删除
    def delete(self):
        parser.add_argument('func_id')
        parser.add_argument('designer_id')
        args = parser.parse_args()
        func_id = args['func_id']
        designer_id = args['designer_id']
        designer_ids = designer_id.split(',')
        for i in designer_ids:
            deletedata = Function.query.filter_by(func_id = func_id,designer_id = i,flag = 0).delete()
            db.session.commit()
        funcdata = Function.query.filter_by(func_id = func_id,flag = 0).all()
        if (deletedata):
            return Commom.returnTrueJosn(Commom,marshal(funcdata,func_fields))
        else:
            raise InvalidAPIUsage(3007,"delete the func's designers message faield")

        