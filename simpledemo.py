# Planner Agent
def planner_agent(query): #plan the steps based on user input
    print("[Planner Agent] Understanding the user input...")
    return "Retrieve dermatology evidence → Summarize → Recommend → Reflect"

# Search Agent - Rag Retrieval (from dermatology PDF) - not using for this example
def search_agent(condition): #retrieve evidence from dermatology PDF
    print("[Search Agent] Searching dermatology PDF...")
    if condition == "acne":
        return "Topical retinoids (tretinoin, adapalene) and benzoyl peroxide are first-line acne treatments."
    elif condition == "hyperpigmentation":
        return "Azelaic acid and retinoids help reduce hyperpigmentation."
    elif condition == "blackheads":
        return "Salicylic acid helps unclog pores and reduce comedonal acne."
    else:
        return "No related evidence found."

# Summarizer Agent
def summarizer_agent(evidence): #summarize the PDF evidence
    print("[Summarizer Agent] Summarizing retrieved evidence...")
    return f"Summary: {evidence} (from dermatology research PDF)" #based on PDF

# Recommendation Agent
def recommender_agent(condition): #get data from summarize and beauty product database 
    print("[Recommender Agent] Suggesting suitable skincare products...")
    if condition == "acne":
        return ["La Roche-Posay Effaclar Duo", "CeraVe Foaming Cleanser", "The Ordinary Niacinamide Serum"]
    elif condition == "hyperpigmentation":
        return ["The Ordinary Azelaic Acid 10%", "Paula’s Choice BHA Exfoliant", "Eucerin Even Pigment Perfector"]
    elif condition == "blackheads":
        return ["Neutrogena Oil-Free Wash", "CeraVe Renewing Cleanser", "COSRX BHA Blackhead Power Liquid"]
    else:
        return ["No recommendations found"]

# Reflective Agent
def reflective_agent(summary, recommendations, query):
    print("[Reflective Agent] Evaluating final answer...")

    # Default Reflective Alignment Score
    score = 5

    # If no relevant evidence was found, lower the score
    if "No related evidence found" in summary:
        score = 2

    # If recommendations are missing or empty, lower the score
    if not recommendations or "No recommendations" in recommendations[0]:
        score = min(score, 3)

    print("\n--- Reflective Evaluation ---")
    print(f"Reflective Alignment Score: {score}/5")

    return score

#output
def main(): 
    print("=== Beauty product Recommendations ===")
    query = "Recommend acne-safe products for oily skin"
    planner_agent(query)
    
    evidence = search_agent("acne")
    summary = summarizer_agent(evidence)
    products = recommender_agent("acne")
    score = reflective_agent(summary, products, query)
    
    print("\n--- Final Output ---")
    print(summary)
    print("\nTop Recommendations:")
    for p in products:
        print("-", p)
    print(f"\nOverall Reflective Score: {avg_score}/5 ✅")

main()