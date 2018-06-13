from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal

class ApiPing(Resource):
    def get(self):
        return 'pong'