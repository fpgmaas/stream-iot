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



Set ACR_REGISTRY_NAME variable on Github repo
also set APP_NAME

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