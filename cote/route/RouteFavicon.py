# coding=utf-8
from flask_restful import Resource
from cote.api.src.cote_method import *


class Favicon(Resource):
    def get(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}
    def option(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}
