# Data Model: OmniRetail Commerce Platform

## 1. Overview

The logical data model represents the core retail entities and their relationships.

## 2. Entities

### Customer

Primary key:

- `customer_id`

Represents a customer purchasing through a store, website, or mobile application.

### Store

Primary key:

- `store_id`

Represents a physical or fulfilment retail location.

### Supplier

Primary key:

- `supplier_id`

Represents an organization supplying products.

### Product

Primary key:

- `product_id`

Foreign key:

- `supplier_id` references Supplier

Represents an item available for sale.

### Order

Primary key:

- `order_id`

Foreign keys:

- `customer_id` references Customer
- `store_id` references Store

Represents a customer purchase transaction.

### Order Item

Primary key:

- `order_item_id`

Foreign keys:

- `order_id` references Order
- `product_id` references Product

Represents an individual product line within an order.

### Inventory

Primary key:

- `inventory_id`

Foreign keys:

- `store_id` references Store
- `product_id` references Product

Represents the quantity of a product held at a store.

### Promotion

Primary key:

- `promotion_id`

Foreign key:

- `product_id` references Product

Represents a time-bound offer applied to a product.

## 3. Relationships

```text
Supplier 1 ───────< Product

Customer 1 ───────< Order >─────── 1 Store

Order 1 ──────────< Order Item >── 1 Product

Store 1 ──────────< Inventory >─── 1 Product

Product 1 ────────< Promotion
```

## 4. Referential Integrity

The synthetic data generator creates child records using identifiers obtained from their parent datasets.

This ensures that:

Every product references an existing supplier.
Every order references an existing customer and store.
Every order item references an existing order and product.
Every inventory record references an existing store and product.
Every promotion references an existing product.