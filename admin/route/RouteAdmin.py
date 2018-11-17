# coding=utf-8
from flask_restful import Resource, reqparse
from admin.api.src.admin_method import *
from admin.api.sql.session_auth import Provider


class Admin(Resource):
    def __init__(self):
        self.arguments = [names.SESSION, names.ID_QUOTATION_TO, names.ID_QUOTATION_FROM,
                          names.COEFFICIENT_PURCHARE, names.COEFFICIENT_SALES, names.COST,
                          names.ACTION, names.QUANT, names.FROM, names.TO, names.COUNT_SEND]
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

    def post(self):
        error, data = self.parse_data()
        if error == errors.OK:
            if data.get(names.ID_QUOTATION_TO, None) and data.get(names.ID_QUOTATION_FROM, None) and \
                    data.get(names.COEFFICIENT_SALES, None) or data.get(names.COEFFICIENT_PURCHARE, None):
                error, answer = change_coefficient(data)
                if error == errors.OK:
                    return errors.OK, answer, {'Access-Control-Allow-Origin': '*'}

        return errors.ROUTE, {names.SESSION: errors.ROUTE}, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*',
                                 'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
                                 'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'}
