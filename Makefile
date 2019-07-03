SHELL := /bin/bash
VERSION ?= latest
.PHONY: run-liquibase restart-api destroy up scrub run test

build:
	docker build -t devcenter-schema-consolidator-api:$(VERSION) .

local-update:
	sh update-local-changes.sh