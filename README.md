# Odoo API Calls
***


### Get all Categories:
URL: /categories
Method: GET
Description: This endpoint gives a list of all categories available in Odoo database

Response:
```json
[
    {
        "id": 3,
        "name": "Agua",
        "parent_id": 1
    },
    {
        "id": 1,
        "name": "All",
        "parent_id": null
    }
]
```


### Get specific category:
URL: /categories/<categ_id>
Method: GET
Description: This endpoint gives details of a specific category in a json object

Response:
```json
    {
        "id": 3,
        "name": "Agua",
        "parent_id": 1
    }
```




### Get all products linked to a category:
URL: /categories/<categ_id>/products
Method: GET
Description: This endpoint gives a list of all products assocuated with the secific "categ_id" in Odoo database

Response:
```json
[
    {
        "pack_stock_management": "decrmnt_products",
        "is_pack": null,
        "formato_peq": null,
        "agua": null,
        "categ_id": 1,
        "name": "SERVICIOS DE NOTARIOS",
        "type": "service",
        "list_price": "1.00",
        "description": null,
        "id": 10,
        "template_id": 10,
        "ean13": null,
        "default_code": null,
        "pack_items": [],
        "image_url": "http://gestiontest.fontoasis.es/website/image/product.template/10/image_medium"
    },
    {
        "pack_stock_management": "decrmnt_products",
        "is_pack": null,
        "formato_peq": null,
        "agua": null,
        "categ_id": 1,
        "name": "SERVICIOS DE NOTARIOS",
        "type": "service",
        "list_price": "1.00",
        "description": null,
        "id": 10,
        "template_id": 10,
        "ean13": null,
        "default_code": null,
        "pack_items": [],
        "image_url": "http://gestiontest.fontoasis.es/website/image/product.template/10/image_medium"
    }
]
```

### Get All Products:
URL: /products
Method: GET
Description: This endpoint gives details of all products in a list of json object present in Odoo

Response:
```json
[
    {
        "pack_stock_management": "decrmnt_products",
        "is_pack": null,
        "formato_peq": null,
        "agua": null,
        "categ_id": 1,
        "name": "SERVICIOS DE NOTARIOS",
        "type": "service",
        "list_price": "1.00",
        "description": null,
        "id": 10,
        "template_id": 10,
        "ean13": null,
        "default_code": null,
        "pack_items": [],
        "image_url": "http://gestiontest.fontoasis.es/website/image/product.template/10/image_medium"
    },
    {
        "pack_stock_management": "decrmnt_products",
        "is_pack": null,
        "formato_peq": null,
        "agua": null,
        "categ_id": 1,
        "name": "SERVICIOS DE NOTARIOS",
        "type": "service",
        "list_price": "1.00",
        "description": null,
        "id": 10,
        "template_id": 10,
        "ean13": null,
        "default_code": null,
        "pack_items": [],
        "image_url": "http://gestiontest.fontoasis.es/website/image/product.template/10/image_medium"
    }
]
```

### Get specific product:
URL: /products/<prod_id>
Method: GET
Description: This endpoint gives details of a specifc products in a list of json object present in Odoo

Response:
```json
[
    {
        "pack_stock_management": "decrmnt_products",
        "is_pack": null,
        "formato_peq": null,
        "agua": null,
        "categ_id": 1,
        "name": "SERVICIOS DE NOTARIOS",
        "type": "service",
        "list_price": "1.00",
        "description": null,
        "id": 10,
        "template_id": 10,
        "ean13": null,
        "default_code": null,
        "pack_items": [],
        "image_url": "http://gestiontest.fontoasis.es/website/image/product.template/10/image_medium"
    }
]
```


### Authenticate a User:
URL: /authenticate
Method: POST
Input: ```json{"username": <username>, "password": <password>}```
Description: This endpoint authenticates the user with given credentials.

Success Response:
```json
{"status": "success", "user_id": <uid>}
```
In case of failure:
```json
{"status": "fail", "user_id": False}
```


### Get user details:
URL: /users/<uid>
Method: GET
Description: This endpoint gives user's details available in Odoo database

Success Response:
```json
{
    "id": 1,
    "partner_id": 3,
    "login": "admin",
    "company_id": 1,
    "signature": "<span>--<br>\nAdministrator</span>",
    "alias_id": 1,
    "website": null,
    "street": null,
    "street2": null,
    "city": null,
    "zip": null,
    "email": "m.alzanillas@zclick.es",
    "phone": null,
    "mobile": null
}
```


### Get user's order details:
URL: /users/<uid>/orders
Method: GET
Description: This endpoint gives a list of all the orders for a specifc user available in Odoo database

