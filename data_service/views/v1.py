import json
import logging
from werkzeug.exceptions import BadRequest
from flask import request, Response, Blueprint, make_response
from flask_api import status

import data_service.errors as exceptions
import data_service.utils as utils
import marshmallow
from copy import deepcopy

from data_service.schema import ValidateInput, ValidateOrder, ValidateOrderLine, ValidateAddressInput,ValidateUserInput

JSON_TYPE_HEADERS = {'Content-Type': 'application/json'}
schema = Blueprint('schema', __name__)



@schema.route("/products", defaults={'doc_id': None}, methods=['GET'])
@schema.route("/products/<doc_id>", methods=['GET'])
@utils.error_handler()
def get_all_products_list(doc_id: int) -> Response:
    headers = request.headers
    auth_resp = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not auth_resp:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    if doc_id:
        try:
            temp = int(doc_id)
        except:
            return make_response(json.dumps({"error": "BadRequest", "errorDescription":"Product ID must be an Integer"}), status.HTTP_400_BAD_REQUEST)
    data = utils.get_products(doc_id)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/categories", defaults={'categ_id': None}, methods=['GET'])
@schema.route("/categories/<categ_id>", methods=['GET'])
@utils.error_handler()
def get_all_categories_list(categ_id: int) -> Response:
    headers = request.headers
    auth_resp = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not auth_resp:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    if categ_id:
        try:
            temp = int(categ_id)
        except:
            return make_response(json.dumps({"error": "BadRequest", "errorDescription":"Category ID must be an Integer"}), status.HTTP_400_BAD_REQUEST)
    data = utils.get_categories(categ_id)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/categories/<categ_id>/products", methods=['GET'])
@utils.error_handler()
def get_products_by_categ(categ_id: int) -> Response:
    headers = request.headers
    auth_resp = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not auth_resp:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    if categ_id:
        try:
            temp = int(categ_id)
        except:
            return make_response(json.dumps({"error": "BadRequest", "errorDescription":"Category ID must be an Integer"}), status.HTTP_400_BAD_REQUEST)
    data = utils.get_product_by_category(categ_id)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


# @schema.route("/orders", defaults={'order_id': None}, methods=['GET'])
@schema.route("/orders/<order_id>", methods=['GET'])
@utils.error_handler()
def get_all_orders_list(order_id: int) -> Response:
    headers = request.headers
    auth_resp = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not auth_resp:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    if order_id:
        try:
            temp = int(order_id)
        except:
            return make_response(json.dumps({"error": "BadRequest", "errorDescription":"Order ID must be an Integer"}), status.HTTP_400_BAD_REQUEST)
    data = utils.get_orders(order_id)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp



@schema.route("/authenticate", methods=['POST'])
@utils.error_handler()
def authenticate_user() -> Response:
    try:
        json_data = request.get_json(force=True)
    except BadRequest as e:
        logging.error('Failed to parse json from request body')
        raise exceptions.InvalidSyntaxError('JSON syntax error in request body')
    try:
        if not isinstance(json_data, dict):
            raise exceptions.InvalidSyntaxError('JSON syntax error in request body')
        post_data = ValidateInput().load(json_data)
    except marshmallow.exceptions.ValidationError as e:
        error = deepcopy(e.messages)
        error = {key: " ,".join(value) for (key, value) in error.items() if isinstance(value, list)}
        error.update({'errorDescription': 'Invalid input.'})
        raise exceptions.ValidationError(errors=[error])

    data = utils.authenticate_user(json_data)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/user", methods=['GET'])
@utils.error_handler()
def get_user_info() -> Response:
    headers = request.headers
    auth_resp = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not auth_resp:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)

    data = utils.get_user_data(str(auth_resp))
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/user/orders", methods=['GET'])
@utils.error_handler()
def get_user_orders_info() -> Response:
    headers = request.headers
    auth_resp = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not auth_resp:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    data = utils.get_user_orders(str(auth_resp))
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/user/visits", methods=['GET'])
@utils.error_handler()
def get_user_visits_info() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)

    data = utils.get_user_visits(str(uid))
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/user/reset-password", methods=['POST'])
@utils.error_handler()
def reset_usr_password() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    try:
        request_json = request.get_json(force=True)
        if not isinstance(request_json, dict):
            raise exceptions.InvalidSyntaxError('JSON syntax error in request body')
        post_data = ValidateInput().load(request_json)
    except marshmallow.exceptions.ValidationError as e:
        error = deepcopy(e.messages)
        error = {key: " ,".join(value) for (key, value) in error.items() if isinstance(value, list)}
        error.update({'errorDescription': 'Invalid input.'})
        raise exceptions.ValidationError(errors=[error])
    data = utils.reset_user_password(int(uid), request_json)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/user/address", methods=['GET'])
