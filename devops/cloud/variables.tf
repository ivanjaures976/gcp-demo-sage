variable "project_id" {
  type        = string
  description = "ID del progetto GCP"
}

variable "resource_prefix" {
  type        = string
  description = "Prefisso per i nomi delle risorse"
}

variable "region" {
  type        = string
  description = "Regione GCP"
  default     = "europe-west6"
}