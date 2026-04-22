FROM apache/airflow:3.1.8-python3.12

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

ENV AIRFLOW_HOME=/opt/airflow \
    AIRFLOW_REPO_ROOT=/opt/airflow/dags/repo \
    PYTHONPATH=/opt/airflow/dags/repo/src:/opt/airflow/dags/repo \
    AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags/repo/dags \
    AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/dags/repo/plugins
