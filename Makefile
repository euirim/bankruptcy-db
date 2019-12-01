build:
	docker-compose -f local.yml build --force-rm --parallel
start:
	docker-compose -f local.yml up
run_django:
	docker-compose -f local.yml run --rm django $(cmd)
