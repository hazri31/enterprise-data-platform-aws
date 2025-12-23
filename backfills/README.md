# Replay & Backfill Strategy

This directory contains scripts and documentation related to replaying and
backfilling data in the Enterprise Data Platform.

The platform is designed to support **safe, deterministic reprocessing**
without manual data manipulation.

---

## Core Principle

**Bronze data is immutable.**

All replay and backfill operations originate from Bronze and flow forward
through Silver and Gold layers.

This guarantees:
- Reproducibility
- Auditability
- Consistency across datasets

---

## When Replays Are Required

Replays may be triggered due to:
- Late-arriving events
- Upstream data corrections
- Bug fixes in transformation logic
- Changes to business metrics
- Historical backfills

---

## Replay Scenarios

### Bronze → Silver Replay

Used when:
- Late data arrives
- Deduplication logic changes
- Schema enforcement rules are updated

Mechanism:
- Re-run the existing Bronze → Silver job
- Iceberg MERGE ensures idempotent upserts
- No duplicate records are introduced

---

### Silver → Gold Replay

Used when:
- Metric definitions change
- Aggregation logic is updated
- Gold tables need to be rebuilt

Mechanism:
- Re-run the Silver → Gold job
- Gold tables are rebuilt deterministically
- No direct mutation of Gold data

---

## Backfill Scope Control

Replay scripts accept date ranges to limit scope and cost.

Typical controls:
- Lookback windows (hours or days)
- Dataset-specific reprocessing
- Partition-level overwrites

This avoids full-table scans unless explicitly required.

---

## What Is Explicitly Avoided

- Manual deletes in S3
- Ad-hoc table rewrites
- Partial fixes in Gold
- One-off pipelines for corrections

All fixes go through the same canonical jobs.

---

## Operational Guidance

Before triggering a replay:
- Identify the impacted dataset and layer
- Validate the time window affected
- Communicate expected downstream impact

After replay:
- Verify dataset health via monitoring tables
- Confirm metrics consistency

---

## Why This Matters

Replayability is a **first-class requirement** for enterprise data platforms.

This strategy ensures that:
- Data issues can be corrected safely
- Platform behavior is predictable
- Historical accuracy is maintained