@utils.error_handler()
def get_user_addresses() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)

    data = utils.get_users_address(str(uid))
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/user/create-address", methods=['POST'])
@utils.error_handler()
def create_user_addresses() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    try:
        request_json = request.get_json(force=True)
        if not isinstance(request_json, dict):
            raise exceptions.InvalidSyntaxError('JSON syntax error in request body')
    except marshmallow.exceptions.ValidationError as e:
        request_json = {}

    if not request_json.get("name",False):
        raise exceptions.InvalidSyntaxError('Contact name is mandatory.')
    data = utils.create_users_address(str(uid), request_json)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp



@schema.route("/create-order", methods=['POST'])
@utils.error_handler()
def create_new_order() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    try:
        request_json = request.get_json(force=True)
        if not isinstance(request_json, dict):
            raise exceptions.InvalidSyntaxError('JSON syntax error in request body')
        post_data = ValidateOrder().load(request_json)
    except marshmallow.exceptions.ValidationError as e:
        error = deepcopy(e.messages)
        error = {key: " ,".join(value) for (key, value) in error.items() if isinstance(value, list)}
        error.update({'errorDescription': 'Invalid input.'})
        raise exceptions.ValidationError(errors=[error])

    if request_json:
        try:
            order_line = request_json.get("order_line", [])
            if not order_line:
                raise exceptions.InvalidSyntaxError('Order Lines cannot be empty!')
            for line in order_line:
                post_data = ValidateOrderLine().load(line)
        except marshmallow.exceptions.ValidationError as e:
            error = deepcopy(e.messages)
            error = {key: " ,".join(value) for (key, value) in error.items() if isinstance(value, list)}
            error.update({'errorDescription': 'Invalid order line input'})
            raise exceptions.ValidationError(errors=[error])
    visit_data = {
        'higiene': 0, 
        'averia': 0, 
        'agua_unserviced': 0, 
        'cleaning': 0, 
        'fpeq_unserviced': 0, 
        'higienes_unserviced': 0, 
        'is_partial': 0, 
        'visit_type_id': 1, 
        'visit_status_id': 1, 
        'important': 1, 
        'creator': "cliente-app", 
        'comments': "Please call before",
    }
    rec_data = request_json.get("visit",{})
    if not isinstance(rec_data, dict):
        rec_data = {}
    value = { k : rec_data[k] for k in set(rec_data) - set(visit_data) }
    if value:
        k = ",".join(value)
        raise exceptions.InvalidSyntaxError('Invalid table column for visit creation: %s'%(k))
    else:
        visit_data.update(rec_data)

    data, message = utils.create_order(request_json, visit_data)
    if message:
        resp: Response = make_response(json.dumps(message), status.HTTP_200_OK)
    else:
        resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp



@schema.route("/get-partner", methods=['POST'])
@utils.error_handler()
def get_partnerss() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    try:
        request_json = request.get_json(force=True)
    except marshmallow.exceptions.ValidationError as e:
        request_json = {}


    data = utils.get_partner(request_json)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp


@schema.route("/create-user", methods=['POST'])
@utils.error_handler()
def create_partnerss() -> Response:
    headers = request.headers
    uid = utils.verify_auth_token(headers.get("Authorization","Missing"))
    if not uid:
        return make_response(json.dumps({"error": "notAuthorized", "errorDescription":"Invalid/Expired Authorization Token!"}), status.HTTP_403_FORBIDDEN)
    try:
        request_json = request.get_json(force=True)
        if not isinstance(request_json, dict):
            raise exceptions.InvalidSyntaxError('JSON syntax error in request body')
        post_data = ValidateUserInput().load(request_json)
    except marshmallow.exceptions.ValidationError as e:
        error = deepcopy(e.messages)
        error = {key: " ,".join(value) for (key, value) in error.items() if isinstance(value, list)}
        error.update({'errorDescription': 'Invalid input.'})
        raise exceptions.ValidationError(errors=[error])


    data = utils.create_user_partner(request_json)
    resp: Response = make_response(json.dumps(data), status.HTTP_200_OK)
    resp.headers = JSON_TYPE_HEADERS
    return resp
