import quotation.api.helpers.base_name as names
import quotation.api.helpers.base_errors as errors
from quotation.api.sql.quotation_provider import Provider


def quotation_user(args):
    """
    Метод по ID формирует данные по валюте для кабинета пользователя
    :param args:
    :return:
    """
    check = [names.ID_USER]
    data = dict.fromkeys(check, '')
    error = False
    for c in check:
        if args.get(c, None) is None:
            data[c] = 'Пустой параметр!'
            error = True
        else:
            data[c] = args[c]
    if error:
        return errors.logic, None
    provider = Provider()
    error, quotation = provider.select_quotation_user(data)
    error, name = provider.select_user_name(data)
    answer = {
        "Name": name['name'],
        "Currency": quotation
    }
    if error == errors.OK:
        return errors.OK, answer
    return errors.logic, None


def get_quotation_actual(args):
    check = [names.ID_USER]
    data = dict.fromkeys(check, '')
    error = False
    for c in check:
        if args.get(c, None) is None:
            data[c] = 'Пустой параметр!'
            error = True
        else:
            data[c] = args[c]
    if error:
        return errors.logic, None
    provider = Provider()
    error, answer = provider.select_quotation_actual(args)
    if error == errors.OK:
        return errors.OK, answer
    return errors.logic, None


def put_quotation_history(args):
    """
    Метод добавляет данные о котировках в момент времени
    :return:
    """
    check = [names.ID_QUOTATION_FROM, names.ID_QUOTATION_TO, names.COST,
             names.COEFFICIENT_PURCHARE, names.COEFFICIENT_SALES]
    data = dict.fromkeys(check, '')
    error = False
    for c in check:
        if args.get(c, None) is None:
            data[c] = 'Пустой параметр!'
            error = True
        else:
            data[c] = args[c]
    if error:
        return errors.logic, None
    provider = Provider()
    error, answer = provider.insert_quotation_history(args)
    if error == errors.OK:
        return errors.OK, answer
    return errors.logic, None

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

def get_graph(args):
    """
    Метод добавляет данные о котировках в момент времени
    :return:
    """
    check = [names.FROM, names.TO,
             names.ID_USER]
    data = dict.fromkeys(check, '')
    error = False
    for c in check:
        if args.get(c, None) is None:
            data[c] = 'Пустой параметр!'
            error = True
        else:
            data[c] = args[c]
    if error:
        return errors.logic, None
    provider = Provider()
    # print(args)
    error, answer = provider.get_graph(args)
    if error == errors.OK:
        return errors.OK, answer
    return errors.logic, None