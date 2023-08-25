resource "azurerm_resource_group" "rg" {
  name     = "${var.app_name}-rg"
  location = var.location
}

module "blob" {
  source               = "./modules/blob"
  storage_account_name = var.app_name
  resource_group_name  = azurerm_resource_group.rg.name
  location             = var.location
}

module "containerregistry" {
  source              = "./modules/container-registry"
  name                = "${var.app_name}acr"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}

module "aks" {
  source                = "./modules/aks"
  name                  = "${var.app_name}aks"
  container_registry_id = module.containerregistry.container_registry_id
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
}