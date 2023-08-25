terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.name

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  storage_profile {
    blob_driver_enabled = true
  }

    auto_scaler_profile {
    # (Optional) Maximum number of seconds the cluster autoscaler waits for pod termination when trying to scale down a node. Defaults to 600.
    max_graceful_termination_sec = 180
    # (Optional) How long after the scale up of AKS nodes the scale down evaluation resumes. Defaults to 10m.)
    scale_down_delay_after_add = "3m"
    # - (Optional) How long a node should be unneeded before it is eligible for scale down. Defaults to 10m.
    scale_down_unneeded = "3m"
    # (Optional) If true cluster autoscaler will never delete nodes with pods from kube-system (except for DaemonSet or mirror pods). Defaults to true.
    # metrics server is not Daemonset, so will not allow scale down.
    skip_nodes_with_system_pods = false
    # (Optional) If true cluster autoscaler will never delete nodes with pods with local storage, for example, EmptyDir or HostPath. Defaults to true.
    skip_nodes_with_local_storage = false
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "application" {
  name                  = "application"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_B2ms"
  enable_auto_scaling   = true
  min_count             = 0
  max_count             = 1
  node_labels = {
    "type" = "application"
  }
}

resource "azurerm_role_assignment" "main" {
  principal_id                     = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = var.container_registry_id
  skip_service_principal_aad_check = true
}