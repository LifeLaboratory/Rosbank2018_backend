import quotation.api.helpers.base_name as names
import quotation.api.helpers.base_errors as errors
from quotation.api.helpers.service import Sql


class Provider:
    """
    Провайдер для работы с котировками
    """



    @staticmethod
    def select_user_name(args):
        """
        По ID пользователя получает его имя
        :param args:
        :return: dict
        """
        query = """
  select Name
  from users
  where id_user = {}
                    """.format(args['id_user'])
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            print(result)
            return errors.OK, result[0]

    @staticmethod
    def select_quotation_user(args):
        """
        По ID пользователя получает все его деньги по валютам
        :param args:
        :return:
        """
        query = """
select
 id_quotation as id_currency
 , name as Name_currency
 , cost::double precision
from quotation q
left join (
  select *
  from quotation_users
  where id_user = {}
) qu using(id_quotation)
                """.format(args['id_user'])
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result

    @staticmethod
    def select_quotation_actual(args):
        """
        Получает актуальные данные по котировкам
        :param args:
        :return:
        """
        query = """
insert into quotation_history(id_quotation_from, id_quotation_to, cost, 
name, coefficient_sales, coefficient_purchare) 
values ()
                """
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, {'quotation': result}

    @staticmethod
    def select_quotation_actual():
        """
        Получает актуальные данные по котировкам
        :param args:
        :return:
        """
        query = """
select 
  id_quotation_from
  , id_quotation_to
  , Name
  , cost + coefficient_sales as Count_sale
  , cost + coefficient_purchare as Count_purchare
from quotation_trade
                """
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, {'quotation': result}
