# summarizer_agent_groq.py (FREE VERSION)
from groq import Groq

client = Groq(api_key="GROQ_API_KEY") 
import os
from dotenv import load_dotenv
load_dotenv()


def summarizer_agent(evidence_list):
    print("[Summarizer Agent] Summarizing dermatology evidence (FREE using Groq)...")

    if isinstance(evidence_list, list):
        evidence_text = "\n".join(evidence_list)
    else:
        evidence_text = str(evidence_list)

    prompt = f"""
You are a dermatology assistant.

Summarize the medical evidence below in 3–5 natural, readable sentences.
Rules:
- No bullet points.
- No “Summary:” phrases.
- No list format.
- Use natural academic English.
- Focus on causes, symptoms, treatments.

Evidence:
{evidence_text}
"""

    # ⬇️ AQUÍ SOLO ENVOLVEMOS TU LLAMADA ORIGINAL EN try/except
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        # Si Groq falla (403 u otro error), NO rompemos la app
        print("[Summarizer Agent] Groq error, usando fallback local.")
        print(f"Detalle del error: {e}")

        if not evidence_text:
            return (
                "Summary (fallback): Groq API is not available right now "
                "and no evidence text was provided."
            )

        short_preview = evidence_text[:800]

        return (
            "Summary (fallback): Groq API is not available right now. "
            "Here is a basic preview of the retrieved medical evidence:\n\n"
            f"{short_preview}"
        )
