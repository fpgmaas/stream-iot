variable "name" {
  type        = string
  description = "Name of the Service Bus Namespace"
}

variable "location" {
  type        = string
  description = "Location where the Service Bus will be deployed"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the resource group that will contain the Service Bus"
}
