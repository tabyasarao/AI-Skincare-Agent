from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarizer_agent(evidence_list):
    print("[Summarizer Agent] Summarizing dermatology evidence...")

    if isinstance(evidence_list, list):
        evidence_text = "\n".join(evidence_list)
    else:
        evidence_text = str(evidence_list)

    prompt = f"""
You are a dermatology assistant.

Summarize the medical evidence below in 3–5 natural, readable sentences.
Rules:
- No bullet points.
- No “Summary:” label.
- No list format.
- Use natural academic English.
- Focus on causes, symptoms, treatments.

Evidence:
{evidence_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )        
        return response.choices[0].message.content

    except Exception as e:
        print("[Summarizer Agent] Groq error, using fallback local.")
        print(f"Error detail: {e}")

        if not evidence_text:
            return (
                "Summary (fallback): LLM unavailable and no evidence provided."
            )

        short_preview = evidence_text[:800]

        return (
            "Summary (fallback): LLM unavailable. "
            "Here is a preview of the retrieved medical evidence:\n\n"
            f"{short_preview}"
        )
