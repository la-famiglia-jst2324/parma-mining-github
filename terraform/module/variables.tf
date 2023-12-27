variable "env" {
  description = "staging or prod environment"
  type        = string
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
}

variable "GITHUB_TOKEN" {
  description = "value"
  type        = string
  sensitive   = true
}

variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}
