import json
from copy import deepcopy
from collections import defaultdict
import traceback
import marshmallow
import os

from datetime import datetime, timedelta
from functools import wraps
from enum import unique, Enum

from flask import Response, request, make_response
from flask_api import status

import data_service.errors as exceptions
from data_service.errors import InternalServerError, get_error_response
from xmlrpc import client as xmlrpclib
import psycopg2
import psycopg2.extras
import logging as logger
import pymysql.cursors

from data_service.credentials import CONF

JSON_TYPE_HEADERS = {'Content-Type': 'application/json'}


def get_error_response(exception):
    error = {
        "status": "error",
        "error": {
            "error": exception.type,
            "errorDescription": exception.description
        }
    }
    if hasattr(exception, 'errors'):
        error['error']['validationErrors'] = exception.errors
    return error


def error_handler():
    def decorate(function):
        @wraps(function)
        def call_method(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except (exceptions.InvalidSyntaxError, exceptions.ValidationError) as e:
                resp: Response = make_response((json.dumps(get_error_response(e))), status.HTTP_400_BAD_REQUEST)
                resp.headers = JSON_TYPE_HEADERS
                return resp
            except Exception as e:
                logger.error('INTERNAL SERVER ERROR: (%s)\n%s'%(e,traceback.print_exc()))
                resp: Response = make_response(json.dumps(get_error_response(
                    InternalServerError())), status.HTTP_500_INTERNAL_SERVER_ERROR)
                resp.headers = JSON_TYPE_HEADERS
                return resp
        return call_method
    return decorate



def get_msql_cursor():
    connection = pymysql.connect(host=CONF.get("SQL_HOST"),
                             user=CONF.get("SQL_USER"),
                             password=CONF.get("SQL_PASS"),
                             db=CONF.get("SQL_DB"),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    if connection:
        return connection
    return False


def get_pg_cursor():
    host = CONF.get("PG_HOST")
    user = CONF.get("PG_USER")
    password = CONF.get("PG_PASS")
    db = CONF.get("PG_DB")
    try:
        conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s"%(db, user, host, password))
    except:
        return False, False
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn, cur


def get_products(pid=False):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        if not pid:
            pg_cur.execute("SELECT t.pack_stock_management, t.is_pack, t.formato_peq, t.agua, t.categ_id, t.name, t.type, t.list_price, t.description, v.id as id, t.id as template_id, v.ean13, v.default_code from product_template t INNER JOIN product_product v ON t.id=v.product_tmpl_id ORDER BY v.id" )
        else:
            pg_cur.execute("SELECT t.pack_stock_management, t.is_pack, t.formato_peq, t.agua, t.categ_id, t.name, t.type, t.list_price, t.description, v.id as id, t.id as template_id, v.ean13, v.default_code  from product_template t INNER JOIN product_product v ON t.id=v.product_tmpl_id WHERE v.id=%s"%pid )

        rows = pg_cur.fetchall()
        for row in rows:
            pack = []
            if row.get('is_pack',False):
                pg_cur.execute("""SELECT product_name, product_quantity from product_pack where wk_product_template =%s"""%(str(row['template_id'])))
                pack = pg_cur.fetchall()
            image_url = CONF.get("ODOO_URL")+"/website/image/product.template/"+str(row['template_id'])+"/image_medium"
            row.update({'list_price': str(row['list_price']), "pack_items": pack, "image_url": image_url})
        pg_cur.close()
        conn.close()
    return rows


def get_categories(pid=False):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        query = "SELECT id, name, parent_id FROM product_category"
        if pid:
            query += " WHERE id=%s"%(pid)
        pg_cur.execute(query)
        if pid:
            row = pg_cur.fetchone()
        else:
            row = pg_cur.fetchall()
        pg_cur.close()
        conn.close()
        if row:
            rows = row
    return rows


def get_product_by_category(pid):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        pg_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        pg_cur.execute("SELECT t.formato_peq, t.agua, t.categ_id, t.name, t.type, t.list_price, t.description, v.id as id, t.id as template_id, v.ean13, v.default_code from product_template t INNER JOIN product_product v ON t.id=v.product_tmpl_id WHERE t.categ_id=%s"%pid )
        dataaa = pg_cur.fetchall()
        for row in dataaa:
            pack = []
            if row.get("is_pack",False):
                pg_cur.execute("""SELECT product_name, product_quantity from product_pack where wk_product_template =%s"""%(str(row['template_id'])))
                pack = pg_cur.fetchall()
            image_url = CONF.get("ODOO_URL")+"website/image/product.template/"+str(row['template_id'])+"/image_medium"

            row.update({'list_price': str(row['list_price']), "pack_items": pack, "image_url": image_url})
        pg_cur.close()
        conn.close()
        if dataaa:
            rows = dataaa
    return rows


def get_orders(pid=False):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        order_ids = [pid]
        if not pid:
            pg_cur.execute("SELECT id FROM sale_order")
            rows = pg_cur.fetchall()
            order_ids = [x['id'] for x in rows]
        order_ids = [str(x) for x in order_ids]
        l = ",".join(order_ids)
        pg_cur.execute("""SELECT "sale_order"."id" as "id","sale_order"."origin" as "origin","sale_order"."date_order" as "date_order","sale_order"."picking_policy" as "picking_policy","sale_order"."create_uid" as "create_uid","sale_order"."partner_id" as "partner_id","sale_order"."client_order_ref" as "client_order_ref","sale_order"."note" as "note", "sale_order"."partner_invoice_id" as "partner_invoice_id","sale_order"."amount_untaxed" as "amount_untaxed","sale_order"."partner_shipping_id" as "partner_shipping_id","sale_order"."create_date" as "create_date","sale_order"."company_id" as "company_id","sale_order"."amount_tax" as "amount_tax","sale_order"."payment_term" as "payment_term","sale_order"."carrier_id" as "carrier_id","sale_order"."amount_total" as "amount_total","sale_order"."name" as "name","sale_order"."state" as "state","sale_order"."user_id" as "user_id" FROM "sale_order" WHERE "sale_order".id IN (%s)"""%(l))
        rows = pg_cur.fetchall()
        for row in rows:
            if row.get("create_date", False):
                row.update({"create_date": row['create_date'].strftime("%m/%d/%Y, %H:%M:%S")})
            if row.get("confirmation_date", False):
                row.update({"confirmation_date": row['confirmation_date'].strftime("%m/%d/%Y, %H:%M:%S")})
            if row.get("date_order", False):
                row.update({"date_order": row['date_order'].strftime("%m/%d/%Y, %H:%M:%S")})
            row.update({'amount_untaxed': str(row['amount_untaxed'])})
            row.update({'amount_total': str(row['amount_total'])})
            row.update({'amount_tax': str(row['amount_tax'])})
            row.update({'line_data': []})
            pg_cur.execute("""SELECT  "product_uom", "sequence", "price_unit", "product_uom_qty", "invoiced", "id", "order_id", "discount", "product_id", "name" FROM sale_order_line where order_id =%s"""%(row['id']))
            line_data = pg_cur.fetchall()
            for line in line_data:
                line.update({'price_unit': str(line['price_unit'])})
                line.update({'product_uom_qty': str(line['product_uom_qty'])})
                # line.update({'qty_invoiced': str(line['qty_invoiced'])})
                # line.update({'price_tax': str(line['price_tax'])})
                line.update({'discount': str(line['discount'])})
                # line.update({'price_subtotal': str(line['price_subtotal'])})
                # line.update({'qty_delivered': str(line['qty_delivered'])})
                # line.update({'price_total': str(line['price_total'])})
                row['line_data'].append(line)
        pg_cur.close()
        conn.close()
        if pid and rows:
            return rows[0]
    return rows


def authenticate_user(json_data):
    url = CONF.get("ODOO_URL")
    username = json_data.get("username")
    password = json_data.get("password")
    db = CONF.get("ODOO_DB")
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    uid = common.login(db, username, password)
    # result = sock.execute(db, uid, password, 'res.partner', 'search_read', [['id', '=', 1]])
    # number_of_customers = sock.execute(db, uid, password, 'res.partner', 'search_count', [])
    if uid:
        return {'status': "success", "user_id": uid}
    return {'status': "fail", "user_id": False}


def get_user_data(pid=False):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        pg_cur.execute("""SELECT  "res_users"."id" as "id","res_users"."partner_id" as "partner_id","res_users"."login" as "login","res_users"."company_id" as "company_id","res_users"."signature" as "signature","res_users"."alias_id" as "alias_id" FROM "res_users" WHERE "res_users".id IN (%s)"""%(pid))
        rows = pg_cur.fetchone()
        if rows and rows.get('partner_id',False):
            pg_cur.execute("""SELECT "website", "street", "street2", "city", "zip", "email", "phone", "mobile" FROM "res_partner" WHERE id IN (%s)"""%(rows['partner_id']))
            partner_data = pg_cur.fetchone()
            rows.update(partner_data)
        else:
            rows = {'status':"NotFound"}
        pg_cur.close()
        conn.close()
    return rows


def get_user_orders(pid=False):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        pg_cur.execute("""SELECT "res_users"."partner_id" as "partner_id" FROM "res_users" WHERE "res_users".id IN (%s)"""%(pid))
        rows = pg_cur.fetchone()
        if rows and rows.get('partner_id',False):
            pg_cur.execute("""SELECT "sale_order"."id" as "id","sale_order"."origin" as "origin","sale_order"."date_order" as "date_order","sale_order"."picking_policy" as "picking_policy","sale_order"."create_uid" as "create_uid","sale_order"."partner_id" as "partner_id","sale_order"."client_order_ref" as "client_order_ref","sale_order"."note" as "note", "sale_order"."partner_invoice_id" as "partner_invoice_id","sale_order"."amount_untaxed" as "amount_untaxed","sale_order"."partner_shipping_id" as "partner_shipping_id","sale_order"."create_date" as "create_date","sale_order"."company_id" as "company_id","sale_order"."amount_tax" as "amount_tax","sale_order"."payment_term" as "payment_term","sale_order"."carrier_id" as "carrier_id","sale_order"."amount_total" as "amount_total","sale_order"."name" as "name","sale_order"."state" as "state","sale_order"."user_id" as "user_id" FROM "sale_order" WHERE "sale_order".partner_id=%s"""%(rows.get('partner_id',False)))
            rows = pg_cur.fetchall()
            for row in rows:
                if row.get("create_date", False):
                    row.update({"create_date": row['create_date'].strftime("%m/%d/%Y, %H:%M:%S")})
                if row.get("confirmation_date", False):
                    row.update({"confirmation_date": row['confirmation_date'].strftime("%m/%d/%Y, %H:%M:%S")})
                if row.get("date_order", False):
                    row.update({"date_order": row['date_order'].strftime("%m/%d/%Y, %H:%M:%S")})
                row.update({'amount_untaxed': str(row['amount_untaxed'])})
                row.update({'amount_total': str(row['amount_total'])})
                row.update({'amount_tax': str(row['amount_tax'])})
                row.update({'line_data': []})
                pg_cur.execute("""SELECT  "product_uom", "sequence", "price_unit", "product_uom_qty", "invoiced", "id", "order_id", "discount", "product_id", "name" FROM sale_order_line where order_id =%s"""%(row['id']))
                line_data = pg_cur.fetchall()
                for line in line_data:
                    line.update({'price_unit': str(line['price_unit'])})
                    line.update({'product_uom_qty': str(line['product_uom_qty'])})
                    # line.update({'qty_invoiced': str(line['qty_invoiced'])})
                    # line.update({'price_tax': str(line['price_tax'])})
                    line.update({'discount': str(line['discount'])})
                    # line.update({'price_subtotal': str(line['price_subtotal'])})
                    # line.update({'qty_delivered': str(line['qty_delivered'])})
                    # line.update({'price_total': str(line['price_total'])})
                    row['line_data'].append(line)
                # partner_data = pg_cur.fetchone()
                # rows.update(partner_data)
        else:
            rows = {'status':"NotFound"}
        pg_cur.close()
        conn.close()
    return rows


def get_sql_client_id():
    return True


def get_erp_partner_id(pg_cur, pid):
    pg_cur.execute("""SELECT "res_users"."partner_id" as "partner_id" FROM "res_users" WHERE "res_users".id IN (%s)"""%(pid))
    rows = pg_cur.fetchone()
    if not rows:
        return False
    return rows.get('partner_id',False)


def get_user_visits(pid):
    rows = {'status':"NotFound"}
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        erp_id = get_erp_partner_id(pg_cur, pid)
        if erp_id:
            connection = get_msql_cursor()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT CLIENTE FROM clientes WHERE odoo_code=%s', erp_id)
                        # cursor.execute('SELECT CLIENTE FROM clientes WHERE odoo_code=%s', 1759)
                        result = cursor.fetchone()
                        if result:
                            cursor.execute('SELECT * FROM visits WHERE cliente=%s', str(result.get("CLIENTE")))
                            rows = cursor.fetchall()
                            if rows:
                                for row in rows:
                                    row.pop('modified', None)
                                    if row.get("status_date", False):
                                        row.update({"status_date": row['status_date'].strftime("%m/%d/%Y, %H:%M:%S")})
                                    if row.get("created", False):
                                        row.update({"created": row['created'].strftime("%m/%d/%Y, %H:%M:%S")})
                                    if row.get("visit_date", False):
                                        row.update({"visit_date": row['visit_date'].strftime("%m/%d/%Y")})
                finally:
                    connection.close()
        pg_cur.close()
        conn.close()
    return rows


def reset_user_password(user_id, json_data):
    url = CONF.get("ODOO_URL")
    username = CONF.get("ODOO_USER")
    password = CONF.get("ODOO_PASS")
    db = CONF.get("ODOO_DB")
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    uid = common.login(db, username, password)
    try:
        rec_id = sock.execute(db, uid, password, 'change.password.wizard', 'create', {
            "user_ids" :[(0,0,{"user_login": json_data.get("username"), "new_passwd": json_data.get("password"), "user_id": user_id})]
            })
        number_of_customers = sock.execute(db, uid, password, 'change.password.wizard', 'change_password_button', [rec_id])
    except:
        return {'status': "success", "description": "Password updated!"}
    return {'status': "fail", "user_id": False}


def create_order(json_data, visit_data):
    visit_data, message = get_visit_data(json_data, visit_data)
    if not visit_data:
        return visit_data, message
    print (visit_data)
    url = CONF.get("ODOO_URL")
    username = CONF.get("ODOO_USER")
    password = CONF.get("ODOO_PASS")
    db = CONF.get("ODOO_DB")
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    uid = common.login(db, username, password)
    order_id = False
    if uid:
        try:
            data = sock.execute(db, uid, password, 'sale.order', 'default_get', ["pricelist_id", "company_id", "team_id", "picking_policy", "warehouse_id"])
            data.update(json_data)
            packs = []
            non_pack = []
            for line in data.get("order_line",[]):
                if line.get("tax_id"):
                    line.update({"tax_id" :[(6,0,[int(line.get("tax_id"))])]})
                if line['is_pack']:
                    packs.append(line)
                else:
                    non_pack.append((0,0,line))
            data.update({"order_line": non_pack})
            order_id = sock.execute(db, uid, password, 'sale.order', 'create', data)

            for pack in packs:
                wiz_id = sock.execute(db, uid, password, 'product.pack.wizard', 'create', {
                    'name':pack['name'],
                    'product_name':pack['product_id'],
                    'quantity': pack['product_uom_qty'],
                    'unit_price':pack["price_unit"]
                })
                sock.execute(db, uid, password, 'product.pack.wizard', 'add_product_button', [wiz_id], {'active_id':order_id})
        except Exception as e:
            order_id = False
    if not order_id:
        return {"status": "fail", "errorDescription": str(e)}
    else:
        connection = get_msql_cursor()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT CLIENTE FROM clientes WHERE odoo_code=%s', json_data['partner_id'])
                    # cursor.execute('SELECT CLIENTE FROM clientes WHERE odoo_code=%s', 1759)
                    result = cursor.fetchone()
                    if result:
                        cursor.execute('SELECT * FROM visits WHERE cliente=%s', str(result.get("CLIENTE")))
                        rows = cursor.fetchall()
                        if rows:
                            for row in rows:
                                row.pop('modified', None)
                                if row.get("status_date", False):
                                    row.update({"status_date": row['status_date'].strftime("%m/%d/%Y, %H:%M:%S")})
                                if row.get("created", False):
                                    row.update({"created": row['created'].strftime("%m/%d/%Y, %H:%M:%S")})
                                if row.get("visit_date", False):
                                    row.update({"visit_date": row['visit_date'].strftime("%m/%d/%Y")})
            finally:
                connection.close()


    return {'status': "sucess", "order_id": order_id}, False


def get_visit_data(json_data, visit_data):
    visit_data.update({
        'created': datetime.now(), 
        'status_date': datetime.now()
    })

    for line in json_data.get('order_line'):
        prod_data = get_products(line.get('product_id'))
        if not prod_data:
            return False, make_response(json.dumps({"error": "BadRequest", "errorDescription":"Unable to find product with ID: %s"%(line.get('product_id'))}), status.HTTP_400_BAD_REQUEST)
        if prod_data[0]['agua']:
            visit_data.update({
                'agua': 1
            })
        if prod_data[0]['formato_peq']:
            visit_data.update({
                'formato_peq': 1
            })

    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        name = False
        partner_id = json_data.get('partner_id')
        partner_id = 2077
        pg_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if pg_cur:
            pg_cur.execute("SELECT route_id FROM res_partner WHERE id=%s"%(str(partner_id)))
            row = pg_cur.fetchone()
            if row:
                print (row)
                pg_cur.execute("SELECT name FROM res_partner_routes WHERE id=%s"%(row['route_id']))
                row = pg_cur.fetchone()
                if row:
                    name = row.get("name")
        pg_cur.close()
        conn.close()
        if not name:
            return False, make_response(json.dumps({"error": "BadRequest", "errorDescription":"Unable to find route name in Odoo"}), status.HTTP_400_BAD_REQUEST)
        connection = get_msql_cursor()
        if connection:
            try:
                with connection.cursor() as cursor:
                    weekday = False
                    cursor.execute('SELECT * FROM routes WHERE name=%s', name)
                    result = cursor.fetchone()
                    if result:
                        weekday = int(result['weekday'])
                        datee = calculate_date(weekday)
                        visit_data.update({'driver_id': str(result['driver_id']), "visit_date": datee})
                    else:
                        return False, make_response(json.dumps({"error": "BadRequest", "errorDescription":"No driver ID with name: %s found in mySQL"%(name)}), status.HTTP_400_BAD_REQUEST)
                    cursor.execute('SELECT CLIENTE FROM clientes WHERE odoo_code=%s', str(partner_id))
                    # cursor.execute('SELECT CLIENTE FROM clientes WHERE odoo_code=%s', 1759)
                    data = cursor.fetchone()
                    if data:
                        visit_data.update({'cliente': str(data.get("CLIENTE"))})
                    else:
                        return False, make_response(json.dumps({"error": "BadRequest", "errorDescription":"No client with Odoo_code: %s, found in mySQL"%(str(partner_id))}), status.HTTP_400_BAD_REQUEST)
                    cursor.execute('SELECT * FROM clientes_configs WHERE cliente_id=%s', str(data.get("CLIENTE")))
                    conf_data = cursor.fetchone()
                    if conf_data:
                        visit_data.update({'route_id': str(conf_data.get('route_id'))})
                    else:
                        return False, make_response(json.dumps({"error": "BadRequest", "errorDescription":"No client config found for client: %s, found in mySQL"%(str(data.get("CLIENTE")))}), status.HTTP_400_BAD_REQUEST)
            finally:
                connection.close()
        else:
            return False, make_response(json.dumps({"error": "BadRequest", "errorDescription":"Error in Mysql Connection"}), status.HTTP_400_BAD_REQUEST)

    return visit_data, None



def calculate_date(rec):
    curr =  datetime.now()
    while True:
        iso = curr.isoweekday()
        if iso>6:
            iso = 0
        if rec == iso:
            break
        curr = curr + timedelta(days=1)
    return curr


def get_users_address(pid=False):
    rows = {'status':"NotFound"}
    address = []
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        pg_cur.execute("""SELECT  "res_users"."id" as "id","res_users"."partner_id" as "partner_id" FROM "res_users" WHERE "res_users".id IN (%s)"""%(pid))
        rows = pg_cur.fetchone()
        if rows and rows.get('partner_id',False):
            rows.update({"partner_id": rows['partner_id']})
            pg_cur.execute("""SELECT "id", "name", "type", "function", "street", "street2", "city", "zip", "email", "phone", "mobile" FROM "res_partner" WHERE parent_id IN (%s)"""%(rows['partner_id']))
            address = pg_cur.fetchall()
            rows.update({"status": "success"})
        pg_cur.close()
        conn.close()
    rows.update({"address": address})
    return rows


def create_users_address(pid, request_json):
    rows = {'status':"NotFound"}
    address = []
    conn, pg_cur = get_pg_cursor()
    if pg_cur:
        pg_cur.execute("""SELECT  "res_users"."id" as "id","res_users"."partner_id" as "partner_id" FROM "res_users" WHERE "res_users".id IN (%s)"""%(pid))
        rows = pg_cur.fetchone()
        pg_cur.close()
        conn.close()
        partner_id = rows.get('partner_id',False)
        if partner_id:
            request_json.update({"type": "contact", "use_parent_address": False, "parent_id": partner_id})
            url = CONF.get("ODOO_URL")
            username = CONF.get("ODOO_USER")
            password = CONF.get("ODOO_PASS")
            db = CONF.get("ODOO_DB")
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            uid = common.login(db, username, password)
            rec_id = sock.execute(db, uid, password, 'res.partner', 'create', request_json)
            rows.update({"status": "success", "address_id": rec_id})
    return rows
