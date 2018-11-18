# coding=utf-8
from flask_restful import Resource, reqparse
from quotation.api.src.quotation_method import *
from quotation.api.sql.session_auth import Provider


class Quotation(Resource):
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
            if data[names.SESSION] is not None:
                p = Provider()
                data[names.ID_USER] = p.select_id_user(data[names.SESSION])
        except:
            return errors.PARSE_DATA, None
        return errors.OK, data

    def get(self):
        error, data = self.parse_data()
        answer = {}
        # print(data)
        if error == errors.OK:
            if data.get(names.ACTION) == 'list' and data.get(names.SESSION):
                error, answer = get_quotation_actual(data)
            elif data.get(names.SESSION):
                error, answer = quotation_user(data)
            else:
                error, answer = get_quotation_actual(data)
        if error == errors.OK:
            return answer, {'Access-Control-Allow-Origin': '*'}
        return {names.SESSION: None}, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        error, data = self.parse_data()
        if error == errors.OK:
            if data.get(names.ACTION) == 'graph':
                error, answer = get_graph(data)
                if error == errors.OK:
                    # print("answer", answer)
                    return answer, {'Access-Control-Allow-Origin': '*'}
            if data.get(names.ACTION) is not None and data.get(names.SESSION) is not None\
                    and data.get(names.FROM) is not None and data.get(names.TO) is not None\
                    and data.get(names.COUNT_SEND) is not None:
                # print(data)
                error, answer = transaction(data)
                if error == errors.OK:
                    return answer, {'Access-Control-Allow-Origin': '*'}
            else:
                error, answer = put_quotation_history(data)
                if error == errors.OK:
                    return answer, {'Access-Control-Allow-Origin': '*'}
        return {names.STATUS: errors.CHECK_DATA}, {'Access-Control-Allow-Origin': '*'}

    def option(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*',
                                 'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
                                 'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'}
