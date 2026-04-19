import streamlit as st
import json
import os

MAG_FILE = "data/magazzino.json"
RIC_FILE = "data/ricette.json"

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

magazzino = load_json(MAG_FILE)
ricette = load_json(RIC_FILE)

st.title("👨‍🍳 Cucina")

ricette_fattibili = []
ricette_non_fattibili = []

for nome, ingredienti in ricette.items():
    possibile = True
    
    for ing, qta in ingredienti.items():
        if ing not in magazzino or magazzino[ing] < qta:
            possibile = False
            break
    
    if possibile:
        ricette_fattibili.append(nome)
    else:
        ricette_non_fattibili.append(nome)

st.subheader("✅ Puoi cucinare")

for r in ricette_fattibili:
    st.success(r)

st.subheader("❌ Non puoi cucinare")

for r in ricette_non_fattibili:
    st.error(r)
