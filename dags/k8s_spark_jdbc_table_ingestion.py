from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator

from airflow_dag_project.k8s import apply_spark_application
from airflow_dag_project.spark import spark_application_identity
from airflow_dag_project.tenancy import get_tenant_runtime

tenant_runtime = get_tenant_runtime("shared")
SPARK_APPLICATION_NAMESPACE, SPARK_APPLICATION_NAME = spark_application_identity(
    "jdbc-table-ingestion.yaml"
)


with DAG(
    dag_id="k8s_spark_jdbc_table_ingestion",
    description="Submit a SparkApplication CR through the Apache Spark Operator API.",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "data-platform"},
    tags=["kubernetes", "spark"],
) as dag:
    start = EmptyOperator(task_id="start")

    submit_spark_application = PythonOperator(
        task_id="submit_spark_application",
        python_callable=apply_spark_application,
        op_kwargs={
            "filename": "jdbc-table-ingestion.yaml",
            "kubernetes_conn_id": tenant_runtime.kubernetes_conn_id,
        },
        doc_md=(
            "Creates or replaces the "
            f"`{SPARK_APPLICATION_NAME}` SparkApplication in namespace "
            f"`{SPARK_APPLICATION_NAMESPACE}`."
        ),
    )

    finish = EmptyOperator(task_id="finish")

    start >> submit_spark_application >> finish
