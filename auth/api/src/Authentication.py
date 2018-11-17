import auth.api.helpers.base_name as names
import auth.api.helpers.base_errors as errors
from auth.api.sql.auth_provider import Provider


def auth(user_data):
    check = [names.LOGIN, names.PASSWORD, names.PAGE]
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
    error, answer = provider.select_user(auth_data)
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None


