### Installing Kafka

Locally, login to the AKS cluster:

```sh
az aks get-credentials --resource-group floapp001-rg --name floapp001aks
```

Then, create a namespace called Kafka:

```sh
kubectl create namespace kafka
```

Install the [Strimzi Operator](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator):

```sh
helm install my-strimzi-cluster-operator oci://quay.io/strimzi-helm/strimzi-kafka-operator -n kafka -f kafka/values-strimzi.yaml
```

Then, install our Kafka cluster:

```sh
kubectl apply -n kafka -f kafka/values.yaml
```
