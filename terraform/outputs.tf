output "ecr_api_url" {
  description = "ECR repository URL for the API image"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_worker_url" {
  description = "ECR repository URL for the worker image"
  value       = aws_ecr_repository.worker.repository_url
}

output "alb_url" {
  description = "Public URL of the API via the load balancer"
  value       = "http://${aws_lb.main.dns_name}"
}