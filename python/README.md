# Python

This directory contains Python code for a Kafka producer that generates some very simple mock IoT sensor data, and a consumer that stores that data in CosmosDB.

## Installation

Push the Docker image to the Container Registry by running the `Push Docker image` workflow in GitHub Actions.

Also add `MONGODB_CONNECTION_STRING` as a secret in Kubernetes:

```sh
export MONGODB_CONNECTION_STRING=$(az cosmosdb keys list \
    --name streamiotcosmosdb \
    --resource-group streamiot-rg \
    --type connection-strings \
    --query "connectionStrings[?description=='Primary MongoDB Connection String'].connectionString" \
    --output tsv)

kubectl create secret generic \
    -n airflow mongodb-connection-string \
    --from-literal=mongodb-connection-string=$MONGODB_CONNECTION_STRING
```

## Local development

It is also possible to run the Kafka consumer and producer locally using Docker. To do so, start by navigating into the `python` directory.
There, create a `.env` file with the following command:

```
export MONGODB_CONNECTION_STRING=$(az cosmosdb keys list \
    --name streamiotcosmosdb \
    --resource-group streamiot-rg \
    --type connection-strings \
    --query "connectionStrings[?description=='Primary MongoDB Connection String'].connectionString" \
    --output tsv)

echo "MONGODB_CONNECTION_STRING=\"$MONGODB_CONNECTION_STRING\"" > .env
echo "ENVIRONMENT=local" >> .env
```

Additionally, manually add the external IP of the Kafka cluster's load balancer to `LocalConfig` in `app/config.py`.
It can be found with the following command:

```sh
export CLUSTER_NAME=my-cluster
kubectl get service/$CLUSTER_NAME-kafka-external-bootstrap --output=jsonpath='{.status.loadBalancer.ingress[0].ip}' -n kafka
```

We also download the certificate to our `python` directory:

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
