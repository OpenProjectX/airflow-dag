from __future__ import annotations

from airflow.models import DagBag


def test_dags_import_without_errors() -> None:
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    assert dag_bag.import_errors == {}


def test_expected_dags_are_present() -> None:
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    assert "example_local_debug" in dag_bag.dags
    assert "k8s_spark_jdbc_table_ingestion" in dag_bag.dags

