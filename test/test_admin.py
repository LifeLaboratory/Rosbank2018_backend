import unittest
import requests as req
from admin.config.config import HOST
import admin.api.helpers.base_name as names
from admin.api.src.admin_method import change_coefficient
from admin.api.helpers.service import Gis


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


if __name__ == '__main__':
    unittest.main()