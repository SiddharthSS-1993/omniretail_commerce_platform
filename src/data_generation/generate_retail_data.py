from datetime import timedelta
from pathlib import Path
import random

import pandas as pd
from faker import Faker

OUTPUT_DIRECTORY = Path("data/generated/raw")

CUSTOMER_COUNT = 10000
PRODUCT_COUNT = 1000
STORE_COUNT = 50
SUPPLIER_COUNT = 100
ORDER_COUNT = 50000
PROMOTION_COUNT = 100

RANDOM_SEED = 42

fake_data_generator = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def create_customers(customer_count: int) -> pd.DataFrame:
    """Create synthetic customer master data"""

    customer_records = []

    customer_segments = ["Consumer",
                         "Small Business",
                         "Enterprise"]
    
    loyalty_tiers = ["Bronze",
                     "Silver",
                     "Gold",
                     "Platinum"]
    
    for customer_number in range(1, customer_count + 1):
        customer_records.append({"customer_id": f"C{customer_number:06d}",
                                 "customer_name": fake_data_generator.name(),
                                 "email_address": fake_data_generator.unique.email(),
                                 "phone_number": fake_data_generator.phone_number(),
                                 "city": fake_data_generator.city(),
                                 "country": fake_data_generator.country(),
                                 "customer_segment": random.choice(customer_segments),
                                 "loyalty_tier": random.choice(loyalty_tiers),
                                 "registration_date": fake_data_generator.date_between(
                                     start_date="-5y", end_date="today" 
                                 )
                                 })
        
    return pd.DataFrame(customer_records)


def create_stores(store_count: int) -> pd.DataFrame:
    """Create retail store reference data."""

    store_records = []

    store_formats = [
        "Flagship",
        "Mall",
        "Neighbourhood",
        "Online Fulfilment",
    ]

    for store_number in range(1, store_count + 1):
        store_records.append(
            {
                "store_id": f"S{store_number:04d}",
                "store_name": f"Store {store_number}",
                "city": fake_data_generator.city(),
                "country": fake_data_generator.country(),
                "store_format": random.choice(store_formats),
                "opening_date": fake_data_generator.date_between(
                    start_date="-15y",
                    end_date="-1y",
                ),
            }
        )

    return pd.DataFrame(store_records)


def create_suppliers(supplier_count: int) -> pd.DataFrame:
    """Create supplier master data."""

    supplier_records = []

    supplier_categories = [
        "Electronics",
        "Fashion",
        "Home",
        "Sports",
        "Food",
    ]

    for supplier_number in range(1, supplier_count + 1):
        supplier_records.append(
            {
                "supplier_id": f"SUP{supplier_number:04d}",
                "supplier_name": fake_data_generator.company(),
                "supplier_category": random.choice(supplier_categories),
                "country": fake_data_generator.country(),
                "contract_start_date": fake_data_generator.date_between(
                    start_date="-10y",
                    end_date="-1y",
                ),
            }
        )

    return pd.DataFrame(supplier_records)


def create_products(
    product_count: int,
    suppliers: pd.DataFrame,
) -> pd.DataFrame:
    """Create product master data linked to existing suppliers."""

    product_categories = [
        "Electronics",
        "Fashion",
        "Home",
        "Sports",
        "Food",
    ]

    product_subcategories = {
        "Electronics": [
            "Laptops",
            "Mobile Phones",
            "Headphones",
            "Gaming",
        ],
        "Fashion": [
            "Shirts",
            "Trousers",
            "Footwear",
            "Accessories",
        ],
        "Home": [
            "Furniture",
            "Kitchen",
            "Lighting",
            "Decor",
        ],
        "Sports": [
            "Fitness",
            "Outdoor",
            "Team Sports",
            "Sportswear",
        ],
        "Food": [
            "Snacks",
            "Beverages",
            "Packaged Food",
            "Organic Food",
        ],
    }

    supplier_ids = suppliers["supplier_id"].tolist()
    product_records = []

    for product_number in range(1, product_count + 1):
        product_category = random.choice(product_categories)
        product_subcategory = random.choice(
            product_subcategories[product_category]
        )

        unit_cost = round(random.uniform(50, 50000), 2)
        selling_price = round(
            unit_cost * random.uniform(1.10, 1.60),
            2,
        )

        product_records.append(
            {
                "product_id": f"P{product_number:06d}",
                "supplier_id": random.choice(supplier_ids),
                "product_name": (
                    f"{product_subcategory} Product {product_number}"
                ),
                "product_category": product_category,
                "product_subcategory": product_subcategory,
                "unit_cost": unit_cost,
                "selling_price": selling_price,
                "product_status": random.choice(
                    ["Active", "Discontinued"]
                ),
                "launch_date": fake_data_generator.date_between(
                    start_date="-8y",
                    end_date="today",
                ),
            }
        )

    return pd.DataFrame(product_records)


def create_orders(
    order_count: int,
    customers: pd.DataFrame,
    stores: pd.DataFrame,
) -> pd.DataFrame:
    """Create retail order transactions linked to customers and stores."""

    customer_ids = customers["customer_id"].tolist()
    store_ids = stores["store_id"].tolist()

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "UPI",
        "Net Banking",
        "Cash",
    ]

    order_statuses = [
        "Placed",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled",
        "Returned",
    ]

    sales_channels = [
        "Store",
        "Website",
        "Mobile Application",
    ]

    order_records = []

    for order_number in range(1, order_count + 1):
        order_timestamp = fake_data_generator.date_time_between(
            start_date="-2y",
            end_date="now",
        )

        order_records.append(
            {
                "order_id": f"O{order_number:08d}",
                "customer_id": random.choice(customer_ids),
                "store_id": random.choice(store_ids),
                "order_timestamp": order_timestamp,
                "sales_channel": random.choice(sales_channels),
                "payment_method": random.choice(payment_methods),
                "order_status": random.choice(order_statuses),
            }
        )

    return pd.DataFrame(order_records)

