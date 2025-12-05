import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "knowledge_base", "product_info_slim.csv")

print(f"[Recommender] Loading product CSV from: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

df = df[[
    "brand_name",
    "product_name",
    "ingredients",
    "price_usd",
    "highlights",
    "primary_category",
    "secondary_category",
    "tertiary_category"
]]

df["highlights_lower"] = df["highlights"].fillna("").str.lower()
df["ingredients_lower"] = df["ingredients"].fillna("").str.lower()


def recommender_agent(filters):
    print("[Recommender Agent] Selecting products with scoring...")

    skin_type       = (filters.get("skin_type") or "").lower()
    product_type    = (filters.get("product_type") or "").lower()

    min_price       = float(filters.get("min_price") or 0)
    max_price       = float(filters.get("max_price") or 0)

    main_concerns = filters.get("main_concerns") or []
    if isinstance(main_concerns, str):
        main_concerns = [main_concerns]
    main_concerns = [c.lower() for c in main_concerns if c]

    age_range       = (filters.get("age_range") or "").lower()
    needs_sensitive = bool(filters.get("needs_sensitive") or False)

    filtered_df = df.copy()

    # ---------- PRODUCT TYPE  ----------
    if product_type and product_type.lower() != "other":
        pt = product_type.lower()

        name_lower = filtered_df["product_name"].fillna("").str.lower()
        prim_lower = filtered_df["primary_category"].fillna("").str.lower()
        sec_lower  = filtered_df["secondary_category"].fillna("").str.lower()
        ter_lower  = filtered_df["tertiary_category"].fillna("").str.lower()

        if pt == "serum":
            include = (
                name_lower.str.contains("serum")
                | prim_lower.str.contains("serum")
                | sec_lower.str.contains("serum")
                | ter_lower.str.contains("serum")
            )
            exclude = (
                name_lower.str.contains("primer")
                | name_lower.str.contains("spot")
                | name_lower.str.contains("patch")
                | name_lower.str.contains("dots")
                | name_lower.str.contains("cleanser")
                | name_lower.str.contains("wash")
                | name_lower.str.contains("toner")
                | name_lower.str.contains("mask")
                | name_lower.str.contains("spot treatment")
                | name_lower.str.contains("acne spot")
                | name_lower.str.contains("treatment gel")
                | name_lower.str.contains("scar gel")
                | name_lower.str.contains("concealer")
                | name_lower.str.contains("foundation")
            )
            mask_type = include & (~exclude)

        elif pt == "cleanser":
            include = (
                name_lower.str.contains("cleanser")
                | name_lower.str.contains("cleansing")
                | name_lower.str.contains("face wash")
                | name_lower.str.contains("washing foam")
                | prim_lower.str.contains("cleanser")
                | sec_lower.str.contains("cleanser")
                | ter_lower.str.contains("cleanser")
            )
            exclude = (
                name_lower.str.contains("toner")
                | name_lower.str.contains("moisturizer")
                | name_lower.str.contains("moisturiser")
                | name_lower.str.contains("serum")
                | name_lower.str.contains("mask")
                | name_lower.str.contains("spot treatment")
                | name_lower.str.contains("concealer")
                | name_lower.str.contains("foundation")
            )
            mask_type = include & (~exclude)

        elif pt == "moisturizer":
            include = (
                name_lower.str.contains("moisturizer")
                | name_lower.str.contains("moisturiser")
                | name_lower.str.contains("moisturizing")
                | name_lower.str.contains("moisturising")
                | name_lower.str.contains("hydrating cream")
                | name_lower.str.contains("face cream")
                | prim_lower.str.contains("moisturizer")
                | sec_lower.str.contains("moisturizer")
                | ter_lower.str.contains("moisturizer")
            )
            exclude = (
                name_lower.str.contains("concealer")
                | name_lower.str.contains("foundation")
                | name_lower.str.contains("tinted moisturizer")
                | name_lower.str.contains("tinted")
                | name_lower.str.contains("bb cream")
                | name_lower.str.contains("cc cream")
                | name_lower.str.contains("cleanser")
                | name_lower.str.contains("wash")
                | name_lower.str.contains("toner")
                | name_lower.str.contains("spot treatment")
                | name_lower.str.contains("mask")
            )
            mask_type = include & (~exclude)

        else:
            mask_type = (
                prim_lower.str.contains(pt)
                | sec_lower.str.contains(pt)
                | ter_lower.str.contains(pt)
            )

        filtered_df = filtered_df[mask_type]


    # ---------- PRICE RANGE ----------
    if min_price > 0:
        filtered_df = filtered_df[filtered_df["price_usd"] >= min_price]
    if max_price > 0:
        filtered_df = filtered_df[filtered_df["price_usd"] <= max_price]

    if filtered_df.empty:
        return [
            "No skincare products matched your filters.",
            "Tip: Try widening your price range or changing the product type."
        ]

    # ---------- SCORING ----------
    filtered_df["score"] = 0

    # +2 → Skin type match
    if skin_type:
        mask_skin = filtered_df["highlights_lower"].str.contains(skin_type)
        filtered_df.loc[mask_skin, "score"] += 2

    # +2 → Main concerns
    if main_concerns:
        for concern in main_concerns:
            mask_c = (
                filtered_df["highlights_lower"].str.contains(concern)
                | filtered_df["ingredients_lower"].str.contains(concern)
            )
            filtered_df.loc[mask_c, "score"] += 2

    # +1 → Price 
    if max_price > 0:
        mask_cheap = filtered_df["price_usd"] <= max_price * 0.8
        filtered_df.loc[mask_cheap, "score"] += 1

    # +1 → Age range o “all ages”
    if age_range:
        mask_age = (
            filtered_df["highlights_lower"].str.contains(age_range)
            | filtered_df["highlights_lower"].str.contains("all ages")
        )
        filtered_df.loc[mask_age, "score"] += 1

    # +1 → Suitable for sensitive skin
    if needs_sensitive:
        mask_sens = filtered_df["highlights_lower"].str.contains("sensitive")
        filtered_df.loc[mask_sens, "score"] += 1

    # 
    filtered_df = filtered_df[filtered_df["score"] > 0]

    if filtered_df.empty:
        return [
            "No products fully matched your filters (skin type + concerns + price).",
            "Tip: Try quitar una concern o ampliar el rango de precio."
        ]

    # ---------- RANKING ----------
    filtered_df = filtered_df.sort_values(
        by=["score", "price_usd"],
        ascending=[False, True]
    )

    total_matches = len(filtered_df)

    # ---------- OUTPUT MESSAGES ----------
    pretty_skin = skin_type or "your"
    pretty_concerns = ", ".join(main_concerns) if main_concerns else "your main concern(s)"

    header = (
        f"**Top skincare recommendations for you**  \n"
        f"(Skin type: {pretty_skin}, "
        f"Main concern(s): {pretty_concerns}, "
        f"Budget: {min_price if min_price > 0 else 0}–{max_price if max_price > 0 else 'N/A'})"
    )

    results = [header]

    if 0 < total_matches < 5:
        results.append(
            f"Only **{total_matches}** products matched your filters. Showing all available matches."
        )

    for rank, (_, row) in enumerate(filtered_df.head(5).iterrows(), start=1):
        ing_list = [x.strip() for x in str(row["ingredients"]).split(",") if x.strip()]
        key_ings = ", ".join(ing_list[:3]) if ing_list else "key skincare ingredients"

        item = (
            f"{rank}) **{row['product_name']}** by *{row['brand_name']}* – ${row['price_usd']}\n"
            f"Reason: Recommended for {pretty_skin} skin and {pretty_concerns}.\n"
            f"Contains key ingredients such as {key_ings}.\n"
            f"(Score: {row['score']})"
        )
        results.append(item)

    results.append(
        "_These recommendations are based on product data and tags and are not medical advice._"
    )

    return results
