import cote.api.helpers.base_name as names
import cote.api.helpers.base_errors as errors
from cote.api.sql.quotation_provider import Provider


def quotation_user(user_data):
    """
    Метод по ID формирует данные по валюте для кабинета пользователя
    :param user_data:
    :return:
    """
    check = [names.ID_USER]
    auth_data = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            auth_data[data] = 'Пустой параметр!'
            error = True
        else:
            auth_data[data] = user_data[data]
    if error:
        return errors.AUTH_FAILED, None
    provider = Provider()
    error, quotation = provider.select_quotation_user(auth_data)
    error, name = provider.select_user_name(auth_data)
    answer = {
        "Name": name['name'],
        "Currency": quotation
    }
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None


def get_quotation_actual(user_data):
    check = [names.ID_USER]
    auth_data = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            auth_data[data] = 'Пустой параметр!'
            error = True
        else:
            auth_data[data] = user_data[data]
    if error:
        return errors.AUTH_FAILED, None
    provider = Provider()
    error, answer = provider.select_quotation_actual(user_data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None


def put_quotation_history(user_data):
    """
    Метод добавляет данные о котировках в момент времени
    :return:
    """
    check = [names.ID_QUOTATION_FROM, names.ID_QUOTATION_TO, names.COST,
             names.COEFFICIENT_PURCHARE, names.COEFFICIENT_SALES]
    auth_data = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            auth_data[data] = 'Пустой параметр!'
            error = True
        else:
            auth_data[data] = user_data[data]
    if error:
        return errors.AUTH_FAILED, None
    provider = Provider()
    error, answer = provider.insert_quotation_history(user_data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None

def transaction(args):
    """
    Метод проводит транзакцию покупки/продажи валюты
    :return:
    """
    provider = Provider()
    error, check_cost = provider.check_cost_user(args)
    if check_cost[1]["cost"] - (check_cost[0]["cost"]*float(args[names.COUNT_SEND])) >= 0:
        args["Cost_from"] = check_cost[0]["cost"]*float(args[names.COUNT_SEND])
        error, result = provider.update_quotation_users(args)
        error, result = provider.insert_history_sale(args)
        return error, result

def get_graph(user_data):
    """
    Метод добавляет данные о котировках в момент времени
    :return:
    """
    check = [names.FROM, names.TO,
             names.ID_USER]
    auth_data = dict.fromkeys(check, '')
    error = False
    for data in check:
        if user_data.get(data, None) is None:
            auth_data[data] = 'Пустой параметр!'
            error = True
        else:
            auth_data[data] = user_data[data]
    if error:
        return errors.AUTH_FAILED, None
    provider = Provider()
    # print(user_data)
    error, answer = provider.get_graph(user_data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None