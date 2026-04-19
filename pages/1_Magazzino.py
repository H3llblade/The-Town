import streamlit as st
import json
import os

# -------------------------
# PERCORSO FILE
# -------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "magazzino.json")

# -------------------------
# LOAD DATA
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

# -------------------------
# CARICA INVENTARIO
# -------------------------

data = load_data()

# -------------------------
# UI
# -------------------------

st.title("📦 Magazzino")

st.subheader("📊 Inventario prodotti")

# -------------------------
# RICHIAMO DATI
# -------------------------

if data:

    cols = st.columns(3)  # griglia 3 colonne

    i = 0

    for prodotto, quantita in data.items():

        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="
                    background-color: #1f2937;
                    padding: 15px;
                    border-radius: 12px;
                    text-align: center;
                    margin-bottom: 10px;
                    color: white;
                ">
                    <div style="font-size:18px; font-weight:bold; text-transform:uppercase;">
                        {prodotto}
                    </div>
                    <div style="font-size:32px; margin-top:10px;">
                        {quantita}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        i += 1

else:
    st.info("Magazzino vuoto")
