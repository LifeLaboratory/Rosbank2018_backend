import time
import random
import requests
from quotation.api.helpers.service import Sql
HOST = 'http://127.0.0.1:13452/api/v1/quotation'


def select_pair_quotation():
    sql = """
select id_quotation_to
  , id_quotation_from
  , cost::double precision
  , name
  , coefficient_purchare
  , coefficient_sales
from quotation_trade qt
    """
    pairs = Sql.exec(query=sql)
    answer = {}
    for pair in pairs:
        answer[(pair['id_quotation_to'], pair['id_quotation_from'])] = pair
    return answer


def send_post(rs):
    for rec in rs:
        requests.post(HOST, data=rec)


def generate_tick(pairs):
    for j in range(1000):
        count = random.randint(1, 5)
        _key = list(pairs.keys())
        rs = []
        for i in range(count):
            key = _key[random.randint(0, len(_key) - 1)]
            zn = 1 if random.randint(0, 1) else -1
            pairs[key]['cost'] = float(pairs[key]['cost']) + (random.randint(0, 10) / 100000) * zn
            temp = {
                'id_quotation_to': pairs[key]['id_quotation_to'],
                'id_quotation_from': pairs[key]['id_quotation_from'],
                'cost': pairs[key]['cost'],
                'name': pairs[key]['name'],
                'coefficient_sales': pairs[key]['coefficient_sales'],
                'coefficient_purchare': pairs[key]['coefficient_purchare']
            }
            rs.append(temp)
        # print(rs)
        # send_post(rs)
        print(pairs[(2, 1)])
        # time.sleep(1)


pairs = select_pair_quotation()
generate_tick(pairs)