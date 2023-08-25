data "azurerm_client_config" "current" {}

resource "azurerm_container_registry" "acr" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Standard"
  admin_enabled      = true
}

resource "azurerm_role_assignment" "github_container_app_access" {
  role_definition_name = "AcrPush"
  principal_id         = data.azurerm_client_config.current.object_id
  scope                = azurerm_container_registry.acr.id
}

output "container_registry_id" {
  value = azurerm_container_registry.acr.id
}