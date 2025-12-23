-- Job execution tracking
CREATE TABLE monitoring.job_runs (
                                     job_name STRING,
                                     job_type STRING,               -- streaming | batch
                                     dataset STRING,
                                     run_id STRING,
                                     status STRING,                 -- STARTED | SUCCESS | FAILED
                                     start_time TIMESTAMP,
                                     end_time TIMESTAMP,
                                     records_processed BIGINT,
                                     error_message STRING
)
    USING iceberg
PARTITIONED BY (days(start_time));

-- Dataset-level health
CREATE TABLE monitoring.dataset_status (
                                           dataset STRING,
                                           layer STRING,                  -- bronze | silver | gold
                                           last_success_time TIMESTAMP,
                                           last_record_count BIGINT,
                                           freshness_minutes INT
)
    USING iceberg;