FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow/project

ENV AIRFLOW_HOME=/opt/airflow \
    PYTHONPATH=/opt/airflow/project/src:/opt/airflow/project \
    AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/project/dags \
    AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/project/plugins

COPY --chown=airflow:root pyproject.toml README.md ./
COPY --chown=airflow:root dags dags
COPY --chown=airflow:root include include
COPY --chown=airflow:root plugins plugins
COPY --chown=airflow:root src src

RUN pip install --no-cache-dir uv \
    && uv pip install --system -e .

