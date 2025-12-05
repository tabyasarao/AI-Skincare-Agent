import pandas as pd

INPUT_PATH = "product_info.csv"

OUTPUT_PATH = "product_info_slim.csv"

COLUMNS_NEEDED = [
    "brand_name",
    "product_name",
    "ingredients",
    "price_usd",
    "highlights",
    "primary_category",
    "secondary_category",
    "tertiary_category"
]

def make_slim_csv():
    print("📌 Loading original CSV...")
    df = pd.read_csv(INPUT_PATH)

    print("📌 Original columns:", list(df.columns))

    print("📌 Extracting required columns...")
    df_slim = df[COLUMNS_NEEDED]

    print("📌 Saving slim CSV...")
    df_slim.to_csv(OUTPUT_PATH, index=False)

    print(f"🎉 Done! Saved slim file at: {OUTPUT_PATH}")

if __name__ == "__main__":
    make_slim_csv()
