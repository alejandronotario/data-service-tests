resource "aws_dynamodb_table" "fire_damage" {
  name         = var.fire_damage_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "OBJECTID"

  attribute {
    name = "OBJECTID"
    type = "N"
  }
}

resource "aws_dynamodb_table" "predictions" {
  name         = var.predictions_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "N"
  }
}
