SHELL := /bin/bash

local-create-dev-db:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Creating development database on aws (local)"
	@echo "------------------------------------------------------------------"
	@echo "1. sourcing .local.dev.env"
	@echo $DATABASE_URL
	@echo "2. drop/create extension postgis"
	@source .local.dev.env && python scripts/create_postgis.py
	@echo "3. drop/create tables"
	@source .local.dev.env && python create_tables.py

aws-create-dev-db:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Creating development database on aws"
	@echo "------------------------------------------------------------------"
	@echo "1. sourcing .aws.dev.env"
	@echo $DATABASE_URL
	@echo "2. drop/create extension postgis"
	@source .aws.dev.env && python scripts/create_postgis.py
	@echo "3. drop/create tables"
	@source .aws.dev.env && python create_tables.py


aws-deploy-dev:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Deploying in development"
	@echo "------------------------------------------------------------------"
	@echo "1. sourcing .aws.dev.env"
	@echo "2. set environment variables: APP_SETTINGS, OAUTH_CONSUMER_KEY, OAUTH_SECRET"
	@source .aws.dev.env && eb setenv APP_SETTINGS=$(APP_SETTINGS) OAUTH_CONSUMER_KEY=$(OAUTH_CONSUMER_KEY) \
		OAUTH_SECRET=$(OAUTH_SECRET) DATABASE_URL=$(DATABASE_URL)
	@eb deploy
