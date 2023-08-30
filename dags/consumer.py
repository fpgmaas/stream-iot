from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.kubernetes.secret import Secret
from kubernetes.client import (
    V1Affinity,
    V1NodeAffinity,
    V1NodeSelector,
    V1NodeSelectorRequirement,
    V1NodeSelectorTerm,
)
from kubernetes.client import models as k8s

# Memory requests for the Kubernetes pod
memory_request = k8s.V1ResourceRequirements(
    requests={
        "memory": "1G",
    }
)

# Node affinity ensures that the pod runs on 'application' nodes
affinity = V1Affinity(
    node_affinity=V1NodeAffinity(
        required_during_scheduling_ignored_during_execution=V1NodeSelector(
            node_selector_terms=[
                V1NodeSelectorTerm(
                    match_expressions=[
                        V1NodeSelectorRequirement(
                            key="agentpool", operator="In", values="application"
                        )
                    ]
                )
            ]
        )
    )
)

mongodb_connection_string = Secret(
    deploy_type="env",
    deploy_target="MONGODB_CONNECTION_STRING",
    secret="mongodb-connection-string",  # noqa: S106
    key="mongodb-connection-string",
)

default_args = {
    "retries": 1,
    "start_date": datetime(2022, 1, 1),
    "image_pull_policy": "Always",
    "secrets": [mongodb_connection_string],
    "env_vars": [k8s.V1EnvVar(name="ENVIRONMENT", value="cluster")],
    "affinity": affinity,
}

with DAG(
    dag_id="consumer",
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    tags=["example"],
    max_active_runs=1,
) as dag:
    simple_task = KubernetesPodOperator(
        task_id="consume",
        image="streamiotacr.azurecr.io/streamiot:latest",
        cmds=["python", "app/consumer.py"],
        container_resources=memory_request,
    )
