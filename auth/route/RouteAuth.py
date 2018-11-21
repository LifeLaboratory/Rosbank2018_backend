# coding=utf-8
from auth.api.helpers import base_name as names
from flask_restful import Resource, reqparse
from auth.api.src.Authentication import auth


class Auth(Resource):
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
            return 500, None
        if data[names.LOGIN] is None or data[names.PASSWORD] is None or data[names.PAGE] is None:
            return 400, None
        else:
            return 200, data

    def post(self):
        status_code, data = self.parse_data()
        if status_code == 200:
            status_code, answer = auth(data)
            if status_code == 200:
                return answer, {"status": status_code}
        return None, {"status": status_code}
