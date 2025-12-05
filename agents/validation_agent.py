# agents/validation_agent.py

def is_valid_skincare_question(question: str) -> bool:
    """
    Return True if the question seems related to skincare,
    otherwise False.
    """
    if not question:
        return False

    q = question.lower().strip()

    # Palabras típicas de skincare
    skincare_keywords = [
        "skin", "skincare", "acne", "pimple", "pimples", "blackhead", "blackheads",
        "pores", "oil", "oily", "dry skin", "dryness", "sensitive skin",
        "redness", "rosacea", "eczema", "dark spots", "hyperpigmentation",
        "wrinkles", "fine lines", "blemish", "blemishes",
        "moisturizer", "moisturiser", "cream", "serum", "cleanser", "toner",
        "sunscreen", "spf", "mask", "spot treatment", "lotion", "exfoliant",
        "retinol", "vitamin c", "niacinamide"
    ]

    # Palabras que claramente NO son de skincare (opcional)
    non_skincare_keywords = [
        "weather", "temperature", "rain", "sunny", "cloudy", "storm",
        "football", "soccer", "basketball",
        "movie", "music", "song",
        "exam", "homework", "math", "algebra",
        "stock", "bitcoin", "crypto",
        "flight", "travel", "hotel"
    ]

    # Si contiene algo muy “no skincare”, rechazamos directo
    if any(word in q for word in non_skincare_keywords):
        return False

    # Si contiene palabras de skincare → aceptamos
    if any(word in q for word in skincare_keywords):
        return True

    # Si no encontramos nada, lo tratamos como pregunta no válida
    return False


def validation_agent(user_question: str) -> dict:
    """
    Agente de validación. Devuelve un dict con:
    - is_valid: bool
    - message: str
    """
    print("[Validation Agent] Checking if question is about skincare...")

    if is_valid_skincare_question(user_question):
        return {
            "is_valid": True,
            "message": "Question accepted as skincare-related."
        }

    # Mensaje que verás en el frontend
    return {
        "is_valid": False,
        "message": (
            "Error: Your question does not seem to be about skincare. "
            "Please ask about skin concerns, skincare products, routines, "
            "or ingredients (e.g., acne, dryness, sunscreen, serums, etc.)."
        )
    }
