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
            return json.loads(content)
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

st.subheader("➕ Aggiungi / Aggiorna ingrediente")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome prodotto")

with col2:
    quantita = st.number_input("Quantità", min_value=0.0, step=1.0)

# -------------------------
# SALVATAGGIO
# -------------------------

if st.button("Salva"):
    if nome:
        nome = nome.lower().strip()

        data[nome] = quantita

        save_data(data)

        st.success("Salvato correttamente!")
        st.rerun()

# -------------------------
# VISUALIZZAZIONE STOCK (CARD CORRETTE)
# -------------------------

st.subheader("📊 Stock attuale")

if data:
    cols = st.columns(4)

    for i, (prodotto, qta) in enumerate(data.items()):
        with cols[i % 4]:

            colore = "#16a34a" if qta > 5 else "#dc2626"

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
                        {prodotto.upper()}
                    </div>

                    <div style="
                        font-size: 40px;
                        font-weight: bold;
                        color: {colore};
                        margin-top: 10px;
                    ">
                        {qta}
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.info("Magazzino vuoto")
