from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    current_timestamp,
    to_date,
    row_number
)
from pyspark.sql.window import Window

from config import (
    BRONZE_DB,
    SILVER_DB,
    BRONZE_TABLE,
    SILVER_TABLE,
    S3_WAREHOUSE_PATH,
    PROCESSING_LOOKBACK_HOURS,
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
# Read Bronze Table
# ---------------------------
bronze_df = spark.read.table(
    f"glue_catalog.{BRONZE_DB}.{BRONZE_TABLE}"
)

# ---------------------------
# Filter Processing Window
# ---------------------------
filtered_df = bronze_df.filter(
    col("ingest_time") >=
    current_timestamp() - expr(f"INTERVAL {PROCESSING_LOOKBACK_HOURS} HOURS")
)

# ---------------------------
# Deduplication
# ---------------------------
window_spec = Window.partitionBy("event_id").orderBy(
    col("ingest_time").desc()
)

deduped_df = (
    filtered_df
    .withColumn("row_num", row_number().over(window_spec))
    .filter(col("row_num") == 1)
    .drop("row_num")
)

# ---------------------------
# Silver Projection
# ---------------------------
silver_df = (
    deduped_df
    .select(
        "event_id",
        "event_time",
        "order_id",
        "customer_id",
        "order_total",
        "currency",
        "source_system",
        "items"
    )
    .withColumn("event_date", to_date(col("event_time")))
    .withColumn("processing_time", current_timestamp())
)

silver_df.createOrReplaceTempView("silver_updates")

# ---------------------------
# Upsert into Silver (Iceberg MERGE)
# ---------------------------
spark.sql(f"""
MERGE INTO glue_catalog.{SILVER_DB}.{SILVER_TABLE} target
USING silver_updates source
ON target.event_id = source.event_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")