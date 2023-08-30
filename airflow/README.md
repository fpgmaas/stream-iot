# Airflow

## Installation

First, create a namespace:

```sh
kubectl create namespace airflow
```

### DAG synchronization

Our DAG's are stored in the `dags` folder of this project. To enable synchronization between GitHub and Airflow using GitSync,
we use a deploy key. To create a new deploy key, navigate to `~/.ssh` and run:

```sh
ssh-keygen -t rsa -b 4096 -C "your@email.com"
```

As the name, choose airflowsshkey, and do not set a password. Now, print the public key to the console:

```sh
cat ~/.ssh/airflowsshkey.pub
```

Add the public key as a deploy key to your GitHub repository (`Settings > Deploy Keys > Add deploy key`).

Now we need to add the private key as a secret to our Kubernetes cluster. Before we do so, let's create a namespace
for all our Airflow resources:

```sh
kubectl create namespace airflow
```

Then, let's create a secret called airflow-git-ssh-secret in the airflow namespace in kubernetes:

```sh
kubectl create secret generic -n airflow airflow-git-ssh-secret \
  --from-file=gitSshKey=$HOME/.ssh/airflowsshkey
```

### Storage account credentials

First, add the storage account credentials as a secret. These credentials are needed for log storage in our Blob container.

```sh
export STORAGE_ACCOUNT_KEY=$(az storage account keys list \
-g streamiot-rg \
-n streamiot \
--query '[0]'.value \
-o tsv)

kubectl create secret generic -n airflow storage-account-credentials \
--from-literal azurestorageaccountname=streamiot \
--from-literal azurestorageaccountkey=$STORAGE_ACCOUNT_KEY \
--type=Opaque
```

Now, we can create the PersistentVolume and the PersistentVolumeClaim:

```sh
kubectl apply -n airflow -f airflow/pv-logs.yaml
kubectl apply -n airflow -f airflow/pvc-logs.yaml
```

Now, install Airflow using Helm:

```sh
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow -n airflow -f airflow/values.yaml --debug
```

Fnally, our future DAG's will need access to out CosmosDB instance. In order to enable this connection, store the connection string as a secret in Kubernetes:


```sh
export MONGODB_CONNECTION_STRING=$(az cosmosdb keys list \
    --name streamiotcosmosdb \
    --resource-group streamiot-rg\
    --type connection-strings \
    --query "connectionStrings[?description=='Primary MongoDB Connection String'].connectionString" \
    --output tsv)

kubectl create secret generic \
    -n airflow mongodb-connection-string \
    --from-literal=MONGODB_CONNECTION_STRING=$MONGODB_CONNECTION_STRING
```

## Accessing the UI

To access the webserver, run:

```sh
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```

and visit `localhost:8080` in your browser.
