from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

default_args = {
    "retries": 1,
    "start_date": datetime(2022, 1, 1),
    "image_pull_policy": "Always",
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