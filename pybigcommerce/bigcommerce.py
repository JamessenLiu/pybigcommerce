from pybigcommerce.modules.customers import Customers
from pybigcommerce.modules.store_info import StoreInfo


class BigCommerceModel:

    def __init__(self, store_hash, access_token):
        self.customer = Customers(store_hash, access_token)
        self.store_info = StoreInfo(store_hash, access_token)






