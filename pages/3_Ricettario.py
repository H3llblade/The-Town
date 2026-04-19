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

# -------------------------
# CREAZIONE NUOVA RICETTA
# -------------------------

st.subheader("➕ Crea nuova ricetta")

nome_ricetta = st.text_input("Nome ricetta")

num_ingredienti = st.number_input("Numero ingredienti", min_value=1, step=1)

ingredienti = {}

for i in range(int(num_ingredienti)):
    col1, col2 = st.columns(2)

    with col1:
        ing = st.text_input(f"Ingrediente {i+1}", key=f"ing_{i}")

    with col2:
        qty = st.number_input(f"Quantità {i+1}", min_value=0.0, step=1.0, key=f"qty_{i}")

    if ing:
        ingredienti[ing.lower().strip()] = qty

# -------------------------
# SALVATAGGIO
# -------------------------

if st.button("💾 Salva ricetta"):

    if nome_ricetta and ingredienti:

        nome_ricetta = nome_ricetta.lower().strip()

        ricette[nome_ricetta] = {
            "ingredienti": ingredienti
        }

        save_data(ricette)

        st.success(f"Ricetta '{nome_ricetta}' salvata!")
        st.rerun()

    else:
        st.error("Inserisci nome e ingredienti")
