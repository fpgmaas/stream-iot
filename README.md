# kafka-dev

https://dev.to/azure/kafka-on-kubernetes-the-strimzi-way-part-2-1210

```
az login

export SUBSCRIPTION_ID=$(az account show --query id -o tsv)
export SERVICE_PRINCIPAL_NAME="GitHubServicePrincipal"
 
az ad sp create-for-rbac \
    --name $SERVICE_PRINCIPAL_NAME \
    --role "Owner" \
    --scopes "/subscriptions/$SUBSCRIPTION_ID" > credentials.json
```

set github secrets

```
echo "GitHub secrets:"
echo AZURE_AD_CLIENT_ID = `cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["appId"])'`
echo AZURE_AD_CLIENT_SECRET = `cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["password"])'`
echo AZURE_AD_TENANT_ID = `cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["tenant"])'`
echo AZURE_SUBSCRIPTION_ID = `az account show --query id -o tsv`
```

run deploy terraform state bucket workflow. (to get credentials locally):

```
export ARM_CLIENT_ID=`cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["appId"])'`
export ARM_CLIENT_SECRET=`cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["password"])'`
export ARM_TENANT_ID=`cat credentials.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["tenant"])'`
export ARM_SUBSCRIPTION_ID=`az account show --query id -o tsv`
```

deploy infra

```
az aks get-credentials --resource-group floapp001-rg --name floapp001aks
```


```
kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl apply -n kafka -f kafka/values.yaml
```

```
kubectl get service/${CLUSTER_NAME}-kafka-external-bootstrap --output=jsonpath='{.status.loadBalancer.ingress[0].ip}' -n kafka
```
ip: 20.23.114.182

```
export CLUSTER_NAME=my-cluster
kubectl get secret -n kafka $CLUSTER_NAME-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt
kubectl get secret -n kafka $CLUSTER_NAME-cluster-ca-cert -o jsonpath='{.data.ca\.password}' | base64 --decode > ca.password
```