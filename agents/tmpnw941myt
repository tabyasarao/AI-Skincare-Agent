# Reflective Agent
def reflective_agent(summary, recommendations, query, filters=None):
    print("[Reflective Agent] Evaluating final answer...")

    # Default score (start from fully aligned)
    score = 5

    # 1) Evidence grounding check
    if "No related evidence found" in summary:
        score = 2  # weak alignment if we have no evidence at all

    # 2) Recommendation availability check
    if (not recommendations) or ("No recommendations" in str(recommendations[0])):
        score = min(score, 3)

    # 3) Very simple constraint check (budget)
    if filters and isinstance(filters, dict):
        budget = filters.get("budget", 0)
        if budget and isinstance(recommendations, list):
            over_budget_found = False
            for item in recommendations:

                if isinstance(item, dict) and "price" in item:
                    if item["price"] > budget:
                        over_budget_found = True
                        break
            if over_budget_found:
                # some products do not respect the budget constraint
                score = min(score, 3)

    print("\n--- Reflective Evaluation ---")
    print(f"Reflective Alignment Score: {score}/5")

    return score