# crew_main.py
from crewai import Crew, Process
from agents.planner_agent import planner_agent
from agents.search_agent import rag_agent
from agents.summarizer_agent import summarizer_agent, summarize_text
from agents.recommender_agent import recommender_agent, recommend_products
from agents.reflective_agent import reflective_agent, evaluate_output

def run_pipeline(query, condition, skin_type):
    print("🚀 Running CrewAI Multi-Agent Pipeline...\n")

    # Step 1: Planner
    print("[Planner] Planning workflow: RAG → Summarize → Recommend → Reflect")

    # Step 2: RAG Search
    evidence = rag_search(query)
    print(f"\n[RAG Agent] Retrieved Evidence:\n{evidence[:300]}...\n")

    # Step 3: Summarize
    summary = summarize_text(evidence)
    print(f"[Summarizer] {summary}\n")

    # Step 4: Recommend
    products = recommend_products(condition, skin_type)
    print(f"[Recommender] Top Products: {products}\n")

    # Step 5: Reflective
    score = evaluate_output(summary, products)
    print(f"[Reflective] Overall Quality Score: {score}/5 ✅\n")

    return summary, products, score

crew = Crew(
    agents=[planner_agent, rag_agent, summarizer_agent, recommender_agent, reflective_agent],
    process=Process.sequential,
    verbose=True
)
