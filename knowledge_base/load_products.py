import pandas as pd

def load_products(csv_path="product_info.csv"):
    needed_cols = [
        "brandName",
        "productName",
        "primaryIngredient",
        "skinType",
        "productType",
        "price"
    ]

    df = pd.read_csv(csv_path)
    
    available = [c for c in needed_cols if c in df.columns]
    df = df[available]
    df = df.fillna("")

    return df
