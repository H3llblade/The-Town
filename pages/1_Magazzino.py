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

import streamlit as st

st.subheader("📦 Stock attuale")

if data:
    cols = st.columns(4)  # numero colonne (puoi cambiarlo)

    for i, (ingrediente, qta) in enumerate(data.items()):
        with cols[i % 4]:
            st.markdown(f"""
                <div style="
                    border-radius: 15px;
                    padding: 20px;
                    background-color: #1f2937;
                    text-align: center;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                    margin-bottom: 15px;
                ">
                    <div style="
                        font-size: 14px;
                        color: #9ca3af;
                        letter-spacing: 2px;
                    ">
                        {ingrediente.upper()}
                    </div>
                    <div style="
                        font-size: 40px;
                        font-weight: bold;
                        color: #ffffff;
                        margin-top: 10px;
                    ">
                        {qta}
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Nessun ingrediente in magazzino")
