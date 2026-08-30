import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(
    page_title="Vinted Finder",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Vinted Finder")# ============================================================
# MOTEUR DE RECHERCHE VINTED
# ============================================================

st.subheader("🔍 Trouver une recherche")

marques_recherche = [
    "Ralph Lauren",
    "Nike",
    "Adidas",
    "Lacoste",
    "Carhartt",
    "The North Face",
    "Tommy Hilfiger",
    "Fred Perry",
    "Levi's",
    "New Balance",
    "Asics",
    "Patagonia",
]

articles_recherche = [
    "Half Zip",
    "Quarter Zip",
    "Zip",
    "Pull",
    "Sweat",
    "Hoodie",
    "Polo",
    "Veste",
    "Pantalon",
    "Jogging",
    "T-shirt",
]

marque_choisie = st.selectbox(
    "🏷️ Marque",
    marques_recherche
)

article_choisi = st.selectbox(
    "👕 Article",
    articles_recherche
)

prix_max_recherche = st.number_input(
    "💶 Prix maximum",
    min_value=1,
    max_value=500,
    value=30
)

recherche = f"{marque_choisie} {article_choisi}"

url_recherche = (
    "https://www.vinted.fr/catalog?search_text="
    + urllib.parse.quote_plus(recherche)
)

st.success(
    f"Recherche créée : **{recherche}** — maximum **{prix_max_recherche} €**"
)

st.link_button(
    "🔎 Rechercher sur Vinted",
    url_recherche
)

st.caption("Analyse automatiquement les opportunités d'achat-revente.")

# ============================================================
# PARAMÈTRES
# ============================================================

st.sidebar.header("⚙️ Tes critères")

budget = st.sidebar.number_input(
    "Prix maximum d'achat (€)",
    min_value=1.0,
    value=40.0,
    step=1.0
)

marge_min = st.sidebar.number_input(
    "Marge minimum (€)",
    min_value=0.0,
    value=15.0,
    step=1.0
)

roi_min = st.sidebar.number_input(
    "ROI minimum (%)",
    min_value=0.0,
    value=50.0,
    step=5.0
)

# ============================================================
# PRIX DE REVENTE DE RÉFÉRENCE
# ============================================================

PRIX_REVENTE = {
    "Ralph Lauren": {
        "Pull": 60,
        "Sweat": 55,
        "Polo": 45,
        "Veste": 75,
        "Pantalon": 50,
        "Hoodie": 60,
        "default": 50
    },

    "Nike": {
        "Pull": 45,
        "Sweat": 55,
        "Polo": 35,
        "Veste": 65,
        "Pantalon": 45,
        "Hoodie": 55,
        "default": 45
    },

    "Adidas": {
        "Pull": 40,
        "Sweat": 45,
        "Polo": 30,
        "Veste": 55,
        "Pantalon": 40,
        "Hoodie": 45,
        "default": 40
    },

    "Lacoste": {
        "Pull": 50,
        "Sweat": 50,
        "Polo": 45,
        "Veste": 65,
        "Pantalon": 45,
        "Hoodie": 50,
        "default": 45
    },

    "Carhartt": {
        "Pull": 55,
        "Sweat": 55,
        "Polo": 40,
        "Veste": 75,
        "Pantalon": 55,
        "Hoodie": 60,
        "default": 50
    },

    "The North Face": {
        "Pull": 55,
        "Sweat": 55,
        "Polo": 40,
        "Veste": 90,
        "Pantalon": 50,
        "Hoodie": 60,
        "default": 55
    },

    "Tommy Hilfiger": {
        "Pull": 55,
        "Sweat": 50,
        "Polo": 40,
        "Veste": 65,
        "Pantalon": 45,
        "Hoodie": 55,
        "default": 45
    },

    "Fred Perry": {
        "Pull": 60,
        "Sweat": 55,
        "Polo": 50,
        "Veste": 70,
        "Pantalon": 50,
        "Hoodie": 60,
        "default": 50
    }
}

# ============================================================
# ESTIMATION
# ============================================================

def trouver_marque(marque):

    marque = str(marque).lower()

    for vraie_marque in PRIX_REVENTE:

        if vraie_marque.lower() in marque:
            return vraie_marque

    return None


def estimer_revente(row):

    marque = trouver_marque(row["Marque"])
    categorie = str(row["Categorie"])

    if marque is None:
        prix = 40
    else:

        donnees = PRIX_REVENTE[marque]

        prix = donnees.get(
            categorie,
            donnees["default"]
        )

    # Ajustement selon l'état
    etat = str(row["Etat"]).lower()

    if "neuf avec" in etat:
        prix *= 1.15

    elif "neuf sans" in etat:
        prix *= 1.10

    elif "très bon" in etat:
        prix *= 1.00

    elif "bon état" in etat:
        prix *= 0.85

    elif "satisfaisant" in etat:
        prix *= 0.65

    return round(prix, 2)


# ============================================================
# CHARGEMENT
# ============================================================

try:

    annonces = pd.read_csv("annonces.csv")

except Exception as e:

    st.error("Impossible de charger annonces.csv")
    st.code(str(e))
    st.stop()


# ============================================================
# COLONNES
# ============================================================

colonnes_obligatoires = [
    "Article",
    "Marque",
    "Categorie",
    "Prix",
    "Etat",
    "Taille",
    "URL"
]

manquantes = [
    colonne
    for colonne in colonnes_obligatoires
    if colonne not in annonces.columns
]

if manquantes:

    st.error(
        "Colonnes manquantes : "
        + ", ".join(manquantes)
    )

    st.stop()


# ============================================================
# NETTOYAGE
# ============================================================

annonces["Prix"] = pd.to_numeric(
    annonces["Prix"],
    errors="coerce"
)

annonces = annonces.dropna(
    subset=["Prix"]
)

# ============================================================
# NOUVELLE ESTIMATION
# ============================================================

annonces["Revente estimée"] = annonces.apply(
    estimer_revente,
    axis=1
)

annonces["Marge estimée"] = (
    annonces["Revente estimée"]
    - annonces["Prix"]
)

annonces["ROI estimé"] = (
    annonces["Marge estimée"]
    / annonces["Prix"]
    * 100
)

# ============================================================
# SCORE
# ============================================================

def calcul_score(row):

    score = 0

    marge = row["Marge estimée"]
    roi = row["ROI estimé"]

    # Marge
    if marge >= 50:
        score += 40
    elif marge >= 40:
        score += 35
    elif marge >= 30:
        score += 30
    elif marge >= 20:
        score += 22
    elif marge >= 10:
        score += 12

    # ROI
    if roi >= 200:
        score += 40
    elif roi >= 150:
        score += 35
    elif roi >= 100:
        score += 30
    elif roi >= 75:
        score += 22
    elif roi >= 50:
        score += 15

    # État
    etat = str(row["Etat"]).lower()

    if "neuf avec" in etat:
        score += 20
    elif "neuf sans" in etat:
        score += 18
    elif "très bon" in etat:
        score += 15
    elif "bon état" in etat:
        score += 8

    return min(score, 100)


annonces["Score"] = annonces.apply(
    calcul_score,
    axis=1
)

# ============================================================
# FILTRES
# ============================================================

resultats = annonces[
    (annonces["Prix"] <= budget)
    &
    (annonces["Marge estimée"] >= marge_min)
    &
    (annonces["ROI estimé"] >= roi_min)
].copy()

resultats = resultats.sort_values(
    by="Score",
    ascending=False
)

# ============================================================
# STATISTIQUES
# ============================================================

st.divider()

st.subheader("📊 Résultats")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Opportunités",
        len(resultats)
    )

