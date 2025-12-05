import re

def planner_agent(user_query):
    print("[Planner] Understanding the user query...")

    # condition
    skin_conditions = ["acne", "dryness", "redness", "dark spots", "hyperpigmentation", "wrinkles", "sensitive skin"]
    found_condition = None
    for cond in skin_conditions:
        if cond in user_query.lower():
            found_condition = cond
            break

    # budget
    budget_match = re.search(r"\$?(\d+)", user_query)
    budget = int(budget_match.group(1)) if budget_match else None

    # recommendation filters
    filters = []
    keywords = ["vegan", "fragrance free", "paraben free", "oil free", "hydrating"]
    for word in keywords:
        if word in user_query.lower():
            filters.append(word)

    # plan
    plan = {
        "steps": [
            "Retrieve evidence from dermatology PDF",
            "Summarize findings (key ingredients)",
            "Match products in CSV based on ingredients",
            "Generate recommendation list",
            "Reflect on product–evidence alignment"
        ],
        "condition": found_condition or "general",
        "budget": budget,
        "filters": filters
    }

    print(f"[Planner Output] Condition: {plan['condition']}, Budget: {plan['budget']}, Filters: {plan['filters']}")
    return plan