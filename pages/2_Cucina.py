import streamlit as st
import json
import os

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(layout="wide")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

MAGAZZINO_FILE = os.path.join(DATA_DIR, "magazzino.json")
RICETTE_FILE = os.path.join(DATA_DIR, "ricette.json")

# -------------------------
# LOAD
# -------------------------

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

magazzino = load_json(MAGAZZINO_FILE)
ricette = load_json(RICETTE_FILE)

# -------------------------
# CALCOLO
# -------------------------

def calcola_piatti(ingredienti, magazzino):
    valori = []

    for ing, qty in ingredienti.items():
        if ing not in magazzino:
            return 0
        valori.append(magazzino[ing] // qty)

    return int(min(valori)) if valori else 0

# -------------------------
# SIDEBAR FILTRI
# -------------------------

st.sidebar.title("🔧 Filtri")

solo_cucinabili = st.sidebar.checkbox("✔ Solo cucinabili")
categoria_filtro = st.sidebar.selectbox(
    "📂 Categoria",
    ["TUTTE"] + list(ricette.keys()) if ricette else ["TUTTE"]
)

ordina = st.sidebar.selectbox(
    "📊 Ordina per",
    ["Più cucinabili", "Nome"]
)

# -------------------------
# UI
# -------------------------

st.title("🍳 Dashboard Cucina Ristorante")

# -------------------------
# RACCOLTA DATI PIATTI
# -------------------------

piatti = []

for categoria, lista_ricette in ricette.items():

    if categoria_filtro != "TUTTE" and categoria != categoria_filtro:
        continue

    for nome, info in lista_ricette.items():

        ingredienti = info.get("ingredienti", {})
        max_piatti = calcola_piatti(ingredienti, magazzino)

        piatti.append({
            "categoria": categoria,
            "nome": nome,
            "ingredienti": ingredienti,
            "max": max_piatti
        })

# -------------------------
# ORDINAMENTO
# -------------------------

if ordina == "Più cucinabili":
    piatti.sort(key=lambda x: x["max"], reverse=True)
else:
    piatti.sort(key=lambda x: x["nome"])

# -------------------------
# FILTRO CUCINABILI
# -------------------------

if solo_cucinabili:
    piatti = [p for p in piatti if p["max"] > 0]

# -------------------------
# DISPLAY GRID
# -------------------------

cols_per_row = 4

for i in range(0, len(piatti), cols_per_row):

    cols = st.columns(cols_per_row)

    for j in range(cols_per_row):

        if i + j < len(piatti):

            p = piatti[i + j]

            nome = p["nome"]
            categoria = p["categoria"]
            ingredienti = p["ingredienti"]
            max_piatti = p["max"]

            with cols[j]:

                # ---------------- CARD ----------------
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 12px;
                        padding: 12px;
                        height: 240px;
                        overflow: hidden;
                        background: white;
                    ">
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(f"### 🍽️ {nome}")
                st.caption(f"📂 {categoria}")

                # STATUS COLORATO
                if max_piatti > 5:
                    st.success(f"✔ {max_piatti} piatti")
                elif max_piatti > 0:
                    st.warning(f"⚠ {max_piatti} piatti")
                else:
                    st.error("✖ non cucinabile")

                st.markdown("**Ingredienti:**")

                for ing, qty in ingredienti.items():
                    disp = magazzino.get(ing, 0)
                    st.write(f"- {ing}: {qty} (disp {disp})")

                st.markdown("</div>", unsafe_allow_html=True)
