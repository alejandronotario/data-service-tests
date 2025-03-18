output "fire_damage_table" {
  description = "The name of the DynamoDB table 'fire_damage'"
  value       = aws_dynamodb_table.fire_damage.name
}

output "predictions_table" {
  description = "The name of the DynamoDB table 'Predictions'"
  value       = aws_dynamodb_table.predictions.name
}
