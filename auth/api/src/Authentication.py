import auth.api.helpers.base_name as names
import auth.api.helpers.base_errors as errors
from auth.api.sql.auth_provider import Provider


def check_data(data):
    check = [names.LOGIN, names.PASSWORD, names.PAGE]
    check_data = dict.fromkeys(check, '')
    error = False
    for c in check:
        if data.get(c, None) is None:
            check_data[c] = 'Пустой параметр!'
            error = True
        else:
            check_data[c] = data[c]
    if error:
        return 400, None
    if check_data[names.PAGE] == "client" or check_data[names.PAGE] == "employee":
        if check_data[names.PAGE] == "client":
            check_data[names.PAGE] = 0
        if check_data[names.PAGE] == "employee":
            check_data[names.PAGE] = 1
    else:
        return 400, None
    return 200, check_data


def auth(data):
    status_code, data = check_data(data)
    if status_code == 400:
        return 400, None
    provider = Provider()
    status_code, answer = provider.select_user(data)
    # status_code, status = provider.select_status_user(answer)
    # answer['Status_pack'] = status.get('status_pack', 'Стандарт')
    if status_code == 200:
        return 200, answer
    return 500, None
