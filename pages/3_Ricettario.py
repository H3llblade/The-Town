import streamlit as st
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILE = os.path.join(BASE_DIR, "data", "ricette.json")

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

ricette = load_data()

st.title("📘 Ricettario")

if ricette:

    for categoria, lista_ricette in ricette.items():

        st.markdown(f"## 📂 {categoria}")

        # 👇 QUESTO È IL PEZZO CHE TI MANCAVA
        for nome, info in lista_ricette.items():

            st.markdown(f"### 🍽️ {nome}")

            ingredienti = info.get("ingredienti", {})

            for ing, qty in ingredienti.items():
                st.write(f"- {ing} → {qty}")

            st.markdown("---")

else:
    st.info("Nessuna ricetta presente")
