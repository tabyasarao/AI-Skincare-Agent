import streamlit as st
from pipeline import run_pipeline

# ------------ CUSTOM CSS (solo estilos, no cambia estructura) ------------
# ------------ CUSTOM CSS -----------------------
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* App Background */
.stApp {
    background-color: #f9f7f1 !important;  /* soft ivory */
    color: #2b2b2b !important;             /* neutral dark gray text */
}

/* Headings */
h1, h2, h3, h4, h5 {
    color: #2b2b2b !important;
    font-weight: 700;
}

/Section separators */
h2, h3 {
    border-bottom: 2px solid #b8d8c0 !important;  /* light green mint accent */
    padding-bottom: 0.3rem;
}

/* Text Inputs */
input[type="text"], input[type="number"], textarea {
    background-color: #ffffff !important;          /* white input background */
    color: #2b2b2b !important;                     /* dark gray text */
    border: 1px solid #dcd8cf !important;          /* subtle beige border */
    border-radius: 10px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);        /* soft shadow */
}
input::placeholder {
    color: #a9a9a9 !important;                     /* muted placeholder */
}

/* Selectbox main area */
div[data-testid="stSelectbox"] > div {
    background-color: #ffffff !important;
    color: #2b2b2b !important;
    border-radius: 10px !important;
    border: 1px solid #dcd8cf !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Dropdown list (open state) */
div[data-testid="stSelectbox"] ul {
    background-color: #ffffff !important;          /* white dropdown background */
    border-radius: 10px !important;
    border: 1px solid #cfe6d8 !important;          /* soft mint border */
}

/* Dropdown options */
div[data-testid="stSelectbox"] li,
div[data-testid="stSelectbox"] li span {
    color: #2b2b2b !important;                     /* readable dark text */
    font-weight: 500;
    background-color: #ffffff !important;
}

/* Hover & selected option */
div[data-testid="stSelectbox"] li:hover,
div[data-testid="stSelectbox"] li[data-highlighted="true"] {
    background-color: #e2f5ea !important;          /* light mint hover */
    color: #000000 !important;
}

/* Multiselect selected tags */
.stMultiSelect div[data-baseweb="tag"] {
    background-color: #b8e0c9 !important;          /* mint tag color */
    color: #2b2b2b !important;
    font-weight: 600;
    border-radius: 6px !important;
}

/* Buttons */
.stButton>button {
    background-color: #f8a3b3 !important;          /* pastel pink button */
    color: white !important;
    border-radius: 10px;
    border: none;
    font-size: 16px;
    padding: 0.6rem 1.2rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    transition: 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #f3839d !important;          /* darker pink on hover */
}

/* General text */
p, label, span, div {
    color: #2b2b2b !important;
}

/* Recommendation / result containers */
.block-container {
    background-color: #fdfcf9 !important;
    color: #2b2b2b !important;
    border-radius: 10px;
    padding: 1rem;
}
/* Add spacing below the Streamlit top bar (Deploy area) */
h1 {
    margin-top: 3rem !important;   /* pushes the title down */
    margin-bottom: 1.5rem !important; /* keeps good spacing below */
}

/* Optional: adjust the whole block container if needed */
.block-container {
    padding-top: 3rem !important;  /* adds padding between top bar and content */
}
</style>
""", unsafe_allow_html=True)


# ----------------- TU APP NORMAL -----------------
st.title("AI Skincare Multi-Agent System")

# 1) General Question
query = st.text_input(
    "Enter your skincare question:",
    ""
)

# 2) Skin type
skin_type = st.selectbox(
    "Skin Type",
    ["", "oily", "dry", "combination", "normal", "sensitive"]
)

# 3) Product type
product_type = st.selectbox(
    "Product Type",
    ["", "cleanser", "serum", "moisturizer", "sunscreen", "other"]
)

# 4) Budget
min_price_str = st.text_input("Min Price", value="", placeholder="0.00")
max_price_str = st.text_input("Max Price", value="", placeholder="0.00")

def parse_price(s: str) -> float:
    s = (s or "").strip()
    if s == "":
        # Si el usuario dejó vacío, lo tomamos como 0 (sin mostrar 0 en la caja)
        return 0.0
    try:
        return float(s)
    except ValueError:
        st.warning("Min/Max Price must be a number. Using 0 as default.")
        return 0.0

min_price = parse_price(min_price_str)
max_price = parse_price(max_price_str)

# 5) Main Skin Concern
main_concerns = st.multiselect(
    "Main Skin Concerns (choose up to 3)",
    ["acne", "redness", "hydration", "dark spots", "wrinkles", "sensitivity"]
)

if len(main_concerns) > 3:
    main_concerns = main_concerns[:3]

# 6) Age Range
age_range = st.selectbox(
    "Age Range",
    ["", "less_than_18", "18_to_25", "25_to_35", "35_to_45", "45_plus"]
)

# Ask the need to prioritize for sensible skin
needs_sensitive = st.checkbox(
    "Prioritize products suitable for sensitive skin",
    value=True
)

filters = {
    "skin_type": skin_type,
    "product_type": product_type,
    "min_price": min_price,
    "max_price": max_price,
    "main_concerns": main_concerns,
    "age_range": age_range,
    "needs_sensitive": needs_sensitive
}

if st.button("Run Consultation"):
    if len(main_concerns) == 0:
        st.warning("Please select at least one main concern.")
    else:
        summary, recs, score = run_pipeline(query, filters)

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Recommendations")
        for r in recs:
            st.markdown(r)
