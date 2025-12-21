resource "aws_glue_catalog_database" "bronze" {
  name = "bronze_${var.environment}"
}

resource "aws_glue_catalog_database" "silver" {
  name = "silver_${var.environment}"
}

resource "aws_glue_catalog_database" "gold" {
  name = "gold_${var.environment}"
}