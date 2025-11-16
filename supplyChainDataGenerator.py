import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta, date

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of rows
n_rows = 30000

# Define categories with realistic characteristics
product_types = ["Electronics", "Clothing", "Home", "Sports", "Toys"]
shipping_carriers = ["DHL", "FedEx", "UPS", "USPS", "Aramex"]
suppliers = ["Global Supplies Inc.", "FastTrack Ltd.", "Prime Distributors", "SupplyHub", "MegaCorp"]
locations = ["USA", "China", "Germany", "India", "Egypt"]

# Product type characteristics (base price ranges and complexity)
product_characteristics = {
    "Electronics": {"price_range": (50, 800), "complexity": 1.5, "demand": 1.2},
    "Clothing": {"price_range": (10, 150), "complexity": 0.6, "demand": 1.5},
    "Home": {"price_range": (20, 400), "complexity": 1.0, "demand": 1.0},
    "Sports": {"price_range": (15, 300), "complexity": 0.8, "demand": 0.9},
    "Toys": {"price_range": (5, 100), "complexity": 0.7, "demand": 1.3}
}

# Location characteristics (shipping cost multiplier, lead time days)
location_characteristics = {
    "USA": {"ship_mult": 1.0, "lead_days": 5},
    "China": {"ship_mult": 1.8, "lead_days": 15},
    "Germany": {"ship_mult": 1.4, "lead_days": 10},
    "India": {"ship_mult": 1.6, "lead_days": 12},
    "Egypt": {"ship_mult": 1.5, "lead_days": 14}
}

# Carrier characteristics (base cost and reliability)
carrier_characteristics = {
    "DHL": {"base_cost": 25, "reliability": 0.95},
    "FedEx": {"base_cost": 30, "reliability": 0.93},
    "UPS": {"base_cost": 22, "reliability": 0.92},
    "USPS": {"base_cost": 15, "reliability": 0.85},
    "Aramex": {"base_cost": 20, "reliability": 0.88}
}

# Surrogate key seeds and helper mappings
supplier_id_map = {name: f"SUP{1000 + idx:04d}" for idx, name in enumerate(suppliers, start=1)}

# Build a realistic customer pool by demographics and location buckets
customer_pool_size = 5000
demographics_categories = ["Teen", "Adult", "Senior"]
demographics_weights = [0.25, 0.6, 0.15]
location_weights = {
    "USA": 0.25,
    "China": 0.2,
    "Germany": 0.2,
    "India": 0.2,
    "Egypt": 0.15
}

# Create buckets mapping (demographics, location) -> list of customer IDs
bucket_to_customers = {(d, l): [] for d in demographics_categories for l in locations}
for i in range(customer_pool_size):
    d = random.choices(demographics_categories, weights=demographics_weights, k=1)[0]
    l = random.choices(locations, weights=[location_weights[x] for x in locations], k=1)[0]
    bucket_to_customers[(d, l)].append(f"CUST{100000 + i:06d}")

# Shipping and manufacturing ID counters
shipping_seq = 1
manufacturing_seq = 1

# Order date generator with seasonal patterns by product type
today = date.today()
start_date = today - timedelta(days=730)

def generate_order_date(selected_product_type: str) -> date:
    # Month seasonality: Clothing/Toys/Electronics peak in Q4, Sports peak in Q2-Q3
    month_weights = [1]*12
    if selected_product_type in ("Clothing", "Toys", "Electronics"):
        # Heavier weights for Oct-Dec
        month_weights = [1,1,1,1,1,1,1,1,2,3,3,2]
    elif selected_product_type == "Sports":
        # Peak in spring/summer
        month_weights = [1,1,2,2,3,3,3,2,1,1,1,1]
    else:
        # Home balanced with slight Q2 bump
        month_weights = [1,1,2,2,2,2,2,1,1,1,1,1]

    # Choose a random month in the last 24 months with weights applied by month number
    # Sample a random day count offset, but bias by target month
    target_month = random.choices(range(1,13), weights=month_weights, k=1)[0]

    # Pick a random date within last 24 months, then adjust towards target month by resampling
    for _ in range(5):
        rand_days = random.randint(0, 730)
        candidate = start_date + timedelta(days=rand_days)
        if candidate.month == target_month:
            return candidate
    # Fallback: return candidate even if month mismatch
    return start_date + timedelta(days=random.randint(0, 730))

