import admin.api.helpers.base_name as names
import admin.api.helpers.base_errors as errors
from admin.api.helpers.service import Sql


class Provider:
    """
    Провайдер для работы с панелью администратора
    """
    @staticmethod
    def change_coefficients(args):
        """
        Метод по связке id валют изменяет коэффициенты котировок
        :param args:
        :return: dict
        """
        coefficient = ""
        if args.get(names.COEFFICIENT_SALES, None) is None:
            coefficient = "set coefficient_purchare = {coefficient_purchare}".format(
                coefficient_purchare=args.get(names.COEFFICIENT_PURCHARE))
        if args.get(names.COEFFICIENT_PURCHARE, None) is None:
            coefficient = "set coefficient_sales = {coefficient_sales}".format(
                coefficient_sales=args.get(names.COEFFICIENT_SALES))
        query = """
update quotation_trade
    {coefficient}
where id_quotation_to = {id_quotation_to} and id_quotation_from = {id_quotation_from}
returning 200 as "Status"
                """.format(coefficient=coefficient,
                           id_quotation_to=args[names.ID_QUOTATION_TO],
                           id_quotation_from=args[names.ID_QUOTATION_FROM]
                           )
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        else:
            return errors.OK, result[0]

    @staticmethod
    def change_pack(args):
        """
        Метод для ручного изменения пакета пользователя
        :param args:
        :return: dict
        """
        query = """
update users
    set rating = {pack}
where id_user = {id_user}
returning 200 as "Status"
                    """.format(pack=args[names.PACK],
                               id_user=args[names.ID_USER])
        print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        else:
            return errors.OK, result[0]

    @staticmethod
    def change_status_pack(args):
        """
        Метод для ручного изменения пакета пользователя
        :param args:
        :return: dict
        """
        query = """
    update users
        set "status_pack" = '{status_pack}'
    where id_user = {id_user}
    returning 200 as "Status"
                        """.format(status_pack=args[names.STATUS_PACK],
                                   id_user=args[names.ID_USER])
        print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        else:
            return errors.OK, result[0]

    @staticmethod
    def list_users():
        """
        Получение списка клиентов
        """
        query = """
select id_user
       , name as "Name"
       , login as "Login"
       , pack::double precision as "Pack"
       , status_pack as "Status_pack"
from users
where privilege = 0
                """
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, {"Status": errors.SQL_ERROR}
        else:
            return errors.OK, result

