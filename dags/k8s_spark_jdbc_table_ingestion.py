from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)

from airflow_dag_project.spark import spark_application_path

with DAG(
    dag_id="k8s_spark_jdbc_table_ingestion",
    description="Submit a SparkApplication to Kubernetes using the Spark Operator.",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "data-platform"},
    tags=["kubernetes", "spark"],
) as dag:
    start = EmptyOperator(task_id="start")

    submit_spark_application = SparkKubernetesOperator(
        task_id="submit_spark_application",
        namespace="{{ var.value.get('spark_k8s_namespace', 'analytics') }}",
        application_file=str(spark_application_path("jdbc-table-ingestion.yaml")),
        kubernetes_conn_id="kubernetes_default",
        do_xcom_push=False,
        get_logs=True,
        delete_on_termination=False,
    )

    finish = EmptyOperator(task_id="finish")

    start >> submit_spark_application >> finish
