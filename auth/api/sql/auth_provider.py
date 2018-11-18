import auth.api.helpers.base_name as names
import auth.api.helpers.base_errors as errors
from auth.api.helpers.service import Sql


class Provider:
    def select_user(self, args):
        if args[names.PAGE] == "client":
            args[names.PAGE] = 0
        if args[names.PAGE] == "employee":
            args[names.PAGE] = 1
        query = """
                    insert into "session"("session", "id_user")
                    select md5(random()::text || clock_timestamp()::text)::uuid
                    , "id_user"
                    from (
                      select (
                      select "id_user"
                      from "users"
                      where "login" = '{Login}'
                        and "password" = '{Password}'
                        and "privilege" = {Pages}
                      limit 1
                      ) )"id_user"
                    where "id_user" is not null
                    returning "session" as "Session"
                """.format(Login=args[names.LOGIN], Password=args[names.PASSWORD], Pages=args[names.PAGE])
        # print(query)
        try:
            auth_data = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if auth_data == errors.SQL_ERROR or auth_data[0] is None:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, auth_data[0]

    def select_status_user(self, args):
        query = """
  select "status_pack"
  from "users"
  where "id_user" = (select id_user from session where session = '{Session}')
                """.format(**args)
        # print(query)
        try:
            auth_data = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if auth_data == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, auth_data[0]

