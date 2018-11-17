import unittest
import requests as req
from quotation.config.config import HOST
import quotation.api.helpers.base_name as names
from auth.api.src.Authentication import auth
from quotation.api.helpers.service import Gis


class TestAuth(unittest.TestCase):
    def test_auth_back(self):
        data = {
                names.LOGIN: 'boris',
                names.PASSWORD: 'boris'
                }
        result = auth(data)
        self.assertEqual(result[0], 200)
        self.assertTrue(result[1], None)
        return

    def test_quotation_front(self):
        s = req.Session()
        r = s.get(HOST + '/api/v1/quotation')
        result = r.text
        # self.assertTrue(result.get(names.SESSION, None), None)
        return

    def test_quotation_cabinet_front(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/quotation?Session='2dc503ef-72d0-8ad3-7876-b06ac05615a7'")
        result = r.text
        print(result)
        # self.assertTrue(result.get(names.SESSION, None), None)
        return

    def test_auth_none(self):
        s = req.Session()
        data = {names.LOGIN: 'boris'}
        r = s.post(HOST + '/api/v1/auth', data=data)
        result = Gis.converter(r.text)
        self.assertEqual(result.get(names.SESSION), None)
        return

    def test_insert_quotation_history(self):
        s = req.Session()
        data = {names.ID_QUOTATION_FROM: 2, names.ID_QUOTATION_TO: 1, names.COST: 1.2,
             names.COEFFICIENT_PURCHARE: 0.2, names.COEFFICIENT_SALES: 0.1}
        r = s.post(HOST + '/api/v1/quotation', data=data)
        result = Gis.converter(r.text)
        print(result)
        self.assertEqual(result.get(names.SESSION), None)
        return


if __name__ == '__main__':
    unittest.main()
