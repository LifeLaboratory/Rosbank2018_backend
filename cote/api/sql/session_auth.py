import cote.api.helpers.base_errors as errors
from cote.api.helpers.service import Sql


class Provider:
    """
    Провайдер для работы с сессией
    """
    @staticmethod
    def select_id_user(Session):
        """
        По сессии получает ID пользователя
        :param args:
        :return:
        """
        query = """
select id_user
from session
where session.session = '{}'
                """.format(Session)
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return result[0]['id_user']
