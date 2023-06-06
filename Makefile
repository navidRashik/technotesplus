SHELL := /bin/bash

run_dev:
	cp example.env .env
	docker-compose up --build