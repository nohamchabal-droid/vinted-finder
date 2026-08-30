import streamlit as st
import pandas as pd
import urllib.parse

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Vinted Finder",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Vinted Finder")
st.caption("Ton assistant pour repérer et analyser les opportunités.")

# ============================================================
# MARQUES
# ============================================================

MARQUES = [
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
    "ASICS",
    "Patagonia",
    "Stone Island",
    "CP Company",
    "Arc'teryx",
    "Dickies",
    "Champion",
    "Columbia",
    "Fila",
    "Salomon",
]

ARTICLES = [
    "Half Zip",
    "Quarter Zip",
    "Zip",
    "Pull",
    "Sweat",
    "Hoodie",
    "Polo",
    "Veste",
    "Doudoune",
    "Pantalon",
    "Jogging",
    "T-shirt",
    "Chemise",
    "Jean",
    "Polaire",
]

ETATS = [
    "Neuf avec étiquette",
    "Neuf sans étiquette",
    "Très bon état",
    "Bon état",
    "Satisfaisant",
]

# ============================================================
# BARRE LATÉRALE
# ============================================================

st.sidebar.header("⚙️ Critères")

budget = st.sidebar.number_input(
    "💶 Prix maximum d'achat",
    min_value=1.0,
    max_value=1000.0,
    value=40.0,
    step=1.0
)

marge_min = st.sidebar.number_input(
    "💰 Marge minimum",
    min_value=0.0,
    max_value=1000.0,
    value=15.0,
    step=1.0
)

roi_min = st.sidebar.number_input(
    "📈 ROI minimum",
    min_value=0.0,
    max_value=1000.0,
    value=50.0,
    step=5.0
)

# ============================================================
# RECHERCHE VINTED
# ============================================================

st.subheader("🔍 Recherche Vinted")

col1, col2 = st.columns(2)

with col1:

    marque = st.selectbox(
        "🏷️ Marque",
        MARQUES
    )

with col2:

    article = st.selectbox(
        "👕 Article",
        ARTICLES
    )

prix_recherche = st.number_input(
    "💶 Budget maximum pour cette recherche",
    min_value=1,
    max_value=1000,
    value=30
)

recherche = f"{marque} {article}"

url_vinted = (
    "https://www.vinted.fr/catalog?search_text="
    + urllib.parse.quote_plus(recherche)
)

st.info(
    f"Recherche : **{recherche}** — jusqu'à **{prix_recherche} €**"
)

st.link_button(
    "🔎 Ouvrir la recherche Vinted",
    url_vinted
)

# ============================================================
# PRIX DE REVENTE DE RÉFÉRENCE
# ============================================================

PRIX_REVENTE = {

    "Ralph Lauren": {
        "Half Zip": 65,
        "Quarter Zip": 65,
        "Zip": 55,
        "Pull": 60,
        "Sweat": 55,
        "Hoodie": 60,
        "Polo": 45,
        "Veste": 75,
        "Doudoune": 100,
        "Pantalon": 50,
        "Jogging": 55,
        "T-shirt": 35,
        "Chemise": 50,
        "Jean": 55,
        "Polaire": 65,
    },

    "Nike": {
        "Half Zip": 55,
        "Quarter Zip": 55,
        "Zip": 50,
        "Pull": 45,
        "Sweat": 55,
        "Hoodie": 60,
        "Polo": 35,
        "Veste": 65,
        "Doudoune": 80,
        "Pantalon": 45,
        "Jogging": 55,
        "T-shirt": 30,
        "Chemise": 35,
        "Jean": 40,
        "Polaire": 55,
    },

    "Adidas": {
        "Half Zip": 45,
        "Quarter Zip": 45,
        "Zip": 40,
        "Pull": 40,
        "Sweat": 45,
        "Hoodie": 50,
        "Polo": 30,
        "Veste": 55,
        "Doudoune": 70,
        "Pantalon": 40,
        "Jogging": 45,
        "T-shirt": 25,
        "Chemise": 30,
        "Jean": 35,
        "Polaire": 45,
    },

    "Lacoste": {
        "Half Zip": 55,
        "Quarter Zip": 55,
        "Zip": 50,
        "Pull": 55,
        "Sweat": 50,
        "Hoodie": 55,
        "Polo": 45,
        "Veste": 70,
        "Doudoune": 90,
        "Pantalon": 45,
        "Jogging": 50,
        "T-shirt": 30,
        "Chemise": 50,
        "Jean": 45,
        "Polaire": 55,
    },

    "Carhartt": {
        "Half Zip": 55,
        "Quarter Zip": 55,
        "Zip": 55,
        "Pull": 55,
        "Sweat": 55,
        "Hoodie": 60,
        "Polo": 40,
        "Veste": 80,
        "Doudoune": 100,
        "Pantalon": 60,
        "Jogging": 50,
        "T-shirt": 30,
        "Chemise": 45,
        "Jean": 55,
        "Polaire": 60,
    },

    "The North Face": {
        "Half Zip": 60,
        "Quarter Zip": 60,
        "Zip": 60,
        "Pull": 55,
        "Sweat": 55,
        "Hoodie": 65,
        "Polo": 40,
        "Veste": 90,
        "Doudoune": 130,
        "Pantalon": 55,
        "Jogging": 50,
        "T-shirt": 30,
        "Chemise": 40,
        "Jean": 45,
        "Polaire": 70,
    },

    "Tommy Hilfiger": {
        "Half Zip": 60,
        "Quarter Zip": 60,
        "Zip": 55,
        "Pull": 55,
        "Sweat": 50,
        "Hoodie": 55,
        "Polo": 40,
        "Veste": 65,
        "Doudoune": 90,
        "Pantalon": 45,
        "Jogging": 45,
        "T-shirt": 30,
        "Chemise": 45,
        "Jean": 45,
        "Polaire": 55,
    },

    "Fred Perry": {
        "Half Zip": 60,
        "Quarter Zip": 60,
        "Zip": 55,
        "Pull": 60,
        "Sweat": 55,
        "Hoodie": 60,
        "Polo": 50,
        "Veste": 70,
        "Doudoune": 90,
        "Pantalon": 50,
        "Jogging": 50,
        "T-shirt": 35,
        "Chemise": 50,
        "Jean": 45,
        "Polaire": 60,
    },

    "Patagonia": {
        "Half Zip": 60,
        "Quarter Zip": 60,
        "Zip": 60,
        "Pull": 55,
        "Sweat": 55,
        "Hoodie": 60,
        "Polo": 40,
        "Veste": 90,
        "Doudoune": 120,
        "Pantalon": 60,
        "Jogging": 50,
        "T-shirt": 30,
        "Chemise": 40,
        "Jean": 45,
        "Polaire": 80,
    },
}

