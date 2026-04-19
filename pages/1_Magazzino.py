import streamlit as st
import json
import os

FILE = "data/magazzino.json"

# -------------------------
# FUNZIONI
# -------------------------

def load_data():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({}, f)
        return {}

    try:
        with open(FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.load(f)
    except:
        return {}

def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# UI
# -------------------------

st.title("📦 Magazzino")

data = load_data()

# -------------------------
# INPUT
# -------------------------

st.subheader("➕ Aggiungi / Aggiorna prodotto")

nome = st.text_input("Nome prodotto")
quantita = st.number_input("Quantità", min_value=0.0, step=1.0)

if st.button("Salva"):
    if nome:
        nome = nome.lower().strip()
        data[nome] = quantita
        save_data(data)

        st.success("Salvato correttamente!")
        st.rerun()

# -------------------------
# VISUALIZZAZIONE SEMPLICE (NO HTML)
# -------------------------

st.subheader("📊 Stock attuale")

if data:
    for prodotto, qta in data.items():
        st.write(f"{prodotto} → {qta}")
else:
    st.info("Magazzino vuoto")
