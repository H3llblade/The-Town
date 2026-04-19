import streamlit as st
import json
import os

# -------------------------
# PATH
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

MAGAZZINO_FILE = os.path.join(DATA_DIR, "magazzino.json")
RICETTE_FILE = os.path.join(DATA_DIR, "ricette.json")

# -------------------------
# LOAD
# -------------------------

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

magazzino = load_json(MAGAZZINO_FILE)
ricette = load_json(RICETTE_FILE)

# -------------------------
# CALCOLO
# -------------------------

def calcola_piatti(ingredienti, magazzino):
    valori = []

    for ing, qty in ingredienti.items():
        if ing not in magazzino:
            return 0
        valori.append(magazzino[ing] // qty)

    return int(min(valori)) if valori else 0

# -------------------------
# UI
# -------------------------

st.title("🍳 Cucina")

if ricette:

    for categoria, lista_ricette in ricette.items():

        st.markdown(f"## 📂 {categoria}")

        cols = st.columns(2)  # 🔥 layout a griglia

        i = 0

        for nome, info in lista_ricette.items():

            ingredienti = info.get("ingredienti", {})
            max_piatti = calcola_piatti(ingredienti, magazzino)

            with cols[i % 2]:

                # ---------------- CARD ----------------
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 12px;
                        padding: 12px;
                        margin-bottom: 10px;
                        background-color: #fafafa;
                        height: 180px;
                    ">
                        <h4 style="margin-bottom:5px;">🍽️ {nome}</h4>
                        <p><b>Produzione:</b> {max_piatti} piatti</p>
                        <p style="font-size:12px;">
                    """,
                    unsafe_allow_html=True
                )

                # ingredienti compatti
                ing_text = ""
                for ing, qty in ingredienti.items():
                    ing_text += f"{ing} ({qty}) • "

                st.markdown(ing_text[:-3], unsafe_allow_html=True)

                st.markdown("</p></div>", unsafe_allow_html=True)

            i += 1

        st.markdown("---")

else:
    st.info("Nessuna ricetta disponibile")
