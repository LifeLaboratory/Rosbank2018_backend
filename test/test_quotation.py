import unittest
import requests as req
from quotation.config.config import HOST
import quotation.api.helpers.base_name as names
from quotation.api.helpers.service import Gis
from quotation.api.src.quotation_method import quotation_user, get_quotation_actual, transaction


class TestQuotation(unittest.TestCase):
    def test_quotation_front(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/quotation?Session=db09824d-ef98-6811-9a83-ce2ab340b240&Action=list")
        self.assertTrue(Gis.converter(r.text).get("Quotation", None), None)
        return

    def test_quotation_back(self):
        data = {
            names.ID_USER: 63
        }
        error, result = get_quotation_actual(data)
        self.assertTrue(result.get("Quotation", None), None)
        self.assertEqual(error, 200)
        return

    def test_quotation_cabinet_front(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/quotation?Session=2dc503ef-72d0-8ad3-7876-b06ac05615a7")
        result = r.text
        self.assertTrue(Gis.converter(r.text).get("Name", None), None)
        self.assertTrue(Gis.converter(r.text).get("Currency", None), None)
        return

    def test_quotation_cabinet_back(self):
        data = {
            names.ID_USER: 63
        }
        error, result = quotation_user(data)
        self.assertTrue(result.get("Name", None), "Оператор Борис")
        self.assertEqual(error, 200)
        return

    def test_quotation_cabinet_none(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/quotation?Session='2dc508ad3-7876-b06ac05615a7'")
        self.assertFalse(Gis.converter(r.text).get("Name", None), None)
        self.assertFalse(Gis.converter(r.text).get("Currency", None), None)
        return


    def test_list_quotation_user(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/quotation?Session=2dc503ef-72d0-8ad3-7876-b06ac05615a7&Action=list")
        result = Gis.converter(r.text)
        self.assertTrue(result.get("Quotation", None), None)
        return

    def test_trans_purchase_front(self):
        s = req.Session()
        args = {
            names.ACTION: "purchase",
            names.FROM: 2,
            names.TO: 1,
            names.COUNT_SEND: 1387500,
            names.SESSION: "7d8144e0-f15f-6b70-ab42-51da2f1a9d09",
            names.COST_USER: 10
        }
        r = s.post(HOST + '/api/v1/quotation', data=args)
        result = Gis.converter(r.text)
        self.assertEqual(result.get(names.STATUS, None), 200)
        return

    def test_trans_sale_front(self):
        s = req.Session()
        args = {
            names.ACTION: "sales",
            names.FROM: 1,
            names.TO: 2,
            names.COUNT_SEND: 0.0001,
            names.SESSION: "89a4ea52-c883-e1da-1e1e-f39469d7dfb1",
            names.COST_USER: 100
        }
        r = s.post(HOST + '/api/v1/quotation', data=args)
        result = Gis.converter(r.text)
        print(result)
        self.assertEqual(result.get(names.STATUS, None), 200)
        return

    def test_get_graph(self):
        s = req.Session()
        data = {names.TO: 2,
                names.FROM: 1,
                names.SESSION: "2dc503ef-72d0-8ad3-7876-b06ac05615a7",
                names.ACTION: 'graph'}
        r = s.post(HOST + '/api/v1/quotation', data=data)
        result = Gis.converter(r.text)
        # print(result)
        self.assertEqual(result.get(names.SESSION), None)
        return


if __name__ == '__main__':
    unittest.main()
