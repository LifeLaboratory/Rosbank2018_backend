# coding=utf-8
from quotation.api.helpers import base_errors as errors
from quotation.api.helpers import base_name as names
from flask_restful import Resource, reqparse
from quotation.api.src.quotation import *
from quotation.api.sql.session_auth import Provider


class Quotation(Resource):
    def __init__(self):
        self.arguments = [names.SESSION, names.ID_QUOTATION_TO, names.ID_QUOTATION_FROM,
                          names.COEFFICIENT_PURCHARE, names.COEFFICIENT_SALES, names.COST]
        self._parser = reqparse.RequestParser()
        for argument in self.arguments:
            self._parser.add_argument(argument)
        self.__args = self._parser.parse_args()

    def parse_data(self):
        try:
            data = dict(short=None, long=None)
            for argument in self.arguments:
                data[argument] = self.__args.get(argument, None)
            if data[names.SESSION]:
                p = Provider()
                data[names.ID_USER] = p.select_id_user(data[names.SESSION])
        except:
            return errors.PARSE_DATA, None
        return errors.OK, data

    def get(self):
        error, data = self.parse_data()
        answer = {}
        if error == errors.OK:
            if data.get(names.SESSION):
                error, answer = quotation_user(data)
            else:
                error, answer = get_quotation_actual()
        if error == errors.OK:
            return answer, {'Access-Control-Allow-Origin': '*'}
        return {names.SESSION: None}, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        error, data = self.parse_data()
        answer = {}
        if error == errors.OK:
            error, answer = put_quotation_history(data)
        if error == errors.OK:
            return answer, {'Access-Control-Allow-Origin': '*'}
        return {names.SESSION: None}, {'Access-Control-Allow-Origin': '*'}

    def option(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}
