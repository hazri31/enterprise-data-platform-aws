import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    current_timestamp,
    to_date
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType,
    DecimalType,
    ArrayType,
    IntegerType
)

from config import (
    KINESIS_STREAM_NAME,
    GLUE_DATABASE,
    ICEBERG_TABLE,
    S3_WAREHOUSE_PATH,
    CHECKPOINT_PATH,
    SPARK_APP_NAME
)

# ---------------------------
# Spark Session
# ---------------------------
spark = (
    SparkSession.builder
    .appName(SPARK_APP_NAME)
    .config(
        "spark.sql.catalog.glue_catalog",
        "org.apache.iceberg.spark.SparkCatalog"
    )
    .config(
        "spark.sql.catalog.glue_catalog.warehouse",
        S3_WAREHOUSE_PATH
    )
    .config(
        "spark.sql.catalog.glue_catalog.catalog-impl",
        "org.apache.iceberg.aws.glue.GlueCatalog"
    )
    .config(
        "spark.sql.catalog.glue_catalog.io-impl",
        "org.apache.iceberg.aws.s3.S3FileIO"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ---------------------------
# Event Schema (Contract)
# ---------------------------
order_created_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_time", TimestampType(), False),
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("order_total", DecimalType(10, 2), False),
    StructField("currency", StringType(), False),
    StructField("source_system", StringType(), False),
    StructField(
        "items",
        ArrayType(
            StructType([
                StructField("sku", StringType(), False),
                StructField("quantity", IntegerType(), False),
                StructField("unit_price", DecimalType(10, 2), False)
            ])
        ),
        True
    ),
    StructField("event_version", StringType(), False)
])

# ---------------------------
# Read from Kinesis
# ---------------------------
raw_stream = (
    spark.readStream
    .format("kinesis")
    .option("streamName", KINESIS_STREAM_NAME)
    .option("startingPosition", "LATEST")
    .option("inferSchema", "false")
    .load()
)

# Kinesis payload is binary
json_stream = raw_stream.selectExpr(
    "CAST(data AS STRING) AS json_payload"
)

# ---------------------------
# Schema Enforcement
# ---------------------------
parsed_stream = (
    json_stream
    .select(
        from_json(
            col("json_payload"),
            order_created_schema
        ).alias("event"),
        col("json_payload").alias("raw_payload")
    )
    .select(
        "event.*",
        "raw_payload"
    )
)

# ---------------------------
# Add Ingestion Metadata
# ---------------------------
bronze_df = (
    parsed_stream
    .withColumn("ingest_time", current_timestamp())
    .withColumn("ingest_date", to_date(col("ingest_time")))
)

# ---------------------------
# Write to Iceberg (Bronze)
# ---------------------------
query = (
    bronze_df.writeStream
    .format("iceberg")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_PATH)
    .toTable(f"glue_catalog.{GLUE_DATABASE}.{ICEBERG_TABLE}")
)

query.awaitTermination()