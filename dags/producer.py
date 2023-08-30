from datetime import datetime, timedelta
from airflow import DAG
from kubernetes.client import (
    V1Affinity,
    V1NodeAffinity,
    V1NodeSelector,
    V1NodeSelectorRequirement,
    V1NodeSelectorTerm,
)
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
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

# Default arguments for the DAG
default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=5),  # Add this if needed
    "start_date": datetime(2022, 1, 1),
    "image_pull_policy": "Always",
    "env_vars": [k8s.V1EnvVar(name="ENVIRONMENT", value="cluster")],
    "affinity": affinity,
}

# DAG definition
with DAG(
    dag_id="producer",
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    tags=["example"],
    max_active_runs=1,
) as dag:
    run_data_producer = KubernetesPodOperator(
        task_id="run_data_producer",
        image="streamiotacr.azurecr.io/streamiot:latest",
        cmds=["python", "app/producer.py"],
        container_resources=memory_request,
    )
