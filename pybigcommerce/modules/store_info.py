
from pybigcommerce.connector import Connection


class StoreInfo(Connection):
    """
        StoreInfo
    """

    def get_store_info(self, version="v2"):

        url = "/store"
        resp = self.get_method(
            uri=url,
            version=version
        )
        return resp

    def get_currency(self, version="v2"):

        url = "/currencies"
        resp = self.get_method(
            uri=url,
            version=version
        )
        return resp

    def get_counties(self, country_name, version="v2"):

        url = "/countries"
        resp = self.get_method(
            uri=url,
            version=version,
            params={
                "country": country_name
            }
        )
        return resp

    def get_state(self, country_id, state, version="v2"):

        url = f"countries/{country_id}/states"
        resp = self.get_method(
            uri=url,
            version=version,
            params={
                "state": state
            }
        )
        return resp

    def __str__(self):
        return "StoreInfo"
