import streamlit as st
import json
import os

# -------------------------
# PERCORSI
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

MAGAZZINO_FILE = os.path.join(DATA_DIR, "magazzino.json")
RICETTE_FILE = os.path.join(DATA_DIR, "ricette.json")

# -------------------------
# LOAD DATA
# -------------------------

def load_json(file):
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
        return {}

    with open(file, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

magazzino = load_json(MAGAZZINO_FILE)
ricette = load_json(RICETTE_FILE)

# -------------------------
# UI
# -------------------------

st.title("🍳 Cucina")

st.subheader("📊 Piatti producibili")

# -------------------------
# CALCOLO
# -------------------------

def calcola_massimo(ricetta_ingredienti, magazzino):
    valori = []

    for ing, qty_richiesta in ricetta_ingredienti.items():

        if ing not in magazzino:
            return 0  # ingrediente mancante → zero piatti

        valori.append(magazzino[ing] // qty_richiesta)

    return int(min(valori)) if valori else 0

# -------------------------
# MOSTRA RISULTATI
# -------------------------

if ricette:

    for nome, info in ricette.items():

        ingredienti = info.get("ingredienti", {})

        max_piatti = calcola_massimo(ingredienti, magazzino)

        st.markdown(f"### 🍽️ {nome}")

        if max_piatti > 0:
            st.success(f"Puoi cucinare: {max_piatti} piatti")
        else:
            st.error("Non puoi cucinare questa ricetta")

        st.write("Ingredienti richiesti:")

        for ing, qty in ingredienti.items():

            disponibili = magazzino.get(ing, 0)

            st.write(f"- {ing}: richiesti {qty} | disponibili {disponibili}")

        st.markdown("---")

else:
    st.info("Nessuna ricetta disponibile")
