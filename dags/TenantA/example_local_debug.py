from __future__ import annotations

from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="tenant_a_example_local_debug",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example", "local"],
    default_args={"owner": "data-platform"},
)
def example_local_debug() -> None:
    @task
    def emit_debug_context() -> dict:
        return {
            "status": "ok",
            "message": "Local Airflow DAG debug path is working.",
        }

    emit_debug_context()


dag = example_local_debug()
