# coding=utf-8
from quotation.api.helpers import base_errors as errors
from quotation.api.helpers import base_name as names
from flask_restful import Resource, reqparse
from quotation.api.src.Authentication import auth


class Quotation(Resource):
    def get(self):
        return {'hello': 'world'}

    def option(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}