Success Response:
```json
[
    {
        "id": 21903,
        "origin": null,
        "date_order": "07/02/2019, 07:56:05",
        "picking_policy": "direct",
        "create_uid": 1,
        "partner_id": 3,
        "client_order_ref": null,
        "note": null,
        "partner_invoice_id": 3,
        "amount_untaxed": "1.00",
        "partner_shipping_id": 3,
        "create_date": "07/02/2019, 07:56:20",
        "company_id": 1,
        "amount_tax": "0.21",
        "payment_term": null,
        "carrier_id": null,
        "amount_total": "1.21",
        "name": "SO6868",
        "state": "draft",
        "user_id": 1,
        "line_data": [
            {
                "product_uom": 1,
                "sequence": 10,
                "price_unit": "1.00",
                "product_uom_qty": "1.000",
                "invoiced": false,
                "id": 28597,
                "order_id": 21903,
                "discount": "0.00",
                "product_id": 50,
                "name": "ANALISIS AGUA"
            }
        ]
    }
]
```


### Reset user password:
URL: /users/<uid>/reset-pass
Method: POST
Input: ```json{"username": <uname>, "password": <password>}```
Description: This endpoint will reset user's password.

Success Response:
```json
{"status": "success", "description": "Password updated!"}
```
Failure response:
```json
{"status": "fail"}
```


### Get user's visits details:
URL: /users/<uid>/visits
Method: GET
Description: This endpoint gives a list of all the orders for a specifc user available in MySQL database

Success Response:
```json
[
    {
        "id": 676,
        "visit_type_id": 1,
        "route_id": 10,
        "visit_date": "09/07/2016",
        "important": 0,
        "cliente": "A02683",
        "visit_status_id": null,
        "status_date": null,
        "driver_id": null,
        "comments": null,
        "cleaning": 0,
        "created": null,
        "creator": null,
        "agua": 1,
        "higiene": 0,
        "averia": 0,
        "formato_peq": 0,
        "agua_unserviced": null,
        "higienes_unserviced": 0,
        "fpeq_unserviced": null,
        "is_partial": null
    },
    {
        "id": 890,
        "visit_type_id": 1,
        "route_id": 21,
        "visit_date": "09/09/2016",
        "important": 1,
        "cliente": "A02683",
        "visit_status_id": 4,
        "status_date": "09/09/2016, 09:42:08",
        "driver_id": 6,
        "comments": "",
        "cleaning": 0,
        "created": "09/08/2016, 08:59:51",
        "creator": "admin-individual-JavierFont",
        "agua": 1,
        "higiene": 0,
        "averia": 0,
        "formato_peq": 0,
        "agua_unserviced": null,
        "higienes_unserviced": 0,
        "fpeq_unserviced": null,
        "is_partial": null
    }
]
```


### Get specific order detail:
URL: /orders/<order_id>
Method: GET
Description: This endpoint gives details of a specifc order in a json object present in Odoo

Response:
```json
{
        "id": 21903,
        "origin": null,
        "date_order": "07/02/2019, 07:56:05",
        "picking_policy": "direct",
        "create_uid": 1,
        "partner_id": 3,
        "client_order_ref": null,
        "note": null,
        "partner_invoice_id": 3,
        "amount_untaxed": "1.00",
        "partner_shipping_id": 3,
        "create_date": "07/02/2019, 07:56:20",
        "company_id": 1,
        "amount_tax": "0.21",
        "payment_term": null,
        "carrier_id": null,
        "amount_total": "1.21",
        "name": "SO6868",
        "state": "draft",
        "user_id": 1,
        "line_data": [
            {
                "product_uom": 1,
                "sequence": 10,
                "price_unit": "1.00",
                "product_uom_qty": "1.000",
                "invoiced": false,
                "id": 28597,
                "order_id": 21903,
                "discount": "0.00",
                "product_id": 50,
                "name": "ANALISIS AGUA"
            }
        ]
    }
```


### Create order in odoo with visit in MySQL:
URL: /create-order
Method: POST
Description: This endpoint creates a order in odoo with input given and also creates a visit in MySQL db.
Input: Input is a valid json object with missing field info available in response in case of failure:

Sample:
```json
{
  "partner_id": 10,
  "partner_invoice_id": 36,
  "partner_shipping_id": 36,
  "pricelist_id": 1,
  "order_line": [{"name":"Laptop E5023", "product_uom_qty": 1.0, "price_unit": 20.0, "product_id": 33, "product_uom":1 ,"tax_id": 1, "is_pack": 0}],
  "visit": {"higiene": 1}
}
```
visit is optional to update any visit column.


Response:
```json
{"status": "sucess", "order_id": <order_id>}
```
