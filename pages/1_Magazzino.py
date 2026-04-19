import streamlit as st
import json
import os

FILE = "data/magazzino.json"

# -------------------------
# FUNZIONI
# -------------------------

def load_data():
    if not os.path.exists(FILE):
        os.makedirs("data", exist_ok=True)
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

st.subheader("➕ Aggiungi / Aggiorna Ingrediente")

col1, col2, col3 = st.columns(3)

with col1:
    nome = st.text_input("Ingrediente")

with col2:
    quantita = st.number_input("Quantità", min_value=0.0, step=1.0)

with col3:
    unita = st.selectbox("Unità", ["pz", "kg", "litri"])

# -------------------------
# SALVATAGGIO CORRETTO
# -------------------------

if st.button("Salva"):
    if nome:
        nome = nome.lower().strip()

        if nome in data:
            data[nome]["quantita"] = quantita
            data[nome]["unita"] = unita
        else:
            data[nome] = {
                "quantita": quantita,
                "unita": unita
            }

        save_data(data)

        st.success("Salvato correttamente!")

        # DEBUG (importantissimo)
        st.write("DEBUG DATI SALVATI:", data)

        st.rerun()

# -------------------------
# VISUALIZZAZIONE A RIQUADRI
# -------------------------

st.subheader("📊 Stock attuale")

if data:
    cols = st.columns(4)

    for i, (ingrediente, info) in enumerate(data.items()):
        with cols[i % 4]:

            qta = info["quantita"]
            unita = info["unita"]

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
                        {ingrediente.upper()}
                    </div>
                    <div style="
                        font-size: 40px;
                        font-weight: bold;
                        color: {colore};
                        margin-top: 10px;
                    ">
                        {qta}
                    </div>
                    <div style="
                        font-size: 12px;
                        color: #9ca3af;
                    ">
                        {unita}
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.info("Magazzino vuoto")
