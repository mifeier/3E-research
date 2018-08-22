from flask_restful import fields, marshal

error_fields = {
    'code': fields.Integer,
    'message': fields.String
}

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, code, message, payload=None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict()
        rv['result'] = None
        rv['success'] = False
        
        rd = dict()
        rd['code'] = self.code
        rd['message'] = self.message
        rd['detail'] = self.payload
        
        rv['error'] = rd
        return rv

# class Error(object):
#     def __init__(self, code, message):
#         self.code = code
#         self.message = message


# class ArrayResult(object):
#     def __init__(self, items, totalCount):
#         self.items = items
#         self.totalCount = totalCount


# class Result(object):
#     def __init__(self, data, fields, totalCount, error):
#         if isinstance(data, list):
#             self.result = ArrayResult(marshal(data, fields), totalCount)
#         elif data != None:
#             self.result = marshal(data, fields)
#         else:
#             self.result = None
#         self.success = error == None
#         self.error = error


# def GenFields(obj, isMulti):
#     nested_fields = obj
#     if isMulti:
#         nested_fields = {
#             'items': fields.Nested(obj),
#             'totalCount': fields.Integer
#         }

#     resultFields = fields.String

#     if obj != None:
#         resultFields = fields.Nested(nested_fields)

#     return {
#         'result': resultFields,
#         'success': fields.Boolean,
#         'error': fields.String
#     }




