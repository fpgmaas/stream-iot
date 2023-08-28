from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.kubernetes.secret import Secret
from kubernetes.client import models as k8s


cosmosdb_connection_string = Secret(
    deploy_type="env",
    deploy_target="COSMOSDB_CONNECTION_STRING",
    secret="cosmosdb-connection-string",  # noqa: S106
    key="cosmosdb-connection-string",
)

default_args = {
    "retries": 1,
    "start_date": datetime(2022, 1, 1),
    "image_pull_policy": "Always",
    "secrets": [cosmosdb_connection_string],
    "env_vars": [k8s.V1EnvVar(name="ENVIRONMENT", value="cluster")],
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
        image="floapp001acr.azurecr.io/floapp001:latest",
        cmds=["python", "app/consumer.py"],
    )
