# kafka-dev

## Prerequisites

- You have [az cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed.
- You have kubectl installed with [`az aks install-cli`](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli#connect-to-the-cluster).

## Installation

### Creating the Service Principal

Start by creating a Service Principal on Azure:

```sh
az login

export SUBSCRIPTION_ID=$(az account show --query id -o tsv)

az ad sp create-for-rbac \
    --name GitHubServicePrincipal \
    --role "Owner" \
    --scopes "/subscriptions/$SUBSCRIPTION_ID" > credentials.json
```

Then, run the following commands and set the displayed key-value pairs as Secrets in the GitHub repository:

```sh
echo "GitHub secrets:"
echo AZURE_AD_CLIENT_ID = `cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["appId"])'`
echo AZURE_AD_CLIENT_SECRET = `cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["password"])'`
echo AZURE_AD_TENANT_ID = `cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["tenant"])'`
echo AZURE_SUBSCRIPTION_ID = `az account show --query id -o tsv`
```

### Deploying infrastructure on Azure

Deploy the Terraform state bucket on Azure by navigating to `Actions` in the GitHub repository. There, run the `Terraform: Deploy state bucket` workflow. This creates a Blob container to hold our Terraform state.

When that is finished, deploy the infrastructure on Azure by similarly running the `Terraform: Deploy infrastructure` workflow.

### Installing Kafka

Locally, login to the created AKS cluster:

```
az aks get-credentials --resource-group floapp001-rg --name floapp001aks
```

Then, create a namespace called Kafka:

```
kubectl create namespace kafka
```

Install the [Strimzi Operator](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator):

```
helm install my-strimzi-cluster-operator oci://quay.io/strimzi-helm/strimzi-kafka-operator -n kafka -f kafka/values-strimzi.yaml
```

Then, install Kafka:

```
kubectl apply -n kafka -f kafka/values.yaml
```



push container to ACR workflow

Install Airflow

deploy key

ssh-keygen -t rsa -b 4096 -C "your@email.com"
cat ~/.ssh/airflowsshkey.pub
`Settings > Deploy Keys > Add deploy key`
kubectl create namespace airflow

```
export STORAGE_ACCOUNT_KEY=$(az storage account keys list \
-g floapp001-rg \
-n floapp001 \
--query '[0]'.value \
-o tsv)

kubectl create secret generic -n airflow storage-account-credentials \
--from-literal azurestorageaccountname=floapp001 \
--from-literal azurestorageaccountkey=$STORAGE_ACCOUNT_KEY \
--type=Opaque
```

az resource update --ids /subscriptions/${SUBSCRIPTION_ID}/resourcegroups/floapp001-rg/providers/Microsoft.ContainerService/managedClusters/floapp001aks/agentpools/default



## Local development

Get public IP of your cluster. Add that to python/app/config.py in the LocalConfig.

```
export CLUSTER_NAME=my-cluster
kubectl get service/$CLUSTER_NAME-kafka-external-bootstrap --output=jsonpath='{.status.loadBalancer.ingress[0].ip}' -n kafka
```


get certificate, Make sure they are in .gitignore!

```
export CLUSTER_NAME=my-cluster
kubectl get secret -n kafka $CLUSTER_NAME-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt
```

```
cd python
docker build -t floapp001 .

# Run producer
docker run \
    -e ENVIRONMENT=local \
    -v $(pwd)/../ca.crt:/code/ca.crt floapp001 \
    poetry run python -u app/producer.py


# Run consumer
docker run \
    -e ENVIRONMENT=local \
    -v $(pwd)/../ca.crt:/code/ca.crt floapp001 \
    poetry run python -u app/consumer.py
```

interactive mode:

```
docker run --rm -it \
    -e ENVIRONMENT=local \
    -v $(pwd)/../ca.crt:/code/ca.crt \
    --entrypoint bash floapp001
```
