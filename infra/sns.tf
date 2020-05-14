resource "aws_sns_topic" "deadletter" {
  name = "poe_item_search_deadletter"
  tags = var.tags
}
