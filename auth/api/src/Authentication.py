import auth.api.helpers.base_name as names
import auth.api.helpers.base_errors as errors
from auth.api.sql.auth_provider import Provider


def auth(user_data):
    check = [names.LOGIN, names.PASSWORD, names.PAGE]
    auth_data = dict.fromkeys(check, '')
    error = False
    for c in check:
        if user_data.get(c, None) is None:
            auth_data[c] = 'Пустой параметр!'
            error = True
        else:
            auth_data[c] = user_data[c]
    if error:
        return errors.AUTH_FAILED, None
    provider = Provider()
    error, answer = provider.select_user(auth_data)
    error, status = provider.select_status_user(answer)
    answer['Status_pack'] = status.get('status_pack', 'Стандарт')
    if error == errors.OK:
        return errors.OK, answer
    return errors.AUTH_FAILED, None
