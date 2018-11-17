import admin.api.helpers.base_name as names
import admin.api.helpers.base_errors as errors
from admin.api.sql.admin_provider import Provider


def change_coefficient(args):
    """
    Метод по связке id валют изменяет коэффициенты котировок
    :param args:
    :return:
    """
    check = [names.ID_QUOTATION_TO, names.ID_QUOTATION_FROM,
             names.COEFFICIENT_SALES, names.COEFFICIENT_PURCHARE]
    data = dict.fromkeys(check, '')
    if args.get(names.ID_QUOTATION_TO, None) is None or args.get(names.ID_QUOTATION_FROM, None) is None or \
            args.get(names.COEFFICIENT_SALES, None) and args.get(names.COEFFICIENT_PURCHARE, None):
        return errors.CHANGE_COEFF, {"Status": errors.CHANGE_COEFF}
    for c in check:
        if args.get(c, None) is None:
            data[c] = None
        else:
            data[c] = args[c]
    provider = Provider()
    error, answer = provider.change_coefficients(data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.CHANGE_COEFF, {"Status": errors.CHANGE_COEFF}


def change_pack(args):
    """
    Метод ручного изменения пакета пользователя
    :param args:
    :return:
    """
    check = [names.ID_USER, names.PACK]
    data = dict.fromkeys(check, '')
    if args.get(names.ID_USER, None) is None or args.get(names.PACK, None) is None:
        return errors.CHANGE_PACK, {"Status": errors.CHANGE_PACK}
    for c in check:
        if args.get(c, None) is None:
            data[c] = None
        else:
            data[c] = args[c]
    provider = Provider()
    error, answer = provider.change_pack(data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.CHANGE_PACK, {"Status": errors.CHANGE_PACK}
