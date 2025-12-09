# agents/planner_agent.py
import re

def planner_agent(user_query):
    print("[Planner] Understanding the user query...")

    query = user_query.lower()

    # 1) Skin condition detection
    conditions = ["acne", "blackheads", "hyperpigmentation"]
    found_condition = None
    for c in conditions:
        if c in query:
            found_condition = c
            break

    # 2) Skin type detection
    skin_types = ["dry", "oily", "combination", "sensitive", "normal"]
    found_skin_type = None
    for st in skin_types:
        if st in query:
            found_skin_type = st
            break

    # 3) Product type detection
    product_types = ["cleanser", "serum", "moisturizer", "sunscreen", "toner"]
    found_product_type = None
    for pt in product_types:
        if pt in query:
            found_product_type = pt
            break

    # 4) Additional filters (allergies, preferences)
    filters = []
    keywords = ["fragrance-free", "vegan", "non-comedogenic", 
                "oil-free", "paraben-free", "alcohol-free"]
    for word in keywords:
        if word in query:
            filters.append(word)

    # 5) Budget extraction
    budget_match = re.search(r"\$?(\d+)", query)
    budget = int(budget_match.group(1)) if budget_match else None

    # === Build the plan ===
    plan = {
        "steps": [
            "Step 1: Retrieve dermatology evidence using RAG Search Agent.",
            "Step 2: Summarize retrieved information using Summarizer Agent.",
            "Step 3: Generate ingredient-based skincare recommendations using Recommender Agent.",
            "Step 4: Perform safety and consistency review using Reflective Agent."
        ],
        "parsed_info": {
            "condition": found_condition or "general",
            "skin_type": found_skin_type,
            "product_type": found_product_type,
            "filters": filters,
            "budget": budget
        },
        "raw_query": user_query
        
    }

    print(f"\n[Planner Output]")
    print(f" Condition: {plan['parsed_info']['condition']}")
    print(f" Skin Type: {plan['parsed_info']['skin_type']}")
    print(f" Product Type: {plan['parsed_info']['product_type']}")
    print(f" Filters: {plan['parsed_info']['filters']}")
    print(f" Budget: {plan['parsed_info']['budget']}\n")
    

    return plan

if __name__ == "__main__":
    query = "Recommend a fragrance-free moisturizer for acne and oily skin under $30"
    plan = planner_agent(query)
    print("\nFINAL PLAN OUTPUT:")
    print(plan)