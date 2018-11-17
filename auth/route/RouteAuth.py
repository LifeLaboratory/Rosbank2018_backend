# coding=utf-8
from auth.api.helpers import base_errors as errors
from auth.api.helpers import base_name as names
from flask_restful import Resource, reqparse
from auth.api.src.Authentication import auth


class Service(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument(names.LOGIN)
        self._parser.add_argument(names.PASSWORD)
        self._parser.add_argument(names.PAGE)
        self.__args = self._parser.parse_args()

    def parse_data(self):
        try:
            data = dict()
            data[names.LOGIN] = self.__args.get(names.LOGIN, None)
            data[names.PASSWORD] = self.__args.get(names.PASSWORD, None)
            data[names.PAGE] = self.__args.get(names.PAGE, None)
        except:
            return errors.PARSE_DATA, None
        if data[names.LOGIN] is None or data[names.PASSWORD] is None or data[names.PAGE] is None:
            return errors.PARSE_DATA, None
        else:
            return errors.OK, data

    def post(self):
        error, data = self.parse_data()
        if error == errors.OK:
            error, answer = auth(data)
            if error == errors.OK:
                return answer, {'Access-Control-Allow-Origin': '*'}
        return {names.SESSION: None}, {'Access-Control-Allow-Origin': '*'}

    def option(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}