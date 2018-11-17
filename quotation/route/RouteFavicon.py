# coding=utf-8
from flask_restful import Resource
from quotation.api.src.quotation_method import *


class Favicon(Resource):
    def get(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*',
                                 'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
                                 'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'}
