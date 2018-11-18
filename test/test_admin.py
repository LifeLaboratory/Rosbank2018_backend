import unittest
import requests as req
from admin.config.config import HOST
from admin.api.src.admin_method import *
from admin.api.helpers.service import Gis
import admin.api.helpers.base_name as names


class TestAdmin(unittest.TestCase):
    def test_change_coefficients_back_sales(self):
        args = {
                names.ID_QUOTATION_FROM: 1,
                names.ID_QUOTATION_TO: 3,
                names.COEFFICIENT_SALES: 0.001,
                }
        result = change_coefficient(args)
        self.assertEqual(result[0], 200)
        self.assertTrue(result[1][names.STATUS], 200)

        return

    def test_change_coefficients_back_purchase(self):
        args = {
                names.ID_QUOTATION_FROM: 1,
                names.ID_QUOTATION_TO: 3,
                names.COEFFICIENT_PURCHARE: 0.001
                }
        result = change_coefficient(args)
        self.assertEqual(result[0], 200)
        self.assertTrue(result[1][names.STATUS], 200)

        return

    def test_change_coefficients_back_sale_purchase(self):
        args = {
                names.ID_QUOTATION_FROM: 1,
                names.ID_QUOTATION_TO: 3,
                names.COEFFICIENT_SALES: 0.001,
                names.COEFFICIENT_PURCHARE: 0.001
                }
        result = change_coefficient(args)
        self.assertEqual(result[0], 108)
        self.assertTrue(result[1][names.STATUS], 108)

        return

    def test_change_coefficients_front_sales(self):
        s = req.Session()
        args = {
            names.ID_QUOTATION_FROM: 1,
            names.ID_QUOTATION_TO: 3,
            names.COEFFICIENT_SALES: 0.001,
        }
        r = s.post(HOST + '/api/v1/admin', data=args)
        result = Gis.converter(r.text)
        self.assertEqual(result, 200)

        return

    def test_change_coefficients_front_purchase(self):
        s = req.Session()
        args = {
            names.ID_QUOTATION_FROM: 1,
            names.ID_QUOTATION_TO: 3,
            names.COEFFICIENT_PURCHARE: 0.001,
        }
        r = s.post(HOST + '/api/v1/admin', data=args)
        result = Gis.converter(r.text)
        self.assertEqual(result, 200)

        return

    def test_change_coefficients_front_sale_purchase(self):
        s = req.Session()
        args = {
            names.ID_QUOTATION_FROM: 1,
            names.ID_QUOTATION_TO: 3,
            names.COEFFICIENT_PURCHARE: 0.001,
            names.COEFFICIENT_SALES: 0.001
        }
        r = s.post(HOST + '/api/v1/admin', data=args)
        result = Gis.converter(r.text)
        self.assertEqual(result, 109)

        return

    def test_change_pack_back(self):
        args = {
                names.ID_USER: 63,
                names.PACK: 0.005
                }
        result = change_pack(args)
        self.assertEqual(result[0], 200)
        self.assertTrue(result[1][names.STATUS], 200)

        return

    def test_change_pack_front(self):
        s = req.Session()
        args = {
            names.ID_USER: 63,
            names.PACK: 0.005
        }
        r = s.post(HOST + '/api/v1/admin', data=args)
        print(r.text)
        result = Gis.converter(r.text)
        self.assertEqual(result, 200)

    def test_change_status_pack(self):
        s = req.Session()
        args = {
            names.ID_USER: 64,
            names.STATUS_PACK: "Стандарт"
        }
        r = s.post(HOST + '/api/v1/admin', data=args)
        print(r.text)
        result = Gis.converter(r.text)
        self.assertEqual(result, 200)

    def test_list_users(self):
        s = req.Session()
        r = s.get(HOST + '/api/v1/admin?Action=list')
        result = Gis.converter(r.text)
        print(result)
        self.assertTrue(result, None)


if __name__ == '__main__':
    unittest.main()