# Initialize lists to store data
product_type_list = []
sku_list = []
order_date_list = []
customer_id_list = []
supplier_id_list = []
shipping_id_list = []
manufacturing_id_list = []
price_list = []
availability_list = []
num_sold_list = []
revenue_list = []
demographics_list = []
stock_levels_list = []
lead_times_list = []
order_quantities_list = []
shipping_times_list = []
shipping_carriers_list = []
shipping_costs_list = []
supplier_list = []
location_list = []
production_volumes_list = []
manufacturing_lead_time_list = []
manufacturing_costs_list = []
inspection_results_list = []

# Generate correlated data row by row
for i in range(n_rows):
    # Select product type and location
    product_type = np.random.choice(product_types)
    location = np.random.choice(locations)
    order_date = generate_order_date(product_type)
    
    # Generate price based on product type with variety
    price_min, price_max = product_characteristics[product_type]["price_range"]
    price = np.round(np.random.uniform(price_min, price_max), 2)
    
    # Generate sales with inverse relationship to price (higher price = generally lower sales)
    # But also influenced by product type demand
    demand_factor = product_characteristics[product_type]["demand"]
    base_sales = max(0, 500 - (price / 2) + np.random.normal(0, 100))
    num_sold = int(max(0, base_sales * demand_factor))
    
    # Revenue = Price × Number Sold (with small random variance)
    revenue = np.round(price * num_sold * np.random.uniform(0.95, 1.05), 2)
    
    # Stock levels influenced by sales patterns (higher sales = need more stock)
    stock_levels = int(max(0, num_sold * 0.5 + np.random.normal(100, 50)))
    
    # Availability based on stock levels
    if stock_levels > 200:
        availability = "In Stock"
    elif stock_levels > 50:
        availability = np.random.choice(["In Stock", "Limited"], p=[0.7, 0.3])
    else:
        availability = np.random.choice(["Limited", "Out of Stock"], p=[0.5, 0.5])
    
    # Order quantities related to sales volume
    order_quantities = int(max(1, num_sold * 0.15 + np.random.normal(20, 10)))
    
    # Lead times influenced by location
    base_lead = location_characteristics[location]["lead_days"]
    lead_times = int(max(1, base_lead + np.random.normal(0, 3)))
    
    # Manufacturing lead time related to product complexity and order quantity
    complexity = product_characteristics[product_type]["complexity"]
    manufacturing_lead_time = int(max(1, 15 * complexity + order_quantities * 0.1 + np.random.normal(0, 5)))
    
    # Production volumes inversely related to complexity (simpler products = higher volumes)
    production_volumes = int(max(100, 5000 / complexity + np.random.normal(0, 500)))
    
    # Manufacturing costs related to product complexity, production volume (economies of scale)
    unit_complexity_cost = complexity * 100
    volume_discount = max(0.5, 1 - (production_volumes / 20000))  # Higher volume = lower per-unit cost
    manufacturing_costs = int(max(50, unit_complexity_cost * order_quantities * volume_discount + np.random.normal(0, 200)))
    
    # Select carrier
    carrier = np.random.choice(shipping_carriers)
    
    # Shipping costs based on location, carrier, and order weight (approximated by quantity)
    base_cost = carrier_characteristics[carrier]["base_cost"]
    location_mult = location_characteristics[location]["ship_mult"]
    weight_factor = 1 + (order_quantities / 100)  # More items = higher shipping cost
    shipping_costs = np.round(base_cost * location_mult * weight_factor * np.random.uniform(0.9, 1.1), 2)
    
    # Shipping times related to location and carrier reliability
    base_ship_time = location_characteristics[location]["lead_days"] * 0.4
    reliability = carrier_characteristics[carrier]["reliability"]
    shipping_times = int(max(1, base_ship_time / reliability + np.random.normal(0, 2)))
    
    # Customer demographics influenced by product type
    if product_type == "Electronics":
        demographics = np.random.choice(["Teen", "Adult", "Senior"], p=[0.3, 0.6, 0.1])
    elif product_type == "Toys":
        demographics = np.random.choice(["Teen", "Adult", "Senior"], p=[0.5, 0.45, 0.05])
    elif product_type == "Clothing":
        demographics = np.random.choice(["Teen", "Adult", "Senior"], p=[0.35, 0.5, 0.15])
    else:
        demographics = np.random.choice(["Teen", "Adult", "Senior"], p=[0.2, 0.6, 0.2])
    
    # Inspection results based on supplier and complexity
    supplier = np.random.choice(suppliers)
    sup_id = supplier_id_map[supplier]
    if supplier == "Prime Distributors":
        inspection = np.random.choice(["Pass", "Fail", "Recheck"], p=[0.9, 0.05, 0.05])
    elif supplier == "MegaCorp":
        inspection = np.random.choice(["Pass", "Fail", "Recheck"], p=[0.85, 0.1, 0.05])
    else:
        inspection = np.random.choice(["Pass", "Fail", "Recheck"], p=[0.8, 0.12, 0.08])

    # Choose a customer ID from the (demographics, location) bucket; if empty, backoff to any location
    bucket = (demographics, location)
    ids = bucket_to_customers.get(bucket, [])
    if ids:
        cust_id = random.choice(ids)
    else:
        # Rare fallback if a bucket ended up empty
        all_ids = [cid for sub in bucket_to_customers.values() for cid in sub]
        cust_id = random.choice(all_ids)

    # Generate shipping and manufacturing surrogate IDs
    ship_id = f"SHIP{shipping_seq:07d}"
    manufacturing_id = f"MFG{manufacturing_seq:07d}"
    shipping_seq += 1
    manufacturing_seq += 1
    
    # Append to lists
    product_type_list.append(product_type)
    sku_list.append(f"SKU{1000+i}")
    order_date_list.append(order_date)
    customer_id_list.append(cust_id)
    supplier_id_list.append(sup_id)
    shipping_id_list.append(ship_id)
    manufacturing_id_list.append(manufacturing_id)
    price_list.append(price)
    availability_list.append(availability)
    num_sold_list.append(num_sold)
    revenue_list.append(revenue)
    demographics_list.append(demographics)
    stock_levels_list.append(stock_levels)
    lead_times_list.append(lead_times)
    order_quantities_list.append(order_quantities)
    shipping_times_list.append(shipping_times)
    shipping_carriers_list.append(carrier)
    shipping_costs_list.append(shipping_costs)
    supplier_list.append(supplier)
    location_list.append(location)
    production_volumes_list.append(production_volumes)
    manufacturing_lead_time_list.append(manufacturing_lead_time)
    manufacturing_costs_list.append(manufacturing_costs)
    inspection_results_list.append(inspection)

