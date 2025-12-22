AWS_REGION = "us-east-1"

KINESIS_STREAM_NAME = "enterprise-events-dev"

GLUE_DATABASE = "bronze_dev"
ICEBERG_TABLE = "bronze_order_created"

S3_WAREHOUSE_PATH = "s3://enterprise-data-platform-dev/"

CHECKPOINT_PATH = (
    "s3://enterprise-data-platform-dev/checkpoints/bronze/order_created/"
)

SPARK_APP_NAME = "bronze-order-created-streaming-job"