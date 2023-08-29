# Python

This directory contains Python code for a Kafka producer that generates some very simple mock IoT sensor data, and a consumer that stores that data in CosmosDB.

## Installation

Push the Docker image to the Container Registry by running the `Push Docker image` workflow in GitHub Actions.

## Local development

Locally, add it to `python/.env`:

```
export COSMOSDB_CONNECTION_STRING=$(az cosmosdb keys list \
    --name streamiotcosmosdb \
    --resource-group streamiot-rg \
    --type connection-strings \
    --query "connectionStrings[?description=='Primary MongoDB Connection String'].connectionString" \
    --output tsv)

echo "COSMOSDB_CONNECTION_STRING=\"$COSMOSDB_CONNECTION_STRING\"" > .env
echo "ENVIRONMENT=local" >> .env
```

Also add it as kubernetes secret in airflow namespace.

```
kubectl create secret generic \
    -n airflow cosmosdb-connection-string \
    --from-literal=cosmosdb-connection-string=$COSMOSDB_CONNECTION_STRING
```

Additionally, add the external IP of the Kafka cluster's load balancer to `LocalConfig` in `python/app/config.py`. It can be found with the following command:

```sh
export CLUSTER_NAME=my-cluster
kubectl get service/$CLUSTER_NAME-kafka-external-bootstrap --output=jsonpath='{.status.loadBalancer.ingress[0].ip}' -n kafka
```

We also download the certificate to our `python` directory.

```sh
export CLUSTER_NAME=my-cluster
kubectl get secret -n kafka $CLUSTER_NAME-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt
```

Now, to build the Docker image:

```sh
docker build -t streamiot .
```

To run the **producer**:

```sh
docker run \
    --env-file ./.env \
    -v $(pwd)/ca.crt:/code/ca.crt streamiot \
    poetry run python -u app/producer.py
```

To run the **consumer**:

```sh
docker run \
    --env-file ./.env \
    -v $(pwd)/ca.crt:/code/ca.crt streamiot \
    poetry run python -u app/consumer.py
```

To spin up the container in interactive mode:

```sh
docker run --rm -it \
    --env-file ./.env \
   -v $(pwd)/ca.crt:/code/ca.crt \
    --entrypoint bash streamiot
```
