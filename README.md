# kafka-dev

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