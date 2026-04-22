# Airflow DAG Project

Production-oriented Airflow DAG repository with:

- `uv` for dependency management
- local DAG debugging and testing
- Docker Compose for a reproducible Airflow stack
- Testcontainers-backed integration tests
- Kubernetes Spark example DAG using the Apache Spark Operator CRD
- tenant-isolated workload execution via `KubernetesPodOperator`

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

## Runtime Model

This repository treats the Airflow runtime image as the platform boundary.

- The Airflow image is authoritative for Airflow core and provider versions.
- DAG code is delivered separately through a repo mount locally and `git-sync` in production.
- Tenant-specific libraries do not belong in the shared Airflow image.
- Tenants that need different libraries should run tasks in dedicated images, typically with `KubernetesPodOperator` or a Spark workload image.

As inspected from the live `data` namespace on April 22, 2026, the current platform versions are:

- `apache-airflow==3.1.8`
- `apache-airflow-providers-cncf-kubernetes==10.13.0`
- `apache-airflow-providers-fab==3.4.0`
- `PyYAML==6.0.3`
- `structlog==25.5.0`

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

The DAG uses [src/airflow_dag_project/k8s.py](/data/Git/airflow-dag/src/airflow_dag_project/k8s.py), which resolves credentials through `apache-airflow-providers-cncf-kubernetes` and then creates or replaces the `sparkapplications.spark.apache.org/v1` custom resource exposed by the Apache Spark Operator.

This manifest is derived from:

- `/data/Git/spark-lakehouse/jobs/bronze/jdbc-table-ingestion/jdbc-table-ingestion.yaml`

Before running the DAG against a cluster, configure:

- `SPARK_K8S_NAMESPACE`
- Airflow connection `kubernetes_default` or another Kubernetes connection ID

The DAG is intentionally written so that unit tests can import it without contacting Kubernetes.

## Multi-Tenancy

The repository assumes a shared Airflow control plane and isolated tenant workloads.

- Shared platform image:
  - Airflow core
  - Airflow providers
  - lightweight orchestration helpers used at DAG parse time
- Tenant runtime images:
  - team-specific Python libraries
  - business logic dependencies
  - native binaries and heavy runtime stacks

The example DAG [dags/tenant_isolated_kubernetes_pod.py](/data/Git/airflow-dag/dags/tenant_isolated_kubernetes_pod.py) shows the expected pattern: use `KubernetesPodOperator` to run tenant code in a separate container image instead of installing tenant libraries into the shared Airflow image.

Tenant defaults are configured through environment variables:

- `DEFAULT_TENANT_NAMESPACE`
- `DEFAULT_KUBERNETES_CONN_ID`
- `DEFAULT_TENANT_TASK_IMAGE`
- `DEFAULT_TENANT_SERVICE_ACCOUNT`

Per-tenant runtime resolution lives in [src/airflow_dag_project/tenancy.py](/data/Git/airflow-dag/src/airflow_dag_project/tenancy.py).

## Git-Sync Runtime Model

The image does not install Python dependencies from this repo. DAGs, plugins, manifests, and shared repo code are expected at runtime under `/opt/airflow/dags/repo`.

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
