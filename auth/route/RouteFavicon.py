# coding=utf-8
from flask_restful import Resource


class Favicon(Resource):
    def get(self):
        return "OK", 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return "OK", 200, {'Access-Control-Allow-Origin': '*'}
