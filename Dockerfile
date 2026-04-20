FROM apache/airflow:3.2.0-python3.12

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

ENV AIRFLOW_HOME=/opt/airflow \
    AIRFLOW_REPO_ROOT=/opt/airflow/dags/repo \
    UV_PROJECT_ENVIRONMENT=/opt/airflow/.venv \
    PATH=/opt/airflow/.venv/bin:/home/airflow/.local/bin:${PATH} \
    PYTHONPATH=/opt/airflow/dags/repo/src:/opt/airflow/dags/repo \
    AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags/repo/dags \
    AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/dags/repo/plugins

COPY --chown=airflow:root pyproject.toml uv.lock README.md /opt/airflow/build/

RUN pip install --no-cache-dir uv
WORKDIR /opt/airflow/build
RUN uv sync --frozen --no-dev --no-install-project
WORKDIR /opt/airflow
