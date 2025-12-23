# Monitoring & Observability

This directory contains the operational monitoring components for the
Enterprise Data Platform.

The platform follows a **data-driven observability model**, where pipeline
health and dataset freshness are tracked using metadata tables rather than
hard-coded alerts inside jobs.

---

## Design Principles

- Monitoring is **decoupled** from processing logic
- Operational state is stored as **queryable data**
- Observability must support **replay and backfills**
- Metrics should be consumable by humans and tools

---

## What Is Tracked

### 1. Job Executions

The `monitoring.job_runs` table captures execution-level metadata for all
ingestion and processing jobs.

Tracked attributes include:
- Job name and type (streaming or batch)
- Dataset affected
- Execution status (STARTED, SUCCESS, FAILED)
- Start and end timestamps
- Records processed
- Error messages (if any)

This enables:
- Failure analysis
- Runtime trending
- SLA verification

---

### 2. Dataset Health

The `monitoring.dataset_status` table tracks dataset-level health indicators.

Examples:
- Last successful update time
- Record counts
- Freshness in minutes

This table serves as the **single source of truth** for downstream consumers
and monitoring dashboards.

---

## How Monitoring Is Used

Monitoring data is queried using Amazon Athena and can be consumed by:
- Platform operators
- Data consumers
- BI dashboards
- Alerting systems (external)

Example use cases:
- Detect stale datasets
- Identify recurring job failures
- Track ingestion volume anomalies

---

## Why This Approach

Instead of embedding alerting logic directly into pipelines, this platform
exposes operational signals as data. This makes monitoring:
- Auditable
- Extensible
- Easy to reason about
- Consistent across jobs

This approach scales better than pipeline-specific logging as the platform grows.

---

## Extensibility

Future enhancements may include:
- Automated SLA checks
- Integration with alerting systems
- Dashboarding on top of metadata tables
- Historical trend analysis

These are intentionally out of scope for the initial implementation.