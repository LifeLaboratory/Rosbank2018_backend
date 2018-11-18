import quotation.api.helpers.base_name as names
import quotation.api.helpers.base_errors as errors
from quotation.api.sql.quotation_provider import Provider
from time import sleep

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
    for data in check:
        if args.get(data, None) is None:
            data[data] = 'Пустой параметр!'
            error = True
        else:
            data[data] = args[data]
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
    print("ЦЕНА ПОКУПКИ КЛИЕНТА", check_cost[0]["cost"])
    if check_cost[1]["cost"] - (check_cost[0]["cost"]*float(args[names.COUNT_SEND])) >= 0:
        args[names.COST_USER] = check_cost[0]["cost"]
        args[names.COST_FROM] = check_cost[0]["cost"]*float(args[names.COUNT_SEND])
        check_action(args)
        error, result = provider.update_quotation_users(args)
        sleep(1)
        error, result = provider.insert_history_purchase(args)
        return error, result
    else:
        return errors.OK, {names.STATUS: errors.NO_BALANCE}

def check_action(args):
    if args.get(names.ACTION) == "purchase":
        args[names.COST_FROM], args[names.COUNT_SEND] = args[names.COUNT_SEND], args[names.COST_FROM]

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
        return errors.logic, errors.logic
    provider = Provider()
    # print(args)
    error, answer = provider.get_graph(args)
    if error == errors.OK:
        return errors.OK, answer
    return errors.logic, errors.logic