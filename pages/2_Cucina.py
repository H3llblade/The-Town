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
# LOAD JSON
# -------------------------

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

magazzino = load_json(MAGAZZINO_FILE)
ricette = load_json(RICETTE_FILE)

# -------------------------
# CALCOLO PIATTI
# -------------------------

def calcola_piatti(ingredienti, magazzino):
    risultati = []

    for ing, qty_richiesta in ingredienti.items():

        disponibili = magazzino.get(ing, 0)

        if disponibili == 0:
            return 0

        risultati.append(disponibili // qty_richiesta)

    return int(min(risultati)) if risultati else 0

# -------------------------
# UI
# -------------------------

st.title("🍳 Cucina")

# -------------------------
# LOGICA
# -------------------------

if ricette:

    for categoria, lista_ricette in ricette.items():

        st.markdown(f"## 📂 {categoria}")

        for nome, info in lista_ricette.items():

            ingredienti = info.get("ingredienti", {})

            max_piatti = calcola_piatti(ingredienti, magazzino)

            st.markdown(f"### 🍽️ {nome}")

            if max_piatti > 0:
                st.success(f"Puoi cucinare: {max_piatti} piatti")
            else:
                st.error("Non puoi cucinare questa ricetta")

            st.write("Ingredienti:")

            for ing, qty in ingredienti.items():

                disponibili = magazzino.get(ing, 0)

                st.write(f"- {ing}: richiesti {qty} | disponibili {disponibili}")

            st.markdown("---")

else:
    st.info("Nessuna ricetta disponibile")
