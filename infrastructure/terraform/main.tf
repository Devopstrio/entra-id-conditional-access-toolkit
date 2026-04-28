provider "azurerm" {
  features {}
}

provider "azuread" {
  # Configuration for Microsoft Graph automation
}

# --- Identity Foundation (Azure) ---

resource "azurerm_resource_group" "identity" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Identity Toolkit Control Plane (Azure Container Apps) ---

resource "azurerm_container_app_environment" "identity" {
  name                = "cae-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.identity.location
  resource_group_name = azurerm_resource_group.identity.name
}

# --- Institutional Identity Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "identity" {
  name                   = "psql-${var.project_name}-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.identity.name
  location               = azurerm_resource_group.identity.location
  version                = "13"
  administrator_login    = "identityadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Identity Secrets & Certificates ---

resource "azurerm_key_vault" "identity" {
  name                        = "kv-identity-${var.environment}"
  location                    = azurerm_resource_group.identity.location
  resource_group_name         = azurerm_resource_group.identity.name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}

# --- App Registrations for Graph API Automation ---

resource "azuread_application" "toolkit_sync" {
  display_name = "Entra-ID-Toolkit-Sync-Service"
  owners       = [var.admin_object_id]

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph

    resource_access {
      id   = "Policy.ReadWrite.ConditionalAccess"
      type = "Role"
    }

    resource_access {
      id   = "User.Read.All"
      type = "Role"
    }
  }
}
