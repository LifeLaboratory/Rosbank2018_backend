import auth.api.helpers.base_name as names
import auth.api.helpers.base_errors as errors
from auth.api.helpers.service import Sql


class Provider:
    def select_user(self, args):
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
            data = Sql.exec(query=query)
        except:
            return 500, None
        if data == 500 or data[0] is None:
            return 500, None
        else:
            return errors.OK, data[0]

    def select_status_user(self, args):
        query = """
  select "status_pack"
  from "users"
  where "id_user" = (select id_user from session where session = '{Session}')
                """.format(**args)
        # print(query)
        try:
            data = Sql.exec(query=query)
        except:
            return 500, None
        if data == 500:
            return 500, None
        else:
            return errors.OK, data[0]

