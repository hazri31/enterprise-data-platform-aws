AWS_REGION = "us-east-1"

BRONZE_DB = "bronze_dev"
SILVER_DB = "silver_dev"

BRONZE_TABLE = "bronze_order_created"
SILVER_TABLE = "silver_order_created"

S3_WAREHOUSE_PATH = "s3://enterprise-data-platform-dev/"

# Process last N hours (supports backfills)
PROCESSING_LOOKBACK_HOURS = 48

SPARK_APP_NAME = "bronze-to-silver-order-created"