# Create DataFrame
data = {
    "Order date": order_date_list,
    "Product type": product_type_list,
    "SKU": sku_list,
    "Customer ID": customer_id_list,
    "Supplier ID": supplier_id_list,
    "Shipping ID": shipping_id_list,
    "Manufacturing ID": manufacturing_id_list,
    "Price": price_list,
    "Availability": availability_list,
    "Number of products sold": num_sold_list,
    "Revenue generated": revenue_list,
    "Customer demographics": demographics_list,
    "Stock levels": stock_levels_list,
    "Lead times": lead_times_list,
    "Order quantities": order_quantities_list,
    "Shipping times": shipping_times_list,
    "Shipping carriers": shipping_carriers_list,
    "Shipping costs": shipping_costs_list,
    "Supplier name": supplier_list,
    "Location": location_list,
    "Production volumes": production_volumes_list,
    "Manufacturing lead time": manufacturing_lead_time_list,
    "Manufacturing costs": manufacturing_costs_list,
    "Inspection results": inspection_results_list
}

df = pd.DataFrame(data)

# Save to CSV and Excel
csv_path = "synthetic_dataset_30000.csv"
xlsx_path = "synthetic_dataset_30000.xlsx"

df.to_csv(csv_path, index=False)
df.to_excel(xlsx_path, index=False)

print(f"Dataset generated successfully with {n_rows} rows!")
print(f"Saved to: {csv_path} and {xlsx_path}")
print("\nKey Correlations Implemented:")
print("- Revenue = Price x Number of products sold")
print("- Higher prices -> Lower sales (demand curve)")
print("- Product type affects price range, complexity, and demand")
print("- Location affects shipping costs, lead times, and shipping times")
print("- Carriers have different costs and reliability")
print("- Manufacturing costs relate to complexity and volume")
print("- Stock levels correlate with sales patterns")
print("- Demographics vary by product type")
