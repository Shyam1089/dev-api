import sys
import json
import logging
import time
import os
import threading

from logging.config import dictConfig

from flask import Flask, make_response, request, Response, g
from flask_api import status

from werkzeug.exceptions import HTTPException


from data_service.utils import error_handler 
from data_service.views.v1 import schema


JSON_TYPE_HEADERS = {'Content-Type': 'application/json'}

DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'json': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter"

        },
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        }
    },
    'loggers': {
        'json': {
            'level': 'INFO',
            'handlers': ['json']

        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}


dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger('json')
application = Flask(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
application.logger.addHandler(logging.StreamHandler(sys.stdout))
application.register_blueprint(schema)


@application.route("/up")
@error_handler()
def up() -> Response:
    return make_response(json.dumps({"status": "happy"}), 200)

  
def get_request_hdr(request) -> dict:
    headers = request.headers
    data = {
        "type": "usage",
        "app": "shipping_document_api",
        "correlationId": headers.get('X-Request-id', "-"),
    }
    return data


@application.before_request
def before_request():
    g.start = time.time()
    headers = request.headers
    data = {
        "api": request.path,
        "uri": request.url,
        "method": request.method,
        "origin": headers.get("X-Forwarded-For", "-"),
        "agent": headers.get('User-Agent', "-"),
        "from": headers.get("FROM", "-"),
        "requested_time": time.time()
    }
    try:
        data["request_body"] = request.data
    except Exception as e:
        logger.info("ERROR while trying request.data: %s" % e)
    hdr = get_request_hdr(request)
    logger.info(dict(requestData=data, requestHeader=hdr))
    print ("%sREQUEST TRACE STARTS%s"%("*"*15,"*"*15))


@application.after_request
def after_request(resp) -> Response:
    print ("%sREQUEST TRACE ENDS%s"%("*"*15,"*"*15))
    # logger.info(dict(responseData=resp.__dict__, responseTime=time.time() - g.start))
    return resp


def http_error_handler(error) -> Response:
    server_error = {
        "status": "error",
        "error": {
            "error": "",
            "errorDescription": "",
        }
    }
    if isinstance(error, HTTPException):
        server_error['error']['error'] = error.name
        server_error['error']['errorDescription'] = error.description
        return make_response(json.dumps(server_error), error.code)
    else:
        server_error['error']['error'] = 'internalServerError'
        server_error['error']['errorDescription'] = \
            'Internal error occurred, please try again.'
        return make_response(json.dumps(server_error), status.HTTP_500_INTERNAL_SERVER_ERROR)


application.register_error_handler(status.HTTP_401_UNAUTHORIZED, http_error_handler)
application.register_error_handler(status.HTTP_403_FORBIDDEN, http_error_handler)
application.register_error_handler(status.HTTP_404_NOT_FOUND, http_error_handler)
application.register_error_handler(status.HTTP_405_METHOD_NOT_ALLOWED, http_error_handler)
application.register_error_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, http_error_handler)