with c2:

    if len(resultats):
        st.metric(
            "Marge moyenne",
            f"{resultats['Marge estimée'].mean():.0f} €"
        )
    else:
        st.metric(
            "Marge moyenne",
            "—"
        )

with c3:

    if len(resultats):
        st.metric(
            "ROI moyen",
            f"{resultats['ROI estimé'].mean():.0f} %"
        )
    else:
        st.metric(
            "ROI moyen",
            "—"
        )

with c4:

    if len(resultats):
        st.metric(
            "Meilleur score",
            f"{resultats['Score'].max()}/100"
        )
    else:
        st.metric(
            "Meilleur score",
            "—"
        )

# ============================================================
# MEILLEURES AFFAIRES
# ============================================================

st.subheader("🔥 Meilleures opportunités")

if len(resultats) == 0:

    st.warning(
        "Aucune opportunité ne correspond aux critères."
    )

else:

    for _, annonce in resultats.iterrows():

        score = annonce["Score"]

        if score >= 85:
            niveau = "🔥 EXCELLENTE AFFAIRE"
        elif score >= 70:
            niveau = "🟢 BONNE AFFAIRE"
        elif score >= 50:
            niveau = "🟡 À ÉTUDIER"
        else:
            niveau = "🔴 FAIBLE"

        st.markdown(
            f"## {niveau}"
        )

        gauche, droite = st.columns([3, 1])

        with gauche:

            st.markdown(
                f"### {annonce['Article']}"
            )

            st.write(
                f"🏷️ **{annonce['Marque']}**"
            )

            st.write(
                f"📦 {annonce['Categorie']}"
            )

            st.write(
                f"📏 Taille : {annonce['Taille']}"
            )

            st.write(
                f"✨ {annonce['Etat']}"
            )

            if str(annonce["URL"]).startswith("http"):

                st.link_button(
                    "🔗 Voir l'annonce",
                    annonce["URL"]
                )

        with droite:

            st.metric(
                "💶 Achat",
                f"{annonce['Prix']:.2f} €"
            )

            st.metric(
                "💰 Revente estimée",
                f"{annonce['Revente estimée']:.2f} €"
            )

            st.metric(
                "📈 Marge",
                f"{annonce['Marge estimée']:.2f} €"
            )

            st.metric(
                "📊 ROI",
                f"{annonce['ROI estimé']:.0f} %"
            )

            st.metric(
                "⭐ Score",
                f"{annonce['Score']}/100"
            )

        st.divider()

# ============================================================
# TABLEAU
# ============================================================

with st.expander("📋 Voir toutes les opportunités"):

    colonnes_affichage = [
        "Article",
        "Marque",
        "Categorie",
        "Prix",
        "Revente estimée",
        "Marge estimée",
        "ROI estimé",
        "Etat",
        "Taille",
        "Score"
    ]

    st.dataframe(
        resultats[colonnes_affichage],
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# AVERTISSEMENT
# ============================================================

st.caption(
    "⚠️ Les prix de revente sont des estimations. "
    "Ils ne garantissent pas le prix auquel l'article sera vendu."
)
