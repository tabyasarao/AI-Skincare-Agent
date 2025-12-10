# agents/reflective_agent.py
import re
from typing import List, Union, Dict, Any


def reflective_agent(
    summary: str,
    recommendations: List[Union[str, Dict[str, Any]]],
    query: str,
    filters: Dict[str, Any] | None = None,
    evidence: str | None = None,
) -> int:
    print("[Reflective Agent] Evaluating final answer...")

    # Start with a perfect alignment score (5 = fully aligned)
    score = 5
    reasons: list[str] = []

    # ---------- 1) Evidence Grounding Check ----------
    # Check if summary is missing or empty
    if summary is None or summary.strip() == "":
        score = min(score, 3)
        reasons.append("Summary is empty or missing.")

    # (Assumption) The summarizer may use this phrase when no evidence is found
    if "No related evidence found" in summary:
        score = min(score, 2)
        reasons.append("Summary indicates that no related evidence was found.")

    # If RAG evidence is not provided, penalize slightly
    if evidence is None or (isinstance(evidence, str) and evidence.strip() == ""):
        score = min(score, 4)
        reasons.append("No RAG evidence text was provided to the reflective agent.")

    # ---------- 2) Recommendation Availability Check ----------
    if not recommendations:
        score = min(score, 3)
        reasons.append("No recommendations were generated.")
    else:
        rec_text_all = " ".join(str(r) for r in recommendations)

        if "No skincare products matched your filters." in rec_text_all:
            score = min(score, 3)
            reasons.append("Recommender reports that no products matched the filters.")

        if "No products fully matched your filters" in rec_text_all:
            score = min(score, 3)
            reasons.append("Recommender reports that no products fully matched the filters.")

    # ---------- 3) Consistency With User Filters ----------
    if filters and isinstance(filters, dict) and recommendations:

        # Filter structure based on app.py
        skin_type = (filters.get("skin_type") or "").lower().strip()

        main_concerns = filters.get("main_concerns") or []
        if isinstance(main_concerns, str):
            main_concerns = [main_concerns]
        main_concerns = [c.lower() for c in main_concerns if c]

        min_price = float(filters.get("min_price") or 0)
        max_price = float(filters.get("max_price") or 0)

        age_range = (filters.get("age_range") or "").lower().strip()
        needs_sensitive = bool(filters.get("needs_sensitive") or False)

        text_all = " ".join(str(r).lower() for r in recommendations)

        # 3-1) Check if skin type is reflected in the recommendation text
        if skin_type and skin_type not in text_all:
            score = min(score, 4)
            reasons.append("User's skin type is not clearly reflected in the recommendations.")

        # 3-2) Each main concern should appear at least once
        for c in main_concerns:
            if c not in text_all:
                score = min(score, 4)
                reasons.append(f"Main concern '{c}' is not reflected in the recommendations.")
                break

        # 3-3) Sensitive-skin priority but no mention of “sensitive”
        if needs_sensitive and "sensitive" not in text_all:
            score = min(score, 3)
            reasons.append(
                "User requested sensitive-skin-safe products but 'sensitive' "
                "is not mentioned in the recommendation output."
            )

        # 3-4) Price range check (extract $xx.xx numbers from text)
        if max_price > 0:
            prices_found = [
                float(m.group(1))
                for m in re.finditer(r"\$(\d+(\.\d+)?)", text_all)
            ]
            over_budget = [p for p in prices_found if p > max_price]

            if over_budget:
                score = min(score, 3)
                reasons.append("Some recommended products appear to exceed the user's budget.")

    # ---------- 4) Safety & Scope Review ----------
    unsafe_phrases = [
        "diagnose",
        "diagnosis",
        "prescribe",
        "prescription",
        "cure",
        "guaranteed cure",
        "permanent cure",
        "replace your doctor",
    ]

    out_of_scope_terms = [
        "skin cancer",
        "melanoma",
        "psoriasis",
        "eczema",
    ]

    combined_text = (summary or "") + " " + " ".join(str(r) for r in recommendations)

    # Detect overconfident or medical-language risks
    if any(phrase in combined_text.lower() for phrase in unsafe_phrases):
        score = min(score, 2)
        reasons.append("Detected potentially diagnostic or unsafe medical language.")

    # Detect out-of-scope dermatological conditions
    if any(term in combined_text.lower() for term in out_of_scope_terms):
        score = min(score, 3)
        reasons.append("Detected references to skin conditions outside the project scope.")

    # ---------- 5) Final Score Normalization (1–5) ----------
    score = max(1, min(score, 5))

    print("\n--- Reflective Evaluation ---")
    print(f"Reflective Alignment Score: {score}/5")
    if reasons:
        print("Reasons:")
        for r in reasons:
            print(" -", r)

    return score
