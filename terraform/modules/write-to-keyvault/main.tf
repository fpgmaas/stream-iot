resource "azurerm_key_vault_secret" "store_github_sp_app_id" {
  name         = "github-sp-app-id"
  value        = var.github_sp_app_id
  key_vault_id = var.key_vault_id
}

resource "azurerm_key_vault_secret" "store_github_app_secret" {
  name         = "github-sp-secret"
  value        = var.github_app_secret
  key_vault_id = var.key_vault_id
}