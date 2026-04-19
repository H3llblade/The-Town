import streamlit as st
import json
import os

# -------------------------
# PERCORSO FILE
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "ricette.json")

# -------------------------
# LOAD / SAVE
# -------------------------

def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({}, f)
        return {}

    with open(FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# CARICA RICETTE
# -------------------------

ricette = load_data()

# -------------------------
# UI
# -------------------------

st.title("📘 Ricettario")

st.subheader("📊 Ricette presenti")

# -------------------------
# MOSTRA RICETTE
# -------------------------

if ricette:

    for nome, info in ricette.items():

        st.markdown(f"### 🍽️ {nome}")

        ingredienti = info.get("ingredienti", {})

        for ing, qty in ingredienti.items():
            st.write(f"- {ing} → {qty}")

        st.markdown("---")

else:
    st.info("Nessuna ricetta presente")
