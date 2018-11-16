import auth.api.helpers.base_name as names
import auth.api.helpers.base_errors as errors
from auth.api.helpers.service import Sql


class Provider:
    def select_user(self, args):
        query = """
                    insert into "session"("session", "id_user", "id_company")
                    select md5(random()::text || clock_timestamp()::text)::uuid
                    , "id_user"
                    , "id_company"
                    from (
                      select (
                      select "id_user"
                      from "users"
                      where "login" = '{Login}'
                        and "password" = '{Password}'
                      limit 1
                      ) "id_user",
                      (
                      select "id_company"
                      from "company"
                      where "login" = '{Login}'
                        and "password" = '{Password}'
                      limit 1
                      ) "id_company"
                    ) nd
                    where "id_user" is not null or "id_company" is not null
                    returning "session" as "Session"
                """.format(Login=args[names.LOGIN], Password=args[names.PASSWORD])
        # print(query)
        try:
            auth_data = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if auth_data == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, auth_data[0]