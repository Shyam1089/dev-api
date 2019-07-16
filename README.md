# Odoo API Calls
***


### Authenticate a User:
URL: /authenticate
Method: POST
Headers: ```json{
    'content-type': 'application/json'
}```
Input: ```json {"username": username, "password": password}```
Description: This endpoint authenticates the user with given credentials and returns back an auth token which is to be passed in header under 'Authorization' key.

Success Response:
```json
{
    "status": "success",
    "user_id": 1,
    "token": "eyJhbGci..............k4Q5WresvNWvQ"
}
```
In case of failure:
```json
{"status": "fail", "user_id": False}
```


### Get user details:
URL: /user
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
Description: This endpoint gives user's details available in Odoo database. User ID will be computed from the Auth token passed in header.

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
URL: /user/orders
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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


### Get user address details:
URL: /user/address
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
Description: This endpoint gives user's address details available in Odoo database

Success Response:
```json
{
    "id": 1,
    "partner_id": 3,
    "status": "success",
    "address": [
        {
            "id": 12327,
            "name": "str test",
            "type": "contact",
            "function": "reception",
            "street": "street",
            "street2": "street",
            "city": "Madrid",
            "zip":  201301,
            "email": "test@test",
            "phone": "12345",
            "mobile": "12345"
        }
    ]
}
```


### Create user address details:
URL: /user/create-address
Method: POST
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
Description: This endpoint creates a new address in Odoo

Input Response:
```json
{
    "name": "str test",
    "function": "reception",
    "street": "street",
    "street2": "street",
    "city": "Madrid",
    "zip":  201301,
    "email": "test@test",
    "phone": "12345",
    "mobile": "12345"
}
```


Success Response:
```json
{
    "id": 20,
    "partner_id": 1872,
    "status": "success",
    "address_id": 12335
}
```
"id" - > userID
"partner_id" - > related PartnerID
"address_id" - > newly created Address


### Reset user password:
URL: /user/reset-pass
Method: POST
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
Input: ```json{"password": "passowrd"}```
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
URL: /user/visits
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


### Get all Categories:
URL: /categories
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```

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
URL: /categories/{categ_id}
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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
URL: /categories/{categ_id}/products
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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
URL: /products/{prod_id}
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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


### Get specific order detail:
URL: /orders/{order_id}
Method: GET
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
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
{"status": "sucess", "order_id": 123}
```



### Search a Partner ID:
URL: /get-partner
Method: POST
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
Input: ```json {"tin": vat number}```
Description: This endpoint will search a partner with provided VAT number and will return the partner data.

Success Response:
```json
{
    "status": "success",
    "vat": "ESB60990298",
    "id": 1872,
    "name": "3G HIDRAULICA S.L.(DOMICILIO)",
    "parent_id": null
}
```
In case of failure:
```json
{"status": "fail", "user_id": False}
```


### Search a Partner ID:
URL: /create-user
Method: POST
Headers: ```json{
    'content-type': 'application/json',
    'Authorization': "eyJ0eXAiOiJ_5ysce6YET5Ew"
}```
Input: ```json {"partner_id": 123, "email": test@test.com, "password": "newpass"}```
Description: This endpoint will create a new user with partner id sent in request. Email would be login and password will be same as shared in post request.

Success Response:
```json
{
    "status": "success",
    "user_id": 1872
}
```
In case of failure:
```json
{"status": "fail", "errorDescription": "message"}
```