# ============================================================
# FONCTION ESTIMATION
# ============================================================

def trouver_marque(marque_annonce):

    texte = str(marque_annonce).lower()

    for marque_connue in PRIX_REVENTE:

        if marque_connue.lower() in texte:
            return marque_connue

    return None


def trouver_categorie(article):

    texte = str(article).lower()

    correspondances = {
        "half zip": "Half Zip",
        "quarter zip": "Quarter Zip",
        "zip": "Zip",
        "pull": "Pull",
        "sweat": "Sweat",
        "hoodie": "Hoodie",
        "polo": "Polo",
        "veste": "Veste",
        "doudoune": "Doudoune",
        "pantalon": "Pantalon",
        "jogging": "Jogging",
        "t-shirt": "T-shirt",
        "chemise": "Chemise",
        "jean": "Jean",
        "polaire": "Polaire",
    }

    for mot, categorie in correspondances.items():

        if mot in texte:
            return categorie

    return None


def estimer_revente(row):

    marque = trouver_marque(row["Marque"])

    categorie = trouver_categorie(
        row["Article"]
    )

    if marque is None:

        prix = 40

    elif categorie in PRIX_REVENTE[marque]:

        prix = PRIX_REVENTE[marque][categorie]

    else:

        prix = 45

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
# CHARGEMENT DES ANNONCES
# ============================================================

st.divider()

st.subheader("📦 Données des annonces")

try:

    annonces = pd.read_csv("annonces.csv")

except Exception as erreur:

    st.error(
        "❌ Le fichier annonces.csv est introuvable."
    )

    st.write(
        "Vérifie qu'il est bien à la racine de ton dépôt GitHub."
    )

    st.stop()

# ============================================================
# VÉRIFICATION
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
        "Colonnes manquantes dans annonces.csv : "
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
# ANALYSE
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
        score += 35

    elif marge >= 40:
        score += 30

    elif marge >= 30:
        score += 25

    elif marge >= 20:
        score += 18

    elif marge >= 10:
        score += 10

    # ROI
    if roi >= 200:
        score += 35

    elif roi >= 150:
        score += 30

    elif roi >= 100:
        score += 25

    elif roi >= 75:
        score += 20

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

st.subheader("📊 Résultats")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "🔥 Opportunités",
        len(resultats)
    )

with c2:

    st.metric(
        "💰 Marge moyenne",
        f"{resultats['Marge estimée'].mean():.0f} €"
        if len(resultats)
        else "—"
    )

with c3:

    st.metric(
        "📈 ROI moyen",
        f"{resultats['ROI estimé'].mean():.0f} %"
        if len(resultats)
        else "—"
    )

with c4:

    st.metric(
        "⭐ Meilleur score",
        f"{resultats['Score'].max()}/100"
        if len(resultats)
        else "—"
    )

# ============================================================
# TOP DES AFFAIRES
# ============================================================

st.subheader("🏆 TOP DES AFFAIRES")

if len(resultats) > 0:

    top_n = st.slider(
        "Nombre d'affaires à afficher",
        min_value=1,
        max_value=min(20, len(resultats)),
        value=min(5, len(resultats))
    )

    top_resultats = resultats.head(top_n)

    for rang, (_, annonce) in enumerate(
        top_resultats.iterrows(),
        start=1
    ):

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
            f"## #{rang} — {niveau}"
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
                f"✨ État : {annonce['Etat']}"
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
                "💰 Revente",
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

else:

    st.warning(
        "Aucune annonce ne correspond à tes critères."
    )

# ============================================================
# TABLEAU
# ============================================================

with st.expander("📋 Toutes les opportunités"):

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
        "Score",
        "URL"
    ]

    st.dataframe(
        resultats[colonnes_affichage],
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# EXPORT
# ============================================================

if len(resultats) > 0:

    csv = resultats.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Télécharger les opportunités",
        csv,
        "vinted_opportunites.csv",
        "text/csv"
    )

# ============================================================
# AVERTISSEMENT
# ============================================================

st.divider()

st.caption(
    "⚠️ Les prix de revente sont des estimations et non des garanties. "
    "Vérifie toujours l'article, son état et son authenticité avant tout achat."
)
