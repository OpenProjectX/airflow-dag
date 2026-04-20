from __future__ import annotations

from airflow_dag_project.spark import load_spark_application, spark_application_path


def test_spark_application_defaults_namespace() -> None:
    manifest = load_spark_application("jdbc-table-ingestion.yaml")

    assert manifest["kind"] == "SparkApplication"
    assert manifest["metadata"]["name"] == "jdbc-table-ingestion"
    assert manifest["metadata"]["namespace"] == "analytics"


def test_spark_application_path_resolves_manifest_name() -> None:
    assert spark_application_path("jdbc-table-ingestion.yaml").name == "jdbc-table-ingestion.yaml"
