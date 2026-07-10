# ADR-001: Use a Layered Data Platform Architecture

## Status

Accepted

## Context

The OmniRetail Commerce Platform will process data from multiple retail business domains, including customers, products, stores, suppliers, orders, order items, inventory, pricing, and promotions.

These datasets serve different purposes and arrive at different levels of quality. Raw source data must be preserved for auditability and reprocessing, while downstream users require cleaned, standardized, and analytics-ready datasets.

Using a single collection of transformed files would make it difficult to trace data issues, rerun processing, and separate operational data from business metrics.

## Decision

Use a layered data platform architecture with three logical stages:

- **Bronze layer:** stores raw ingested data with minimal transformation.
- **Silver layer:** stores cleaned, validated, standardized, and integrated retail data.
- **Gold layer:** stores business-ready datasets and metrics for analytics, reporting, and future machine-learning use cases.

Examples of Gold outputs include:

- Daily and monthly sales
- Revenue by product, store, and region
- Customer purchase behaviour
- Inventory availability and stock-out metrics
- Promotion effectiveness
- Forecasting-ready datasets

## Alternatives Considered

### Single processed dataset

This would be simpler initially, but it would mix raw, cleaned, and analytical data.

It was rejected because it provides weak auditability, makes debugging harder, and limits reprocessing.

### Traditional data warehouse only

A warehouse is suitable for analytical reporting, but using only a final warehouse model would not preserve raw source data or support flexible data processing before dimensional modelling.

It was rejected as the sole architecture, although dimensional warehouse models will still be created in the Gold layer.

### Direct reporting from operational source tables

This would reduce pipeline development, but operational schemas are designed for transactions rather than analytical queries.

It was rejected because it would create tight coupling to source systems and produce poor analytical performance and maintainability.

## Consequences

### Benefits

- Preserves raw retail data for auditing and reprocessing
- Separates ingestion, data quality, integration, and analytics concerns
- Makes pipeline failures easier to diagnose
- Supports multiple source systems and business domains
- Provides a clear path to dimensional modelling
- Supports future migration to distributed and cloud data platforms

### Trade-offs

- Requires additional storage
- Introduces more datasets and transformation stages
- Requires clear naming, lineage, and documentation
- Adds initial implementation effort compared with a single-script pipeline

## Review Trigger

Review this decision if:

- The platform moves to a different architectural pattern such as Data Vault
- Real-time operational workloads require a separate serving architecture
- Storage or processing costs make the current layering inefficient
- The platform adopts a managed lakehouse or warehouse design that changes layer responsibilities