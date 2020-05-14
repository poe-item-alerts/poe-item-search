resource "aws_iam_role" "poe_item_search" {
  name               = "poe_item_search_execution"
  assume_role_policy = file("policies/lambda_assume_role.json")
  tags               = var.tags
}

resource "aws_iam_policy" "poe_item_search_execution" {
  name        = "poe_item_search_execution"
  description = "Allows the poe_item_search function to query the graphql endpoint"
  policy      = file("policies/poe_item_search.json")
}

resource "aws_iam_role_policy_attachment" "poe_item_search" {
  role       = aws_iam_role.poe_item_search.name
  policy_arn = aws_iam_policy.poe_item_search_execution.arn
}

resource "aws_iam_role_policy_attachment" "poe_api_exporter_lambda_basic_execution" {
  role       = aws_iam_role.poe_item_search.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
