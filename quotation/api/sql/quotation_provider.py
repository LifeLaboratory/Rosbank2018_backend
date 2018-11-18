import quotation.api.helpers.base_name as names
import quotation.api.helpers.base_errors as errors
from quotation.api.helpers.service import Sql


class Provider:
    """
    Провайдер для работы с котировками
    """

    @staticmethod
    def select_user_name(args):
        """
        По ID пользователя получает его имя
        :param args:
        :return: dict
        """
        query = """
  select Name
  from users
  where id_user = {}
                    """.format(args['id_user'])
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result[0]

    @staticmethod
    def select_quotation_user(args):
        """
        По ID пользователя получает все его деньги по валютам
        :param args:
        :return:
        """
        query = """
select
 id_quotation as id_currency
 , name as Name_currency
 , cost::double precision
from quotation q
left join (
  select *
  from quotation_users
  where id_user = {}
) qu using(id_quotation)
                """.format(args['id_user'])
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result

    @staticmethod
    def insert_quotation_history(args):
        """
        Добавить данные по котировкам в историю
        :param args:
        :return:
        """
        query = """
with 
  _names as (
    select q1.name || '/' || q2.name as name
    from quotation q1, quotation q2
    where q1.id_quotation = {id_quotation_from} 
      and q2.id_quotation = {id_quotation_to}
    limit 1
  )
insert into quotation_history(id_quotation_to, id_quotation_from, cost, 
name, coefficient_sales, coefficient_purchare, quant, reserve) 
values ({id_quotation_to}, {id_quotation_from}, {cost}::numeric(32, 6), (select name from _names), 
{coefficient_sales}, {coefficient_purchare}, now(), 0.0)
returning id_quotation_to""".format(**args)
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, {'quotation': result}

    @staticmethod
    def select_quotation_actual(user_data):
        """
        Получает актуальные данные по котировкам
        :param args:
        :return:
        """
        query = """
with 
  _pack as (
    select pack + rating as "pack"
    from users
    where id_user = {}
    limit 1
  )
select 
  id_quotation_to
  , id_quotation_from
  , Name as "Name"
  , (cost + coefficient_sales +reserve+ (select pack from _pack))::double precision as "Count_sale"
  , (cost + coefficient_purchare +reserve+ (select pack from _pack))::double precision as "Count_purchare"
from quotation_trade
                """.format(user_data.get('id_user'))
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, {'Quotation': result}

    @staticmethod
    def insert_history_sale(args):
        """
        Добавляет запись в историю при продаже
        :param args:
        :return:
        """
        query = """
with quot as (
select 
(   {cost_user} + "coefficient_sales" + reserve + (select "pack" + rating from users where "id_user" = {id_user}))::double precision as "cost" 
    ,"cost" as "cost_bank"
    , "name"
    , "coefficient_sales" as "coefficient"
from quotation_trade
    where "id_quotation_from" = {id_quotation_from} and "id_quotation_to" = {id_quotation_to}
)

insert into history_billing("id_user", "id_quotation_from", "id_quotation_to", "cost", "cost_bank", "name", 
"coefficient", "quant", "count_send")
select 
{id_user}
, {id_quotation_from}
, {id_quotation_to}
, "cost"
, "cost_bank"
, "name"
, "coefficient"
, now()
, {count_send}
from quot
returning 200 as "Status"
        """.format(id_user=args[names.ID_USER],
                   id_quotation_from=args[names.FROM],
                   id_quotation_to=args[names.TO],
                   count_send=args[names.COUNT_SEND],
                   cost_user=args[names.COST_USER])
        try:
            # print(query)
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result[0]

    @staticmethod
    def insert_history_purchase(args):
        """
        Добавляет запись в историю при продаже
        :param args:
        :return:
        """
        if args[names.ACTION] == "sales":
            action = '+'
        elif args[names.ACTION] == "purchase":
            action = '-'
        query = """
with quot as (
select 
(   "cost" {action} "coefficient_sales" + reserve {action} (select "pack" + rating from users where "id_user" = {id_user}))::double precision as "cost" 
    ,"cost" as "cost_bank"
    , "name"
    , "coefficient_sales" as "coefficient"
from quotation_trade
    where "id_quotation_from" = {id_quotation_from} and "id_quotation_to" = {id_quotation_to}
)

insert into history_billing("id_user", "id_quotation_from", "id_quotation_to", "cost", "cost_bank", "name", 
"coefficient", "quant", "count_send")
select 
{id_user}
, {id_quotation_from}
, {id_quotation_to}
, {cost_user}
, "cost_bank"
, "name"
, "coefficient"
, now()
, {count_send}
from quot
returning 200 as "Status"
            """.format(id_user=args[names.ID_USER], id_quotation_from=args[names.FROM], id_quotation_to=args[names.TO],
                   count_send=args[names.COUNT_SEND], action=action, cost_user=args[names.COST_USER])
        try:
            # print(query)
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result[0]

    @staticmethod
    def check_cost_user(args):
        """
        Получает количество валюты на балансе
        :param args:
        :return:
        """
        query = """
select "cost" from quotation_users 
    where id_user = {id_user} and id_quotation = {id_quotation}
union
select 
    (  {cost_user} + "coefficient_sales" + (select "pack" from users where "id_user" = {id_user}))::double precision as "cost" 
    from quotation_trade
        where "id_quotation_from" = {id_quotation} and "id_quotation_to" = {id_quotation_to}
        """.format(id_user=args[names.ID_USER],
                   id_quotation=args[names.FROM],
                   id_quotation_to=args[names.TO],
                   cost_user=args[names.COST_USER])
        try:
            # print(query)
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result

    @staticmethod
    def update_quotation_users(args):
        """
        Получает количество валюты на балансе
        :param args:
        :return:
        """
        if args[names.ACTION] == "purchase":
            query = """
            update quotation_users
            set "cost" = "cost" - {cost_from}
            where id_user = {id_user} and id_quotation = {id_quotation_from};
            update quotation_users
            set "cost" = "cost" + {count_send}
            where id_user = {id_user} and id_quotation = {id_quotation_to};
                        """.format(id_user=args[names.ID_USER], id_quotation_from=args[names.FROM],
                                   count_send=args[names.COUNT_SEND],
                                   id_quotation_to=args[names.TO], cost_from=args[names.COST_FROM])
        if args[names.ACTION] == "sales":
            query = """
    update quotation_users
    set "cost" = "cost" - {cost_user}
    where id_user = {id_user} and id_quotation = {id_quotation_from};
    update quotation_users
    set "cost" = "cost" + {count_send}
    where id_user = {id_user} and id_quotation = {id_quotation_to};
                """.format(id_user=args[names.ID_USER], id_quotation_from=args[names.FROM], count_send=args[names.COUNT_SEND],
                           id_quotation_to=args[names.TO], cost_user=args[names.COST_USER])
        try:
            # print(query)
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        if result == errors.SQL_ERROR:
            return errors.SQL_ERROR, None
        else:
            return errors.OK, result

    @staticmethod
    def get_graph(user_data):
        """
        Получает актуальные данные по котировкам
        :param args:
        :return:
        """
        query = """
with 
  _pack as (
    select pack + rating as "pack"
    from users
    where id_user = {}
    limit 1
  )
select 
  Quant::text as "Quant"
  , cost::double precision as "Cost"
  , (cost + coefficient_sales + reserve + (select pack from _pack))::double precision as "Cost_sale"
  , (cost - coefficient_purchare + reserve - (select pack from _pack))::double precision as "Cost_purchase"
from quotation_history
where id_quotation_to = {} and id_quotation_from = {}
order by quant desc
limit 250
                """.format(user_data.get('id_user'), user_data.get('From'), user_data.get('To'))
        # print(query)
        try:
            result = Sql.exec(query=query)
        except:
            return errors.SQL_ERROR, None
        return errors.OK, {'Quotation': result}
