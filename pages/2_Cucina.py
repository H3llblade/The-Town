import streamlit as st
import json
import os

# -------------------------
# CONFIG PAGINA (FULL WIDTH)
# -------------------------

st.set_page_config(layout="wide")

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

CARD_STYLE = """
<div style="
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 12px;
    height: 220px;
    overflow: hidden;
">
"""

if ricette:

    for categoria, lista_ricette in ricette.items():

        st.markdown(f"## 📂 {categoria}")

        items = list(lista_ricette.items())

        for i in range(0, len(items), 4):

            cols = st.columns(4)

            for j in range(4):

                if i + j < len(items):

                    nome, info = items[i + j]
                    ingredienti = info.get("ingredienti", {})

                    max_piatti = calcola_piatti(ingredienti, magazzino)

                    with cols[j]:

                        # ---------------- CARD FIXED ----------------
                        st.markdown(CARD_STYLE, unsafe_allow_html=True)

                        st.markdown(f"### 🍽️ {nome}")

                        if max_piatti > 0:
                            st.success(f"✔ {max_piatti} piatti cucinabili")
                        else:
                            st.error("✖ Non cucinabile")

                        st.markdown("**Ingredienti:**")

                        for ing, qty in ingredienti.items():
                            disp = magazzino.get(ing, 0)
                            st.write(f"{ing}: {qty} (disp {disp})")

                        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

else:
    st.info("Nessuna ricetta disponibile")
