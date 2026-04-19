import streamlit as st
import json
import os

# -------------------------
# ROOT PROGETTO (NON /pages)
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

    try:
        with open(FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except:
        return {}

def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# DEBUG PATH (IMPORTANTISSIMO)
# -------------------------

st.write("📁 FILE LETTO:", FILE)

# -------------------------
# CARICA DATI
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
# SALVATAGGIO
# -------------------------

if st.button("Aggiungi / Aggiorna"):
    if nome:
        nome = nome.lower().strip()

        if nome in data:
            data[nome] += quantita
        else:
            data[nome] = quantita

        save_data(data)

        st.success("Salvato correttamente")
        st.rerun()

# -------------------------
# VISUALIZZAZIONE
# -------------------------

st.subheader("📊 Magazzino")

data = load_data()

if data:
    for k, v in data.items():
        st.write(f"{k} → {v}")
else:
    st.warning("Magazzino vuoto")
