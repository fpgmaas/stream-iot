data "azurerm_client_config" "current" {
}

data "azuread_client_config" "current" {
}

# Github Actions

resource "azuread_application" "github" {
  display_name = "${var.name}-github"
  owners       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal" "github" {
  application_id               = azuread_application.github.application_id
  app_role_assignment_required = false
  owners                       = [data.azuread_client_config.current.object_id]
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "azuread_application_password" "github_app_secret" {
  display_name = "terraformgenerated"
  application_object_id = azuread_application.github.object_id
}

output "github_service_principal_object_id" {
  value = azuread_service_principal.github.object_id
}

output "github_application_id" {
  value = azuread_application.github.application_id
}

output "github_application_secret" {
  value = azuread_application_password.github_app_secret.value
}