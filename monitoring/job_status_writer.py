from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from uuid import uuid4

def write_job_status(
    spark: SparkSession,
    job_name: str,
    job_type: str,
    dataset: str,
    status: str,
    records_processed: int = None,
    error_message: str = None
):
    run_id = str(uuid4())

    df = spark.createDataFrame([{
        "job_name": job_name,
        "job_type": job_type,
        "dataset": dataset,
        "run_id": run_id,
        "status": status,
        "start_time": current_timestamp(),
        "end_time": current_timestamp(),
        "records_processed": records_processed,
        "error_message": error_message
    }])

    (
        df.writeTo("glue_catalog.monitoring.job_runs")
        .append()
    )