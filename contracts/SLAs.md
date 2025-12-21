# Data Platform SLAs

This document defines Service Level Agreements (SLAs) for datasets
produced by the Enterprise Data Platform.

---

## 1. Streaming Datasets (Event-Driven)

### Example: `order_created` events

**Freshness**
- 99% of events available in Bronze within **5 minutes** of event_time

**Completeness**
- ≥ 99.9% of events published by producers are ingested successfully

**Availability**
- Platform ingestion availability ≥ 99.9%

**Late Data Handling**
- Events arriving up to **24 hours late** are accepted
- Events later than 24 hours are routed to a separate late-data stream

---

## 2. Batch Datasets (File-Based)

### Example: `partner_daily_snapshot`

**Freshness**
- Daily snapshot available in Bronze by **07:00 UTC**

**Completeness**
- All expected files must be received before Silver processing begins

**Availability**
- Batch ingestion success rate ≥ 99.5%

**Backfills**
- Historical files can be reprocessed without duplication

---

## 3. Silver Layer SLAs

**Data Quality**
- Schema validation enforced
- Primary key uniqueness guaranteed
- Null checks on required fields

**Latency**
- Silver tables available within **30 minutes** of Bronze availability

---

## 4. Gold Layer SLAs

**Availability**
- Gold datasets refreshed daily or near-real-time depending on use case

**Rebuild Guarantees**
- Gold tables are fully reproducible from Silver data

---

## 5. SLA Violations

SLA breaches trigger:
- Incident creation
- Consumer notification
- Root cause analysis

SLAs are reviewed quarterly and adjusted as platform scale evolves.