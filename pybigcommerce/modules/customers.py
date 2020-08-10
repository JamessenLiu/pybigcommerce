
import json

from pybigcommerce.connector import Connection


class Customers(Connection):
    """Customers"""
    def create_customer_by_info(self, param: dict):
        url = "/customers"
        customer_group_id = int(param["customer_group_id"]) \
            if param.get("customer_group_id", None) is not None else None
        params = {
            'email': param["email"],
            'first_name': param["first_name"],
            'last_name': param["last_name"],
            "phone": param["phone"],
            "_authentication": {
                "force_reset": True,
            }
        }
        params = {k: v for k, v in params.items() if v is not None}
        if customer_group_id is not None:
            params.update({"customer_group_id": customer_group_id})
        resp = self.post_method(
            uri=url, data=json.dumps([params]), version="v3"
        )
        return resp

    def update_customer_info(self, param: dict):
        url = "/customers"
        customer_group_id = int(param.get("customer_group_id")) \
            if param.get("customer_group_id", None) is not None else None
        params = {
            "id": int(param["customer_id"]),
            'email': param.get("email", None),
            'first_name': param.get("first_name", None),
            'last_name': param.get("last_name", None),
            "phone": param.get("phone", None),
            "customer_group_id": customer_group_id
        }
        map(lambda x: params.pop(x) if params[x] is None else True,
            ["email", "first_name", "last_name", "phone", "customer_group_id"])
        resp = self.put_method(
            uri=url, data=json.dumps([params]), version="v3"
        )
        return resp

    def get_or_create_custom_attribute(self):
        uri = '/customers/attributes'
        resp = self.get_method(uri, None, 'v3')
        attr = next(
            (item for item in resp['data'] if item["name"] == "is_sales_rep"), None)
        if attr:
            return attr["id"]
        data = json.dumps([{
            "name": "is_sales_rep",
            "type": "number"
        }])
        resp = self.post_method(
            uri, data, 'v3'
        )
        return resp['data'][0]['id']

    def update_attr_value_by_id(self, attr_id, bc_user_id):
        uri = "/customers/attribute-values"
        data = json.dumps([{
            "attribute_id": attr_id,
            "value": "1",
            "customer_id": bc_user_id,
        }])
        return self.put_method(
            uri, data, 'v3'
        )

    def get_customer_info_by_email(self, email, version='v2'):
        uri = "/customers"
        resp = self.get_method(
           uri=uri, params={"email": email}, version=version
        )
        return resp

    def get_customer_by_id(self, customer_id, version='v2'):
        uri = f"/customers/{customer_id}"
        resp = self.get_method(
            uri=uri,
            version=version
        )
        return resp

    def update_customer_groups_to_catalog(
            self, customer_group_id, price_list_id, version="v2"):
        uri = "/customer_groups/{customer_group_id}".format(
            customer_group_id=customer_group_id)
        if price_list_id == "" or price_list_id is None:
            params = {
                "discount_rules": [],
            }
        else:
            params = {
                "discount_rules": [{
                    "type": "price_list",
                    "price_list_id": int(price_list_id),
                }],
            }
        resp = self.put_method(
            uri=uri,
            data=json.dumps(params),
            version=version
        )
        return resp

    def get_customer_by_customer_group_id(
            self, customer_group_id, page: int, result: list):

        url = "/customers"
        params = {
            "customer_group_id:in": int(customer_group_id),
            "page": page,
            "limit": 50
        }
        resp = self.get_method(
            uri=url, version="v3", params=params
        )
        if resp:
            total_pages = resp["meta"]["pagination"]["total_pages"]
            result.extend(resp["data"])
            if total_pages > page:
                return self.get_customer_by_customer_group_id(
                    customer_group_id=customer_group_id,
                    page=page + 1,
                    result=result)
            return result
        return False

    def delete_user_customer_group(self, customer_id, version="v2"):
        url = "/customers/{customer_id}".format(customer_id=customer_id)
        params = {
            "customer_group_id": 0
        }
        resp = self.put_method(
            uri=url, data=json.dumps(params), version=version
        )
        return resp

    def delete_customer_group(self, customer_group_id, version='v2'):

        url = f"/customer_groups/{customer_group_id}"

        resp = self.delete_method(
            uri=url, version=version)
        return resp

    def get_customer_groups_by_id(self, customer_group_id,  version="v2"):
        url = "/customer_groups/{customer_group_id}".format(
            customer_group_id=customer_group_id
        )
        resp = self.get_method(
            uri=url,
            version=version
        )
        return resp

    def get_customer_groups_total(self, **parameter):
        url = "/customer_groups"
        params = {
            "page": parameter["page"],
            "limit": parameter["limit"]
        }
        if parameter["q"] is not None and parameter["q"] != "":
            params.update({
                "name:like": parameter["q"]
            })
        resp = self.get_method(
            uri=url, params=params, version="v2"
        )
        if resp is False:
            return parameter["result"]
        parameter["result"].extend(resp)

        if len(resp) < parameter["limit"]:
            return parameter["result"]
        parameter["page"] = int(parameter["page"]) + 1
        return self.get_customer_groups_total(**parameter)

    def get_customer_groups_count(self,  version="v2"):
        url = "/customer_groups/count"
        resp = self.get_method(
            uri=url,
            version=version
        )
        if resp is False:
            result = {"code": "201", "data": {}}
        else:
            result = {"code": "200", "data": resp}

        return result

    def get_customer_groups_by_id_threading(self, params):
        bc_id = params["bc_id"]
        version = params["version"]
        company_id = params["company_id"]
        url = "/customer_groups/{customer_group_id}".format(
            customer_group_id=bc_id
        )
        resp = self.get_method(
            uri=url, version=version
        )
        if resp is False:
            return {"code": "201", "data": company_id}
        return {"code": "200", "data": resp}

    def create_customer_group(self, company_name, price_list_id=None, version='v2'):
        url = "/customer_groups"
        params = {
            "name": company_name
        }
        if price_list_id is not None:
            params["discount_rules"] = [
                {
                    "type": "price_list",
                    "price_list_id": price_list_id
                }
            ]
        resp = self.post_method(
            uri=url, data=json.dumps(params), version=version
        )
        if resp is False:
            result = {"code": "201", "data": {}}
        else:
            result = {"code": "200", "data": resp["id"]}
        return result

    def update_customer_group(self, customer_group_id, name, version="v2"):
        url = "/customer_groups/{customer_group_id}".format(
            customer_group_id=customer_group_id)
        params = {
            "name": name
        }
        resp = self.put_method(
            uri=url, data=json.dumps(params), version=version
        )
        if resp is False:
            result = {"code": "201", "data": {}}
        else:
            result = {"code": "200", "data": resp["id"]}
        return result

    def update_user_by_bc_id(self, bc_id,  customer_id, version="v3"):
        url = "/customers"
        params = {
            "customer_group_id": int(bc_id),
            "id": int(customer_id)
        }
        resp = self.put_method(
            uri=url, data=json.dumps([params]), version=version
        )

        if resp is False:
            result = {"code": "201", "data": {}}
        else:
            result = {"code": "200", "data": resp["data"][0]["id"]}

        return result

    def update_customer_infos(self, **params):
        url = "/customers"
        _params = {
            "customer_group_id": int(params["bc_id"]),
            "id": int(params["customer_id"]),
            'email': params["email"],
            'first_name': params["first_name"],
            'last_name': params["last_name"],
            "phone": params["phone"],
        }
        _params = {k: v for k, v in _params.items() if v is not None}
        version = "v3"
        resp = self.put_method(
            uri=url, data=json.dumps([_params]), version=version
        )
        return resp

    def get_customer_group_by_name(self, name, version='v2'):
        url = "/customer_groups"
        params = {
            "name": name
        }
        resp = self.get_method(
            uri=url,
            params=params,
            version=version
        )
        return resp

    def get_customer_groups(self, **parameter):
        url = "/customer_groups"
        params = {
            "page": parameter["page"],
            "limit": parameter["limit"]
        }
        if parameter["q"] is not None and parameter["q"] != "":
            params.update({
                "name:like": parameter["q"]
            })
        resp = self.get_method(
            uri=url,  params=params, version="v2"
        )
        if resp is False:
            return []
        return resp
