# Airflow DAG Project

Production-oriented Airflow DAG repository with:

- `uv` for dependency management
- local DAG debugging and testing
- Docker Compose for a reproducible Airflow stack
- Testcontainers-backed integration tests
- Kubernetes Spark example DAG using the Apache Spark Operator CRD

## Layout

```text
.
├── dags/                         # Airflow DAG definitions
├── include/spark-applications/   # SparkApplication manifests
├── plugins/                      # Airflow plugins and local settings
├── src/airflow_dag_project/      # Shared Python code for DAGs/tests
├── tests/                        # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Prerequisites

- `uv`
- Docker with Compose support

## Quick Start

1. Create the virtualenv and install dependencies:

   ```bash
   uv sync
   ```

2. Copy environment defaults:

   ```bash
   cp .env.example .env
   ```

3. Start the local Airflow stack. This mounts the current git checkout into the same runtime path you would normally target with `git-sync`:

   ```bash
   docker compose up --build airflow-init
   docker compose up --build
   ```

4. Open Airflow:

   - URL: `http://localhost:8080`
   - User: `admin`
   - Password: `admin`

## Local Development

Run static checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

Run unit tests:

```bash
uv run pytest tests/unit
```

Run integration tests that exercise Docker Compose through Testcontainers:

```bash
RUN_DOCKER_TESTS=1 uv run pytest -m integration
```

Debug a DAG run locally from the repo:

```bash
uv run airflow dags test example_local_debug 2025-01-01
uv run airflow dags test k8s_spark_jdbc_table_ingestion 2025-01-01
```

Open an interactive shell inside the Airflow image:

```bash
docker compose run --rm airflow-cli bash
```

## Kubernetes Spark Example

The example DAG `k8s_spark_jdbc_table_ingestion` submits the manifest at:

- `include/spark-applications/jdbc-table-ingestion.yaml`

The DAG uses the Kubernetes Python client to create or replace the `sparkapplications.spark.apache.org/v1` custom resource exposed by the Apache Spark Operator.

This manifest is derived from:

- `/data/Git/spark-lakehouse/jobs/bronze/jdbc-table-ingestion/jdbc-table-ingestion.yaml`

Before running the DAG against a cluster, configure:

- `SPARK_K8S_NAMESPACE`
- `KUBECONFIG` or in-cluster credentials
- `K8S_IN_CLUSTER=true` when Airflow runs inside Kubernetes

The DAG is intentionally written so that unit tests can import it without contacting Kubernetes.

## Git-Sync Runtime Model

The image now carries dependencies only. DAGs, plugins, manifests, and shared repo code are expected at runtime under `/opt/airflow/dags/repo`.

For local development, Docker Compose mounts this repository directly to that path:

- local mount: `.:/opt/airflow/dags/repo`
- Airflow DAG folder: `/opt/airflow/dags/repo/dags`
- Python path: `/opt/airflow/dags/repo/src:/opt/airflow/dags/repo`

That is the right local stand-in for a production `git-sync` checkout.

## Local Kubernetes Test Cluster

Yes. A small local Kubernetes cluster is practical for this repo. The supported path here is `kind` plus the official Apache Spark Operator Helm chart.

Bootstrap commands:

```bash
make kind-up
make kind-install-spark-operator
kubectl get crd sparkapplications.spark.apache.org
```

Scripts:

- `scripts/setup-kind-cluster.sh`
- `scripts/install-spark-operator.sh`

Official operator install reference:

- https://apache.github.io/spark-kubernetes-operator/

## Make Targets

```bash
make sync
make lint
make test
make test-integration
make up
make down
make dags-test DAG_ID=example_local_debug EXECUTION_DATE=2025-01-01
make kind-up
make kind-install-spark-operator
make kind-down
```
