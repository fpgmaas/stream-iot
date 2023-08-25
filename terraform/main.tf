terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.70.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.app_name}-rg"
  location = var.location
}

module "serviceprincipals" {
  source = "./modules/service-principals"
  name   = var.app_name
}

module "blob" {
  source                             = "./modules/blob"
  storage_account_name               = var.app_name
  resource_group_name                = azurerm_resource_group.rg.name
  github_service_principal_object_id = module.serviceprincipals.github_service_principal_object_id
  location                           = var.location
}

module "keyvault" {
  source              = "./modules/keyvault"
  name                = "${var.app_name}keyvault"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}

module "containerregistry" {
  source                             = "./modules/container-registry"
  name                               = "${var.app_name}acr"
  github_service_principal_object_id = module.serviceprincipals.github_service_principal_object_id
  location                           = var.location
  resource_group_name                = azurerm_resource_group.rg.name
}

module "aks" {
  source                = "./modules/aks"
  name                  = "${var.app_name}aks"
  container_registry_id = module.containerregistry.container_registry_id
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
}

module "write_to_keyvault" {
  source            = "./modules/write-to-keyvault"
  depends_on        = [module.keyvault]
  key_vault_id      = module.keyvault.key_vault_id
  github_sp_app_id  = module.serviceprincipals.github_application_id
  github_app_secret = module.serviceprincipals.github_application_secret
}