def create_order_items(
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Create order-item records linked to existing orders and products."""

    order_ids = orders["order_id"].tolist()

    product_lookup = products.set_index("product_id")[
        ["selling_price"]
    ].to_dict(orient="index")

    product_ids = list(product_lookup.keys())

    order_item_records = []
    order_item_number = 1

    for order_id in order_ids:
        item_count = random.randint(1, 5)

        selected_product_ids = random.sample(
            product_ids,
            k=item_count,
        )

        for product_id in selected_product_ids:
            quantity = random.randint(1, 4)
            unit_price = product_lookup[product_id]["selling_price"]

            discount_percentage = random.choice(
                [0, 0, 0, 5, 10, 15, 20]
            )

            gross_amount = round(unit_price * quantity, 2)

            discount_amount = round(
                gross_amount * discount_percentage / 100,
                2,
            )

            net_amount = round(
                gross_amount - discount_amount,
                2,
            )

            order_item_records.append(
                {
                    "order_item_id": f"OI{order_item_number:09d}",
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_percentage": discount_percentage,
                    "gross_amount": gross_amount,
                    "discount_amount": discount_amount,
                    "net_amount": net_amount,
                }
            )

            order_item_number += 1

    return pd.DataFrame(order_item_records)

def create_inventory(
    stores: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Create store-level inventory records for existing products."""

    store_ids = stores["store_id"].tolist()
    product_ids = products["product_id"].tolist()

    inventory_records = []
    inventory_record_number = 1

    for store_id in store_ids:
        stocked_product_count = random.randint(
            int(len(product_ids) * 0.60),
            int(len(product_ids) * 0.90),
        )

        stocked_product_ids = random.sample(
            product_ids,
            k=stocked_product_count,
        )

        for product_id in stocked_product_ids:
            quantity_on_hand = random.randint(0, 500)
            reorder_level = random.randint(10, 80)

            inventory_records.append(
                {
                    "inventory_id": f"INV{inventory_record_number:08d}",
                    "store_id": store_id,
                    "product_id": product_id,
                    "quantity_on_hand": quantity_on_hand,
                    "reorder_level": reorder_level,
                    "stock_status": (
                        "Out of Stock"
                        if quantity_on_hand == 0
                        else "Low Stock"
                        if quantity_on_hand <= reorder_level
                        else "In Stock"
                    ),
                    "last_updated_timestamp": (
                        fake_data_generator.date_time_between(
                            start_date="-30d",
                            end_date="now",
                        )
                    ),
                }
            )

            inventory_record_number += 1

    return pd.DataFrame(inventory_records)


def create_promotions(
    promotion_count: int,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Create product-level promotion records."""

    product_ids = products["product_id"].tolist()

    promotion_types = [
        "Percentage Discount",
        "Seasonal Campaign",
        "Clearance",
        "Loyalty Offer",
        "Festival Offer",
    ]

    promotion_records = []

    for promotion_number in range(1, promotion_count + 1):
        start_date = fake_data_generator.date_between(
            start_date="-2y",
            end_date="+30d",
        )

        end_date = start_date + timedelta(
            days=random.randint(7, 60)
        )

        promotion_records.append(
            {
                "promotion_id": f"PR{promotion_number:05d}",
                "product_id": random.choice(product_ids),
                "promotion_name": f"Promotion {promotion_number}",
                "promotion_type": random.choice(promotion_types),
                "discount_percentage": random.choice(
                    [5, 10, 15, 20, 25, 30]
                ),
                "start_date": start_date,
                "end_date": end_date,
            }
        )

    return pd.DataFrame(promotion_records)

def write_dataset(
        dataset: pd.DataFrame,
        file_name: str
) -> None: 
    """Write One generated dataset to the Output Directory"""

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_file_path = OUTPUT_DIRECTORY / file_name

    dataset.to_csv(output_file_path, index=False)

    print(f"Created {file_name}: {len(dataset)} records")

def generate_all_retail_datasets() -> None:
    """Generate and sell all OmniRetail Source datasets"""

    customers = create_customers(customer_count=CUSTOMER_COUNT)
    stores = create_stores(store_count=STORE_COUNT)
    suppliers = create_suppliers(supplier_count=SUPPLIER_COUNT)

    products = create_products(product_count=PRODUCT_COUNT,
                               suppliers=suppliers)
    
    orders = create_orders(order_count=ORDER_COUNT,
                           customers=customers,
                           stores=stores)
    
    order_items = create_order_items(orders=orders,
                                     products=products)
    
    inventory = create_inventory(stores=stores,
                                 products=products)
    
    promotions = create_promotions(promotion_count=PROMOTION_COUNT,
                                   products=products)
    
    write_dataset(customers, "customers.csv")
    write_dataset(stores, "stores.csv")
    write_dataset(suppliers, "suppliers.csv")
    write_dataset(products, "products.csv")
    write_dataset(orders, "orders.csv")
    write_dataset(order_items, "order_items.csv")
    write_dataset(inventory, "inventory.csv")
    write_dataset(promotions, "promotions.csv")

if __name__ == "__main__":
    generate_all_retail_datasets()