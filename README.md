# enterprise-data-platform-aws
A production-grade, event-driven data platform on AWS supporting batch and streaming ingestion, lakehouse storage, governance, and SLAs.

This repository contains the design and implementation of a production-grade enterprise data platform built on AWS.
The platform supports high-volume batch and streaming ingestion, schema-enforced lakehouse storage, data quality guarantees, and operational SLAs, with a strong focus on scalability, reliability, and cost efficiency.

Architecture Flow:

┌───────────────────────────────────────────────────────────┐
│                     PRODUCER SYSTEMS                      │
│  (Applications, Microservices, External Partners, APIs)   │
└───────────────┬───────────────────────────┬──────────────┘
                │                           │
        Streaming Events               Batch Data
     (JSON / Avro Events)        (API Pulls / File Drops)
                │                           │
┌───────────────▼──────────────┐   ┌────────▼────────┐
│ Amazon Kinesis Data Streams  │   │   Airflow (MWAA) │
│  - Ordered ingestion         │   │  - Scheduling    │
│  - Backpressure handling    │   │  - Retries       │
│  - Spike absorption         │   │  - Dependency mgmt│
└───────────────┬──────────────┘   └────────┬────────┘
                │                           │
                └──────────────┬────────────┘
                               │
                    AWS Glue (Apache Spark)
           - Streaming & Batch Processing
           - Schema enforcement
           - Deduplication
           - Idempotent writes
                               │
        ┌──────────────────────┴──────────────────────┐
        │                AMAZON S3 LAKEHOUSE           │
        │            (Apache Iceberg Table Format)     │
        │                                              │
        │   ┌────────────┐  ┌────────────┐  ┌────────┐│
        │   │   BRONZE   │  │   SILVER   │  │  GOLD  ││
        │   │ Raw Events │  │ Clean Data │  │ Marts  ││
        │   │ Immutable  │  │ Validated  │  │ KPIs   ││
        │   └────────────┘  └────────────┘  └────────┘│
        └──────────────────────┬──────────────────────┘
                               │
                   AWS Glue Data Catalog
            - Schemas & metadata
            - Table discovery
            - Engine decoupling
                               │
                         Amazon Athena
              - Ad-hoc analytics
              - BI / reporting access
                               │
                     Analysts / Consumers
