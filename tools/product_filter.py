# tools/product_filter.py
import pandas as pd

def load_products():
    df = pd.read_csv("knowledge_base/product_info.csv")
    required = ["name", "brand", "price", "skin_type", "concern", "ingredients"]
    df = df[required].fillna("")
    return df

def simple_filter_products(condition, skin_type=None, budget=None):
    df = load_products()

    df = df[df["concern"].str.contains(condition, case=False, na=False)]

    if skin_type:
        df = df[df["skin_type"].str.contains(skin_type, case=False, na=False)]

    if budget:
        df = df[df["price"].astype(float) <= float(budget)]

    return df.head(5).to_dict(orient="records")
