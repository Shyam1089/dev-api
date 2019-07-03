#!/bin/sh -e

echo "Starting API..."
uwsgi --ini /etc/uwsgi.ini

