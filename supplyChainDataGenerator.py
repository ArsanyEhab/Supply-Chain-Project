import pandas as pd
import random
import numpy as np

# Number of rows
n_rows = 30000

# Generate synthetic dataset
product_types = ["Electronics", "Clothing", "Home", "Sports", "Toys"]
shipping_carriers = ["DHL", "FedEx", "UPS", "USPS", "Aramex"]
suppliers = ["Global Supplies Inc.", "FastTrack Ltd.", "Prime Distributors", "SupplyHub", "MegaCorp"]
locations = ["USA", "China", "Germany", "India", "Egypt"]

data = {
    "Product type": np.random.choice(product_types, n_rows),
    "SKU": [f"SKU{1000+i}" for i in range(n_rows)],
    "Price": np.random.randint(5, 500, n_rows),
    "Availability": np.random.choice(["In Stock", "Out of Stock", "Limited"], n_rows, p=[0.7, 0.2, 0.1]),
    "Number of products sold": np.random.randint(0, 1000, n_rows),
    "Revenue generated": np.random.randint(100, 50000, n_rows),
    "Customer demographics": np.random.choice(["Teen", "Adult", "Senior"], n_rows),
    "Stock levels": np.random.randint(0, 500, n_rows),
    "Lead times": np.random.randint(1, 30, n_rows),
    "Order quantities": np.random.randint(1, 100, n_rows),
    "Shipping times": np.random.randint(1, 14, n_rows),
    "Shipping carriers": np.random.choice(shipping_carriers, n_rows),
    "Shipping costs": np.round(np.random.uniform(5, 100, n_rows), 2),
    "Supplier name": np.random.choice(suppliers, n_rows),
    "Location": np.random.choice(locations, n_rows),
    "Production volumes": np.random.randint(100, 10000, n_rows),
    "Manufacturing lead time": np.random.randint(1, 60, n_rows),
    "Manufacturing costs": np.random.randint(100, 10000, n_rows),
    "Inspection results": np.random.choice(["Pass", "Fail", "Recheck"], n_rows)
}

df = pd.DataFrame(data)

# Save to CSV
file_path = "synthetic_dataset_30000.csv"  # Save in current folder
df.to_csv(file_path, index=False)

file_path
