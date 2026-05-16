variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for naming resources"
  type        = string
  default     = "cloud-infra-monitor"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "db_username" {
  description = "RDS database username"
  type        = string
  default     = "appuser"
}

variable "db_password" {
  description = "RDS database password"
  type        = string
  sensitive   = true
}