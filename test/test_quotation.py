import unittest
import requests as req
from auth.config.config import HOST
import auth.api.helpers.base_name as names
from auth.api.src.Authentication import auth
from auth.api.helpers.service import Gis


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

    def test_auth_none(self):
        s = req.Session()
        data = {names.LOGIN: 'boris'}
        r = s.post(HOST + '/api/v1/auth', data=data)
        result = Gis.converter(r.text)
        self.assertEqual(result.get(names.SESSION), None)
        return


if __name__ == '__main__':
    unittest.main()
