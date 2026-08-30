import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Vinted Finder",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Vinted Finder")
st.write("Trouve et analyse les meilleures opportunités d'achat-revente.")

# -----------------------------
# PARAMÈTRES
# -----------------------------

st.sidebar.header("⚙️ Tes critères")

budget = st.sidebar.number_input(
    "Prix d'achat maximum (€)",
    min_value=1.0,
    value=40.0
)

marge_min = st.sidebar.number_input(
    "Marge minimum souhaitée (€)",
    min_value=0.0,
    value=20.0
)

marques = st.sidebar.text_input(
    "Marques recherchées",
    "Ralph Lauren, Nike, Adidas, Lacoste, Carhartt, The North Face"
)

mots_cles = st.sidebar.text_input(
    "Articles recherchés",
    "zip, half zip, pull, sweat, veste, polo, pantalon"
)

# -----------------------------
# DONNÉES
# -----------------------------

annonces = pd.DataFrame([
    {
        "Article": "Ralph Lauren Half-Zip bleu marine",
        "Marque": "Ralph Lauren",
        "Catégorie": "Pull",
        "Prix": 25,
        "Revente estimée": 60,
        "État": "Très bon état",
        "Taille": "M"
    },
    {
        "Article": "Ralph Lauren Quarter-Zip gris",
        "Marque": "Ralph Lauren",
        "Catégorie": "Pull",
        "Prix": 30,
        "Revente estimée": 65,
        "État": "Très bon état",
        "Taille": "L"
    },
    {
        "Article": "Nike Tech Fleece",
        "Marque": "Nike",
        "Catégorie": "Ensemble",
        "Prix": 45,
        "Revente estimée": 70,
        "État": "Bon état",
        "Taille": "M"
    },
    {
        "Article": "Lacoste Pull Vintage",
        "Marque": "Lacoste",
        "Catégorie": "Pull",
        "Prix": 18,
        "Revente estimée": 45,
        "État": "Très bon état",
        "Taille": "M"
    },
    {
        "Article": "Carhartt Sweat",
        "Marque": "Carhartt",
        "Catégorie": "Sweat",
        "Prix": 28,
        "Revente estimée": 60,
        "État": "Très bon état",
        "Taille": "L"
    }
])

# -----------------------------
# FILTRES
# -----------------------------

marques_liste = [
    marque.strip().lower()
    for marque in marques.split(",")
]

annonces = annonces[
    annonces["Marque"].str.lower().isin(marques_liste)
]

annonces = annonces[
    annonces["Prix"] <= budget
]

# -----------------------------
# CALCULS
# -----------------------------

annonces["Marge"] = (
    annonces["Revente estimée"]
    - annonces["Prix"]
)

annonces["ROI"] = (
    annonces["Marge"]
    / annonces["Prix"]
    * 100
)

def calcul_score(row):

    score = 0

    # Marge
    if row["Marge"] >= 40:
        score += 40
    elif row["Marge"] >= 30:
        score += 32
    elif row["Marge"] >= 20:
        score += 24
    elif row["Marge"] >= 10:
        score += 12

    # ROI
    if row["ROI"] >= 100:
        score += 35
    elif row["ROI"] >= 70:
        score += 28
    elif row["ROI"] >= 50:
        score += 20
    elif row["ROI"] >= 30:
        score += 10

    # État
    if row["État"] == "Très bon état":
        score += 15
    elif row["État"] == "Bon état":
        score += 8

    # Bonus marques
    if row["Marque"] == "Ralph Lauren":
        score += 10

    return min(score, 100)

annonces["Score"] = annonces.apply(
    calcul_score,
    axis=1
)

# -----------------------------
# FILTRE MARGE
# -----------------------------

resultats = annonces[
    annonces["Marge"] >= marge_min
].sort_values(
    "Score",
    ascending=False
)

# -----------------------------
# AFFICHAGE
# -----------------------------

st.subheader("🔥 Meilleures opportunités")

if len(resultats) == 0:

    st.warning(
        "Aucune affaire ne correspond à tes critères."
    )

else:

    for _, article in resultats.iterrows():

        if article["Score"] >= 85:
            niveau = "🔥 EXCELLENTE AFFAIRE"
        elif article["Score"] >= 70:
            niveau = "🟢 BONNE AFFAIRE"
        else:
            niveau = "🟡 À ÉTUDIER"

        st.markdown(
            f"""
            ## {niveau}

            **{article['Article']}**

            💰 Achat : **{article['Prix']} €**

            📈 Revente estimée :
            **{article['Revente estimée']} €**

            💵 Marge potentielle :
            **{article['Marge']} €**

            📊 ROI :
            **{article['ROI']:.0f} %**

            ⭐ Score :
            **{article['Score']}/100**

            👕 Taille : **{article['Taille']}**

            📦 État : **{article['État']}**
            """
        )

        st.divider()

st.caption(
    "Les prix de revente sont des estimations : "
    "vérifie toujours l'état, l'authenticité, les frais et la demande."
)
