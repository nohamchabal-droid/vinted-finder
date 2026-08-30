import streamlit as st
import pandas as pd
import urllib.parse
import re

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Vinted Finder",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Vinted Finder")
st.caption("Analyseur d'opportunités d'achat-revente")

# ============================================================
# LISTES
# ============================================================

MARQUES = [
    "Toutes",
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
    "Tous",
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

# ============================================================
# PRIX DE RÉFÉRENCE
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
        "Polaire": 80,
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
# FONCTIONS
# ============================================================

def trouver_marque(texte):

    texte = str(texte).lower()

    for marque in PRIX_REVENTE:

        if marque.lower() in texte:
            return marque

    return None


def trouver_article(texte):

    texte = str(texte).lower()

    correspondances = [
        ("half zip", "Half Zip"),
        ("half-zip", "Half Zip"),
        ("quarter zip", "Quarter Zip"),
        ("quarter-zip", "Quarter Zip"),
        ("hoodie", "Hoodie"),
        ("sweat", "Sweat"),
        ("polo", "Polo"),
        ("doudoune", "Doudoune"),
        ("polaire", "Polaire"),
        ("jogging", "Jogging"),
        ("pantalon", "Pantalon"),
        ("chemise", "Chemise"),
        ("t-shirt", "T-shirt"),
        ("tshirt", "T-shirt"),
        ("jean", "Jean"),
        ("veste", "Veste"),
        ("pull", "Pull"),
        ("zip", "Zip"),
    ]

    for mot, article in correspondances:

        if mot in texte:
            return article

    return None


def estimer_revente(row):

    marque = trouver_marque(
        f"{row['Marque']} {row['Article']}"
    )

    article = trouver_article(
        f"{row['Article']} {row['Categorie']}"
    )

    if marque and article:

        prix = PRIX_REVENTE[marque].get(
            article,
            45
        )

    elif marque:

        prix = 45

    else:

        prix = 35

    # Ajustement état
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

    # Etat
    etat = str(row["Etat"]).lower()

    if "neuf avec" in etat:
        score += 20
    elif "neuf sans" in etat:
        score += 18
    elif "très bon" in etat:
        score += 15
    elif "bon état" in etat:
        score += 8

    # Marque reconnue
    marque = trouver_marque(
        f"{row['Marque']} {row['Article']}"
    )

    if marque:
        score += 10

    return min(score, 100)


def analyser_annonces(df):

    df = df.copy()

    df["Prix"] = pd.to_numeric(
        df["Prix"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Prix"]
    )

    df["Revente estimée"] = df.apply(
        estimer_revente,
        axis=1
    )

    df["Marge estimée"] = (
        df["Revente estimée"]
        - df["Prix"]
    )

    df["ROI estimé"] = (
        df["Marge estimée"]
        / df["Prix"].replace(0, 1)
        * 100
    )

    df["Score"] = df.apply(
        calcul_score,
        axis=1
    )

    return df


# ============================================================
# IMPORT DES ANNONCES
# ============================================================

st.sidebar.header("📥 Données")

fichier = st.sidebar.file_uploader(
    "Importer un fichier CSV",
    type=["csv"]
)

# ============================================================
# CHARGEMENT
# ============================================================

if fichier is not None:

    try:

        annonces = pd.read_csv(
            fichier
        )

        st.sidebar.success(
            "✅ Fichier importé"
        )

    except Exception as erreur:

        st.error(
            f"Impossible de lire le fichier : {erreur}"
        )

        st.stop()

else:

    try:

        annonces = pd.read_csv(
            "annonces.csv"
        )

        st.sidebar.info(
            "📄 Utilisation de annonces.csv"
        )

    except:

        annonces = pd.DataFrame()


# ============================================================
# DONNÉES VIDES
# ============================================================

if annonces.empty:

    st.info(
        "📥 Importe ton fichier CSV pour commencer."
    )

    st.markdown(
        """
### Format recommandé

Ton fichier doit contenir au minimum :

`Article | Marque | Categorie | Prix | Etat | Taille | URL`

Exemple :

`Half Zip | Ralph Lauren | Pull | 25 | Très bon état | M | https://...`
        """
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
    c for c in colonnes_obligatoires
    if c not in annonces.columns
]

if manquantes:

    st.error(
        "❌ Colonnes manquantes : "
        + ", ".join(manquantes)
    )

    st.info(
        "Colonnes nécessaires : "
        + ", ".join(colonnes_obligatoires)
    )

    st.stop()


# ============================================================
# ANALYSE
# ============================================================

annonces = analyser_annonces(
    annonces
)

# ============================================================
# FILTRES
# ============================================================

st.sidebar.header("🎯 Filtres")

budget = st.sidebar.number_input(
    "Prix maximum (€)",
    min_value=1.0,
    max_value=1000.0,
    value=40.0,
    step=1.0
)

marge_min = st.sidebar.number_input(
    "Marge minimum (€)",
    min_value=0.0,
    max_value=1000.0,
    value=15.0,
    step=1.0
)

roi_min = st.sidebar.number_input(
    "ROI minimum (%)",
    min_value=0.0,
    max_value=1000.0,
    value=50.0,
    step=5.0
)

marque_filtre = st.sidebar.selectbox(
    "Marque",
    MARQUES
)

article_filtre = st.sidebar.selectbox(
    "Article",
    ARTICLES
)

# ============================================================
# APPLICATION DES FILTRES
# ============================================================

resultats = annonces[
    annonces["Prix"] <= budget
].copy()

resultats = resultats[
    resultats["Marge estimée"] >= marge_min
]

resultats = resultats[
    resultats["ROI estimé"] >= roi_min
]

if marque_filtre != "Toutes":

    resultats = resultats[
        resultats["Marque"]
        .astype(str)
        .str.contains(
            marque_filtre,
            case=False,
            na=False
        )
    ]

if article_filtre != "Tous":

    texte_article = (
        resultats["Article"].astype(str)
        + " "
        + resultats["Categorie"].astype(str)
    )

    resultats = resultats[
        texte_article.str.contains(
            article_filtre,
            case=False,
            na=False
        )
    ]

resultats = resultats.sort_values(
    by="Score",
    ascending=False
)


# ============================================================
# RECHERCHE VINTED
# ============================================================

st.divider()

st.subheader("🔎 Recherche Vinted")

c1, c2 = st.columns(2)

with c1:

    recherche_marque = st.selectbox(
        "Marque recherchée",
        MARQUES[1:]
    )

with c2:

    recherche_article = st.selectbox(
        "Article recherché",
        ARTICLES[1:]
    )

recherche = (
    recherche_marque
    + " "
    + recherche_article
)

url = (
    "https://www.vinted.fr/catalog?search_text="
    + urllib.parse.quote_plus(recherche)
)

st.link_button(
    "🔎 Ouvrir cette recherche sur Vinted",
    url
)

st.caption(
    "Le bouton ouvre une recherche Vinted. "
    "Il ne récupère pas automatiquement les annonces."
)


# ============================================================
# STATISTIQUES
# ============================================================

st.divider()

st.subheader("📊 Analyse")

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "🔥 Opportunités",
        len(resultats)
    )

with b:

    if len(resultats):

        st.metric(
            "💰 Marge moyenne",
            f"{resultats['Marge estimée'].mean():.0f} €"
        )

    else:

        st.metric(
            "💰 Marge moyenne",
            "—"
        )

with c:

    if len(resultats):

        st.metric(
            "📈 ROI moyen",
            f"{resultats['ROI estimé'].mean():.0f} %"
        )

    else:

        st.metric(
            "📈 ROI moyen",
            "—"
        )

with d:

    if len(resultats):

        st.metric(
            "⭐ Meilleur score",
            f"{resultats['Score'].max()}/100"
        )

    else:

        st.metric(
            "⭐ Meilleur score",
            "—"
        )


# ============================================================
# TOP AFFAIRES
# ============================================================

st.subheader("🏆 Meilleures opportunités")

if len(resultats) == 0:

    st.warning(
        "Aucune annonce ne correspond à tes critères."
    )

else:

    nombre = st.slider(
        "Nombre d'annonces",
        1,
        min(20, len(resultats)),
        min(5, len(resultats))
    )

    top = resultats.head(
        nombre
    )

    for rang, (_, annonce) in enumerate(
        top.iterrows(),
        start=1
    ):

        score = int(
            annonce["Score"]
        )

        if score >= 85:
            niveau = "🔥 EXCELLENTE"
        elif score >= 70:
            niveau = "🟢 TRÈS INTÉRESSANTE"
        elif score >= 50:
            niveau = "🟡 À ÉTUDIER"
        else:
            niveau = "🔴 FAIBLE"

        st.markdown(
            f"## #{rang} — {niveau}"
        )

        gauche, droite = st.columns(
            [3, 1]
        )

        with gauche:

            st.markdown(
                f"### {annonce['Article']}"
            )

            st.write(
                f"🏷️ Marque : **{annonce['Marque']}**"
            )

            st.write(
                f"📦 Catégorie : {annonce['Categorie']}"
            )

            st.write(
                f"📏 Taille : {annonce['Taille']}"
            )

            st.write(
                f"✨ État : {annonce['Etat']}"
            )

            if str(
                annonce["URL"]
            ).startswith("http"):

                st.link_button(
                    "🔗 Ouvrir l'annonce",
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
                f"{score}/100"
            )

        st.divider()


# ============================================================
# TABLEAU
# ============================================================

with st.expander(
    "📋 Voir le tableau complet"
):

    colonnes = [
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
        resultats[colonnes],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPORT
# ============================================================

if len(resultats) > 0:

    export = resultats.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Télécharger les résultats",
        export,
        "vinted_opportunites.csv",
        "text/csv"
    )


# ============================================================
# MODÈLE CSV
# ============================================================

with st.expander(
    "📄 Voir le format CSV attendu"
):

    exemple = pd.DataFrame({
        "Article": [
            "Half Zip"
        ],
        "Marque": [
            "Ralph Lauren"
        ],
        "Categorie": [
            "Pull"
        ],
        "Prix": [
            25
        ],
        "Etat": [
            "Très bon état"
        ],
        "Taille": [
            "M"
        ],
        "URL": [
            "https://www.vinted.fr/"
        ]
    })

    st.dataframe(
        exemple,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# AVERTISSEMENT
# ============================================================

st.divider()

st.caption(
    "⚠️ Les prix de revente sont des estimations. "
    "Ils ne garantissent pas le prix auquel un article sera vendu. "
    "Vérifie toujours l'état et l'authenticité avant un achat."
)
