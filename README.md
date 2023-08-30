# stream-iot

Welcome to **stream-iot**! This project contains an example of an end-to-end workflow for real-time IoT data processing.
The workflow consists of mocking sensor data, channeling it through Kafka, and then storing the parsed data in a MongoDB database.

I started this project as a way to learn and get some initial hands-on experience with Kafka. I hope that this project can help others get started on similar projects. At the same time, I am sure I can learn from others viewing this project. If you have feedback or improvement suggestions, please [create an issue](https://github.com/fpgmaas/stream-iot/issues/new) in this repository.


## Tools & Technologies

* Cloud - [**Azure**](https://azure.microsoft.com/en-us/)
* Infrastructure as Code - [**Terraform**](https://www.terraform.io/)
* Containerization - [**Docker**](https://www.docker.com/)
* Container Orchestration - [**Kubernetes**](https://kubernetes.io/)
* Monitoring - [**Prometheus**](https://prometheus.io), [**Grafana**](https://grafana.com/)
* Workflow Orchestration - [**Airflow**](https://airflow.apache.org/)
* Messaging & Stream Processing - [**Kafka**](https://kafka.apache.org/)
* Data Storage - [**CosmosDB**](https://azure.microsoft.com/en-us/products/cosmos-db), [**MongoDB**](https://www.mongodb.com)
* Languages - [**Python**](https://www.python.org/)


## Architecture

![Alt text](./architecture.png)


## Prerequisites

- You have [az cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed.
- You have kubectl installed with [`az aks install-cli`](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli#connect-to-the-cluster).

## Installation

Follow the installation instructions in the README's of these directories in order:

- [terraform](./terraform/README.md#installation)
- [kafka](./kafka/README.md#installation)
- [airflow](./airflow/README.md#installation)
- [python](./python/README.md)
- [monitoring](./monitoring/README.md) (optional)

When this is done, open the Airflow UI with

```sh
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```

and trigger the DAG's manually.
