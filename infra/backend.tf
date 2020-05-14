terraform {
  backend "s3" {
    bucket = "poe-item-alerts-state"
    key    = "poe-item-alerts/poe-item-search.tfstate"
    region = "eu-central-1"
    acl    = "bucket-owner-full-control"
  }
}
