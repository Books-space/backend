#!make
include .env
export

lint:
	@flake8 webapp
	@mypy webapp

db.upd:
	docker-compose up -d

db.up:
	docker-compose up

db.create:
	python -m webapp.tools.db create

db.fill:
	python -m webapp.tools.db fill

db.down:
	docker-compose down

db.down.volumes:
	docker-compose down -t1 --volumes

webapp.run:
	python -m webapp