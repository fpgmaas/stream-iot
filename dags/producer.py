from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import models as k8s

default_args = {
    "retries": 1,
    "start_date": datetime(2022, 1, 1),
    "image_pull_policy": "Always",
    "env_vars": [k8s.V1EnvVar(name="ENVIRONMENT", value="cluster")],
}

with DAG(
    dag_id="producer",
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    tags=["example"],
    max_active_runs=1,
) as dag:
    simple_task = KubernetesPodOperator(
        task_id="produce",
        image="floapp001acr.azurecr.io/floapp001:latest",
        cmds=["python", "app/producer.py"],
    )
