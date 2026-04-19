import streamlit as st
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data", "magazzino.json")

# -------------------------
# LOAD / SAVE SICURI
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
            return json.loads(content)
    except:
        return {}

def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# CARICA SEMPRE DAL FILE
# -------------------------

data = load_data()

# -------------------------
# UI
# -------------------------

st.title("📦 Magazzino")

st.subheader("➕ Aggiungi prodotto")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome prodotto")

with col2:
    quantita = st.number_input("Quantità", min_value=0.0, step=1.0)

# -------------------------
# AGGIORNAMENTO FILE
# -------------------------

if st.button("Aggiungi / Aggiorna"):
    if nome:
        nome = nome.lower().strip()

        # se esiste lo somma, altrimenti crea
        if nome in data:
            data[nome] += quantita
        else:
            data[nome] = quantita

        save_data(data)

        st.success(f"{nome} aggiornato nel magazzino")

        st.rerun()

# -------------------------
# VISUALIZZAZIONE
# -------------------------

st.subheader("📊 Stock attuale (da file JSON)")

data = load_data()  # 🔥 ricarica sempre dal file

if data:
    for prodotto, qta in data.items():
        st.write(f"{prodotto} → {qta}")
else:
    st.info("Magazzino vuoto")
