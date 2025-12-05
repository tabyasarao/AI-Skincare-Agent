from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent

def rag_tool(query):
    print("[RAG TOOL] Running RAG Pipeline...")

    # 1) Retrieve chunks
    chunks = search_agent(query)

    # 2) Summarize them
    summary = summarizer_agent(chunks)

    return summary
