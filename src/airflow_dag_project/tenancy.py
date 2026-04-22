from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TenantRuntime:
    tenant: str
    namespace: str
    kubernetes_conn_id: str
    task_image: str
    service_account_name: str


def get_tenant_runtime(tenant: str) -> TenantRuntime:
    tenant_key = tenant.upper().replace("-", "_")
    default_namespace = os.getenv("DEFAULT_TENANT_NAMESPACE", "data")
    default_kubernetes_conn_id = os.getenv("DEFAULT_KUBERNETES_CONN_ID", "kubernetes_default")
    default_image = os.getenv("DEFAULT_TENANT_TASK_IMAGE", "python:3.12-slim")
    default_service_account = os.getenv("DEFAULT_TENANT_SERVICE_ACCOUNT", "default")

    return TenantRuntime(
        tenant=tenant,
        namespace=os.getenv(f"TENANT_{tenant_key}_NAMESPACE", default_namespace),
        kubernetes_conn_id=os.getenv(
            f"TENANT_{tenant_key}_KUBERNETES_CONN_ID",
            default_kubernetes_conn_id,
        ),
        task_image=os.getenv(f"TENANT_{tenant_key}_TASK_IMAGE", default_image),
        service_account_name=os.getenv(
            f"TENANT_{tenant_key}_SERVICE_ACCOUNT_NAME",
            default_service_account,
        ),
    )
