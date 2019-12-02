build:
	docker-compose -f local.yml build --force-rm --parallel
start:
	docker-compose -f local.yml up
run_django:
	docker-compose -f local.yml run --rm django $(cmd)
build_prod:
	docker-compose -f production.yml build --force-rm
start_prod:
	docker-compose -f production.yml up -d
run_django_prod:
	docker-compose -f production.yml run --rm django $(cmd)
