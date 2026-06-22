variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Prefix used to name and tag resources"
  type        = string
  default     = "receipt-vault"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "db_password" {
  description = "Master password for the RDS Postgres instance"
  type        = string
  sensitive   = true
}

variable "db_username" {
  description = "Master username for the RDS Postgres instance"
  type        = string
  default     = "receipts"
}

variable "db_name" {
  description = "Initial database name"
  type        = string
  default     = "receipts"
}

variable "private_subnet_b_cidr" {
  description = "CIDR for a second private subnet in another AZ (RDS requirement)"
  type        = string
  default     = "10.0.3.0/24"
}