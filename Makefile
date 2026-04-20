PYTHON := uv run
EXECUTION_DATE ?= 2025-01-01
AIRFLOW_SERVICE ?= airflow-cli

.PHONY: sync lint format test test-integration up down logs dags-test kind-up kind-down kind-install-spark-operator

sync:
	uv sync

lint:
	$(PYTHON) ruff check .
	$(PYTHON) ruff format --check .

format:
	$(PYTHON) ruff check . --fix
	$(PYTHON) ruff format .

test:
	$(PYTHON) pytest tests/unit

test-integration:
	RUN_DOCKER_TESTS=1 $(PYTHON) pytest -m integration

up:
	docker compose up --build airflow-init
	docker compose up --build -d

down:
	docker compose down --volumes --remove-orphans

logs:
	docker compose logs -f

dags-test:
	test -n "$(DAG_ID)"
	$(PYTHON) airflow dags test $(DAG_ID) $(EXECUTION_DATE)

kind-up:
	./scripts/setup-kind-cluster.sh

kind-install-spark-operator:
	./scripts/install-spark-operator.sh

kind-down:
	kind delete cluster --name airflow-dag-local
