# coding=utf-8
from flask_restful import Resource, reqparse
from admin.api.src.admin_method import *
from admin.api.sql.session_auth import Provider
from admin.api.sql.admin_provider import Provider

class Admin(Resource):
    def __init__(self):
        self.arguments = [names.SESSION, names.ID_QUOTATION_TO, names.ID_QUOTATION_FROM,
                          names.COEFFICIENT_PURCHARE, names.COEFFICIENT_SALES, names.PACK,
                          names.ACTION, names.ID_USER, names.STATUS_PACK]
        self._parser = reqparse.RequestParser()
        for argument in self.arguments:
            self._parser.add_argument(argument)
        self.__args = self._parser.parse_args()

    def parse_data(self):
        try:
            data = dict()
            for argument in self.arguments:
                data[argument] = self.__args.get(argument, None)
                if data[argument]:
                    print(argument, data[argument])
            if data[names.SESSION]:
                p = Provider()
                data[names.ID_USER] = p.select_id_user(data[names.SESSION])
        except:
            return errors.PARSE_DATA, None
        return errors.OK, data

    def get(self):
        error, data = self.parse_data()
        if error == errors.OK:
            if data.get(names.ACTION) == "list":
                p = Provider()
                error, answer = p.list_users()
                if error == errors.OK:
                    return answer, {'Access-Control-Allow-Origin': '*'}
        return errors.ROUTE, {names.SESSION: errors.ROUTE}, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        error, data = self.parse_data()
        if error == errors.OK:
            if data.get(names.ID_QUOTATION_TO, None) and data.get(names.ID_QUOTATION_FROM, None) and \
                    data.get(names.COEFFICIENT_SALES, None) or data.get(names.COEFFICIENT_PURCHARE, None):
                error, answer = change_coefficient(data)
                if error == errors.OK:
                    return errors.OK, answer, {'Access-Control-Allow-Origin': '*'}

            if data.get(names.ID_USER, None) is not None and data.get(names.PACK, None) is not None:
                error, answer = change_pack(data)
                if error == errors.OK:
                    return errors.OK, answer, {'Access-Control-Allow-Origin': '*'}

            if data.get(names.ID_USER, None) is not None and data.get(names.STATUS_PACK, None) is not None:
                error, answer = change_status_pack(data)
                if error == errors.OK:
                    return errors.OK, answer, {'Access-Control-Allow-Origin': '*'}
        return errors.ROUTE, {names.SESSION: errors.ROUTE}, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*',
                                 'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
                                 'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'}
