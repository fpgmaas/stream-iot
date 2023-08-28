# Terraform

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

## Local development

For local development, initialize the project with:

```sh
terraform init -backend=false
```
