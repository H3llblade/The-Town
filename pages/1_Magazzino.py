import streamlit as st
import json
import os

FILE = "data/magazzino.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

st.title("📦 Magazzino")

data = load_data()

# Aggiunta ingrediente
st.subheader("Aggiungi / Aggiorna Ingrediente")

nome = st.text_input("Nome ingrediente")
quantita = st.number_input("Quantità", min_value=0.0, step=0.1)

if st.button("Salva"):
    if nome:
        data[nome] = quantita
        save_data(data)
        st.success("Salvato!")

# Visualizzazione
st.subheader("Stock attuale")

for ingrediente, qta in data.items():
    st.write(f"{ingrediente}: {qta}")
