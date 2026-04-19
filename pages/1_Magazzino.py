import streamlit as st
import json
import os

# -------------------------
# PERCORSO REALE FILE
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "magazzino.json")

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
# CARICA INVENTARIO
# -------------------------

data = load_data()

# -------------------------
# UI
# -------------------------

st.title("📦 Magazzino")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Prodotto")

with col2:
    quantita = st.number_input("Quantità", min_value=0.0, step=1.0)

# -------------------------
# AGGIUNTA / UPDATE
# -------------------------

if st.button("Aggiungi / Aggiorna"):
    if nome and quantita is not None:

        nome = nome.lower().strip()

        if nome in data:
            data[nome] += quantita
        else:
            data[nome] = quantita

        save_data(data)

        st.success(f"Salvato: {nome} → {data[nome]}")
        st.rerun()

# -------------------------
# VISUALIZZAZIONE INVENTARIO
# -------------------------

st.subheader("📊 Inventario")

data = load_data()

if data:
    for prodotto, qty in data.items():
        st.write(f"{prodotto} → {qty}")
else:
    st.info("Magazzino vuoto")
