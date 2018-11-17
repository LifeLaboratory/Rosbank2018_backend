import unittest
import requests as req
from cote.config.config import HOST
import cote.api.helpers.base_name as names
from cote.api.helpers.service import Gis
from cote.api.src.cote_method import quotation_user, get_quotation_actual, transaction


class TestQuotation(unittest.TestCase):
    def test_quotation_front(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/cote?Session=db09824d-ef98-6811-9a83-ce2ab340b240&Action=list")
        result = r.text
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
        r = s.get(HOST + "/api/v1/cote?Session=2dc503ef-72d0-8ad3-7876-b06ac05615a7")
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
        r = s.get(HOST + "/api/v1/cote?Session='2dc508ad3-7876-b06ac05615a7'")
        result = r.text
        self.assertFalse(Gis.converter(r.text).get("Name", None), None)
        self.assertFalse(Gis.converter(r.text).get("Currency", None), None)
        return

    def test_insert_quotation_history(self):
        s = req.Session()
        data = {names.ID_QUOTATION_FROM: 2, names.ID_QUOTATION_TO: 1, names.COST: 1.2,
             names.COEFFICIENT_PURCHARE: 0.2, names.COEFFICIENT_SALES: 0.1}
        r = s.post(HOST + '/api/v1/cote', data=data)
        result = Gis.converter(r.text)
        print(result)
        self.assertEqual(result.get(names.SESSION), None)
        return

    def test_list_quotation_user(self):
        s = req.Session()
        r = s.get(HOST + "/api/v1/cote?Session=2dc503ef-72d0-8ad3-7876-b06ac05615a7&Action=list")
        result = Gis.converter(r.text)
        self.assertTrue(result.get("Quotation", None), None)
        return

    def test_trans_sale_back(self):
        args = {
                names.ACTION: "sales",
                names.FROM: 1,
                names.TO: 2,
                names.COUNT_SEND: 0.001,
                names.ID_USER: 63
                }
        error, result = transaction(args)
        self.assertEqual(result.get(names.STATUS, None), 200)
        self.assertEqual(error, 200)
        return

    def test_trans_purchase_front(self):
        s = req.Session()
        args = {
            names.ACTION: "purchase",
            names.FROM: 1,
            names.TO: 2,
            names.COUNT_SEND: 0.001,
            names.SESSION: "7d8144e0-f15f-6b70-ab42-51da2f1a9d09"
        }
        r = s.post(HOST + '/api/v1/cote', data=args)
        result = Gis.converter(r.text)
        self.assertEqual(result.get(names.STATUS, None), 200)
        return

    def test_trans_sale_front(self):
        s = req.Session()
        args = {
            names.ACTION: "sale",
            names.FROM: 1,
            names.TO: 2,
            names.COUNT_SEND: 0.001,
            names.SESSION: "7d8144e0-f15f-6b70-ab42-51da2f1a9d09"
        }
        r = s.post(HOST + '/api/v1/cote', data=args)
        result = Gis.converter(r.text)
        self.assertEqual(result.get(names.STATUS, None), 200)
        return

    def test_get_graph(self):
        s = req.Session()
        data = {names.TO: 2, names.FROM: 1,
                names.SESSION: "2dc503ef-72d0-8ad3-7876-b06ac05615a7",
                names.ACTION: 'graph'}
        r = s.post(HOST + '/api/v1/cote', data=data)
        result = Gis.converter(r.text)
        # print(result)
        self.assertEqual(result.get(names.SESSION), None)
        return

if __name__ == '__main__':
    unittest.main()
