import unittest
from pybigcommerce.bigcommerce import BigCommerceModel


class BigcommerceTest(unittest.TestCase):

    bc = BigCommerceModel(store_hash="abcdef", access_token="qwertyuiop")

    def test_get_customer(self):
        self.assertIsNotNone(self.bc.customer.get_customer_by_id(1))

    def test_get_store_info(self):
        self.assertIsNotNone(self.bc.store_info.get_store_info())
