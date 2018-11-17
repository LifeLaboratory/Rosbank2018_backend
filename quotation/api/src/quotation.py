import quotation.api.helpers.base_name as names
import quotation.api.helpers.base_errors as errors
from quotation.api.sql.quotation_provider import Provider


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
    print(name)
    answer = {
        "Name": name['name'],
        "Currency": quotation
    }
    print(answer)
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
    print(user_data)
    error, answer = provider.get_graph(user_data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None