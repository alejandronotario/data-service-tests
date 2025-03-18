variable "fire_damage_table_name" {
  description = "DynamoDB table name for fire damage data"
  default     = "fire_damage"
}

variable "predictions_table_name" {
  description = "DynamoDB table name for predictions"
  default     = "Predictions"
}
