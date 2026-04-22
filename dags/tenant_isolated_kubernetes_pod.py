from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import Param

from airflow_dag_project.tenancy import get_tenant_runtime

DEFAULT_TENANT = "shared"
tenant_runtime = get_tenant_runtime(DEFAULT_TENANT)


with DAG(
    dag_id="tenant_isolated_kubernetes_pod",
    description="Run tenant workload in an isolated pod image instead of the shared Airflow image.",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "data-platform"},
    params={"tenant": Param(DEFAULT_TENANT, type="string")},
    tags=["kubernetes", "tenant-isolation"],
) as dag:
    start = EmptyOperator(task_id="start")

    run_isolated_workload = KubernetesPodOperator(
        task_id="run_isolated_workload",
        kubernetes_conn_id=tenant_runtime.kubernetes_conn_id,
        namespace=tenant_runtime.namespace,
        image=tenant_runtime.task_image,
        name="tenant-isolated-workload",
        cmds=["bash", "-lc"],
        arguments=[
            (
                "python - <<'PY'\n"
                "import os\n"
                "print('tenant:', os.environ['TENANT'])\n"
                "print('image isolation active')\n"
                "PY"
            )
        ],
        env_vars={"TENANT": "{{ params.tenant }}"},
        service_account_name=tenant_runtime.service_account_name,
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=False,
    )

    finish = EmptyOperator(task_id="finish")

    start >> run_isolated_workload >> finish
