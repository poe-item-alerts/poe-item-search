variable "aws_region" {
  description = "The region for the application environment - Default is Frankfurt as our main region"
  default     = "eu-central-1"
}

variable "commit_sha" {
  description = "Variable that is required to be set through `export TF_VAR_commit_short_sha=$(git rev-parse HEAD)` this will determine the source code zip for the lambda"
  type        = string
}

variable "lambda_config" {
  description = "Configuration of the deployed lambda function"
  type = object({
    memory_size = number,
    runtime     = string,
    timeout     = number,
    log_level   = string,
  })
  default = {
    memory_size = 512
    runtime     = "python3.7"
    timeout     = 600
    log_level   = "INFO"
  }
}

variable "tags" {
  description = "Common tags shared across all resources, specific tags are in the resources"
  type = object({
    Application = string,
    Component   = string
  })
  default = {
    Application = "poe-item-alerts"
    Component   = "poe-item-search"
  }
}

