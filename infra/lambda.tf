resource "aws_lambda_function" "poe_item_search" {
  filename      = "../src/poe_item_search-${var.commit_sha}.zip"
  function_name = "poe_item_search"
  description   = "Queries the existing item cache and returns filtered results"
  role          = aws_iam_role.poe_item_search.arn
  handler       = "poe_item_search.handler.handler"
  runtime       = var.lambda_config["runtime"]
  timeout       = var.lambda_config["timeout"]
  memory_size   = var.lambda_config["memory_size"]
  tags          = var.tags
  
  environment {
    variables = {
      LOG_LEVEL = var.lambda_config["log_level"]
    }
  }

  dead_letter_config {
    target_arn = aws_sns_topic.deadletter.arn
  }
}
