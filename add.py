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
st.caption("Analyse les opportunités d'achat-revente de vêtements.")

# ============================================================
# DONNÉES DE BASE
# ============================================================

BRANDS_DEFAULT = [
    "Ralph Lauren",
    "Nike",
    "Adidas",
    "Lacoste",
    "Carhartt",
    "The North Face",
    "Polo Ralph Lauren",
    "Tommy Hilfiger",
    "Levi's",
    "New Balance",
    "Asics",
    "Patagonia",
    "Stone Island",
    "Fred Perry",
]

KEYWORDS_DEFAULT = [
    "zip",
    "half zip",
    "quarter zip",
    "pull",
    "sweat",
    "veste",
    "polo",
    "pantalon",
    "jogging",
    "hoodie",
    "fleece",
]

SUSPICIOUS_WORDS = [
    "réplique",
    "replica",
    "fake",
    "faux",
    "contrefaçon",
    "inspiré",
    "inspired",
    "1:1",
    "aaa",
    "copie",
]

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Tes critères")

budget = st.sidebar.number_input(
    "Prix d'achat maximum (€)",
    min_value=1.0,
    max_value=1000.0,
    value=40.0,
    step=1.0
)

marge_min = st.sidebar.number_input(
    "Marge minimum (€)",
    min_value=0.0,
    max_value=1000.0,
    value=20.0,
    step=1.0
)

roi_min = st.sidebar.number_input(
    "ROI minimum (%)",
    min_value=0.0,
    max_value=1000.0,
    value=50.0,
    step=5.0
)

marques_input = st.sidebar.text_area(
    "Marques recherchées",
    ", ".join(BRANDS_DEFAULT)
)

mots_cles_input = st.sidebar.text_area(
    "Articles recherchés",
    ", ".join(KEYWORDS_DEFAULT)
)

etats = st.sidebar.multiselect(
    "États acceptés",
    [
        "Neuf avec étiquette",
        "Neuf sans étiquette",
        "Très bon état",
        "Bon état",
        "Satisfaisant"
    ],
    default=[
        "Neuf avec étiquette",
        "Neuf sans étiquette",
        "Très bon état",
        "Bon état"
    ]
)

# ============================================================
# LISTES
# ============================================================

marques = [
    x.strip()
    for x in marques_input.split(",")
    if x.strip()
]

mots_cles = [
    x.strip()
    for x in mots_cles_input.split(",")
    if x.strip()
]

# ============================================================
# OUTIL : URL DE RECHERCHE VINTED
# ============================================================

def vinted_search_url(query):
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.vinted.fr/catalog?search_text={encoded}"


# ============================================================
# GÉNÉRATION DES RECHERCHES
# ============================================================

st.subheader("🔎 Recherches Vinted")

if marques and mots_cles:

    recherches = []

    for marque in marques:
        for mot in mots_cles:
            recherches.append({
                "Marque": marque,
                "Recherche": f"{marque} {mot}",
                "Lien": vinted_search_url(f"{marque} {mot}")
            })

    recherches_df = pd.DataFrame(recherches)

    # Limite d'affichage pour garder l'interface propre
    recherches_affichage = recherches_df.head(50)

    for _, recherche in recherches_affichage.iterrows():

        st.markdown(
            f"**{recherche['Marque']} — {recherche['Recherche']}**"
        )

        st.link_button(
            "🔎 Ouvrir la recherche",
            recherche["Lien"]
        )

else:
    st.warning("Ajoute au moins une marque et un mot-clé.")

# ============================================================
# IMPORT DES ANNONCES
# ============================================================

st.divider()

st.subheader("📥 Analyser des annonces")

st.write(
    "Tu peux importer un fichier CSV contenant les annonces "
    "que tu veux analyser."
)

uploaded_file = st.file_uploader(
    "Importer un CSV",
    type=["csv"]
)

# ============================================================
# EXEMPLE DE FORMAT
# ============================================================

with st.expander("📋 Format CSV attendu"):

    exemple = pd.DataFrame([
        {
            "Article": "Ralph Lauren Half Zip bleu marine",
            "Marque": "Ralph Lauren",
            "Categorie": "Pull",
            "Prix": 25,
            "Revente": 60,
            "Etat": "Très bon état",
            "Taille": "M",
            "URL": "https://www.vinted.fr/"
        }
    ])

    st.dataframe(
        exemple,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# DONNÉES
# ============================================================

if uploaded_file is not None:

    try:
        annonces = pd.read_csv(uploaded_file)

    except Exception as e:
        st.error(f"Impossible de lire le fichier : {e}")
        st.stop()

else:

    # Données de démonstration
    annonces = pd.DataFrame([
        {
            "Article": "Ralph Lauren Half Zip bleu marine",
            "Marque": "Ralph Lauren",
            "Categorie": "Pull",
            "Prix": 25,
            "Revente": 60,
            "Etat": "Très bon état",
            "Taille": "M",
            "URL": "https://www.vinted.fr/"
        },
        {
            "Article": "Ralph Lauren Quarter Zip gris",
            "Marque": "Ralph Lauren",
            "Categorie": "Pull",
            "Prix": 30,
            "Revente": 65,
            "Etat": "Très bon état",
            "Taille": "L",
            "URL": "https://www.vinted.fr/"
        },
        {
            "Article": "Nike Tech Fleece",
            "Marque": "Nike",
            "Categorie": "Ensemble",
            "Prix": 45,
            "Revente": 70,
            "Etat": "Bon état",
            "Taille": "M",
            "URL": "https://www.vinted.fr/"
        },
        {
            "Article": "Lacoste Pull Vintage",
            "Marque": "Lacoste",
            "Categorie": "Pull",
            "Prix": 18,
            "Revente": 45,
            "Etat": "Très bon état",
            "Taille": "M",
            "URL": "https://www.vinted.fr/"
        },
        {
            "Article": "Carhartt Sweat",
            "Marque": "Carhartt",
            "Categorie": "Sweat",
            "Prix": 28,
            "Revente": 60,
            "Etat": "Très bon état",
            "Taille": "L",
            "URL": "https://www.vinted.fr/"
        }
    ])

# ============================================================
# VÉRIFICATION DES COLONNES
# ============================================================

colonnes_obligatoires = [
    "Article",
    "Marque",
    "Prix",
    "Revente",
    "Etat"
]

manquantes = [
    colonne
    for colonne in colonnes_obligatoires
    if colonne not in annonces.columns
]

if manquantes:

    st.error(
        "Colonnes manquantes dans ton CSV : "
        + ", ".join(manquantes)
    )

    st.stop()

# Colonnes optionnelles
if "Categorie" not in annonces.columns:
    annonces["Categorie"] = ""

if "Taille" not in annonces.columns:
    annonces["Taille"] = ""

if "URL" not in annonces.columns:
    annonces["URL"] = ""

# ============================================================
# NETTOYAGE DES DONNÉES
# ============================================================

annonces["Prix"] = pd.to_numeric(
    annonces["Prix"],
    errors="coerce"
)

annonces["Revente"] = pd.to_numeric(
    annonces["Revente"],
    errors="coerce"
)

annonces = annonces.dropna(
    subset=["Prix", "Revente"]
)

# ============================================================
# FILTRE PRIX
# ============================================================

annonces = annonces[
    annonces["Prix"] <= budget
].copy()

# ============================================================
# FILTRE MARQUES
# ============================================================

if marques:

    marques_lower = [
        marque.lower()
        for marque in marques
    ]

    annonces = annonces[
        annonces["Marque"]
        .fillna("")
        .astype(str)
        .str.lower()
        .apply(
            lambda valeur:
            any(
                marque in valeur
                for marque in marques_lower
            )
        )
    ].copy()

# ============================================================
# FILTRE ÉTAT
# ============================================================

if etats:

    annonces = annonces[
        annonces["Etat"]
        .fillna("")
        .isin(etats)
    ].copy()

# ============================================================
# DÉTECTION MOTS-CLÉS
# ============================================================

def contient_mot_cle(article):

    texte = str(article).lower()

    return any(
        mot.lower() in texte
        for mot in mots_cles
    )


annonces["Mot-clé trouvé"] = annonces[
    "Article"
].apply(contient_mot_cle)

# ============================================================
# CALCUL MARGE
# ============================================================

annonces["Marge"] = (
    annonces["Revente"]
    - annonces["Prix"]
)

# ============================================================
# ROI
# ============================================================

annonces["ROI"] = (
    annonces["Marge"]
    / annonces["Prix"]
    * 100
)

# ============================================================
# DÉTECTION D'ANNONCE DOUTEUSE
# ============================================================

def detecter_doute(row):

    texte = (
        str(row.get("Article", ""))
        + " "
        + str(row.get("Marque", ""))
        + " "
        + str(row.get("Etat", ""))
    ).lower()

    for mot in SUSPICIOUS_WORDS:

        if mot.lower() in texte:
            return True

    return False


annonces["À vérifier"] = annonces.apply(
    detecter_doute,
    axis=1
)

# ============================================================
# SCORE
# ============================================================

def calcul_score(row):

    score = 0

    marge = float(row["Marge"])
    roi = float(row["ROI"])

    # -------------------------
    # MARGE
    # -------------------------

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

    # -------------------------
    # ROI
    # -------------------------

    if roi >= 150:
        score += 30

    elif roi >= 100:
        score += 26

    elif roi >= 75:
        score += 21

    elif roi >= 50:
        score += 16

    elif roi >= 30:
        score += 10

    # -------------------------
    # ÉTAT
    # -------------------------

    etat = str(row["Etat"])

    if etat == "Neuf avec étiquette":
        score += 20

    elif etat == "Neuf sans étiquette":
        score += 18

    elif etat == "Très bon état":
        score += 15

    elif etat == "Bon état":
        score += 8

    # -------------------------
    # MOT-CLÉ
    # -------------------------

    if row["Mot-clé trouvé"]:
        score += 5

    # -------------------------
    # DOUTEUX
    # -------------------------

    if row["À vérifier"]:
        score -= 30

    return max(
        0,
        min(score, 100)
    )


annonces["Score"] = annonces.apply(
    calcul_score,
    axis=1
)

# ============================================================
# FILTRES FINAUX
# ============================================================

resultats = annonces[
    (annonces["Marge"] >= marge_min)
    &
    (annonces["ROI"] >= roi_min)
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

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Opportunités",
        len(resultats)
    )

with col2:

    if len(resultats):
        st.metric(
            "Marge moyenne",
            f"{resultats['Marge'].mean():.0f} €"
        )
    else:
        st.metric(
            "Marge moyenne",
            "—"
        )

with col3:

    if len(resultats):
        st.metric(
            "ROI moyen",
            f"{resultats['ROI'].mean():.0f} %"
        )
    else:
        st.metric(
            "ROI moyen",
            "—"
        )

with col4:

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
# AFFICHAGE
# ============================================================

st.subheader("🔥 Meilleures opportunités")

if len(resultats) == 0:

    st.warning(
        "Aucune annonce ne correspond à tes critères."
    )

else:

    for _, article in resultats.iterrows():

        score = article["Score"]

        if score >= 85:
            niveau = "🔥 EXCELLENTE AFFAIRE"

        elif score >= 70:
            niveau = "🟢 BONNE AFFAIRE"

        elif score >= 50:
            niveau = "🟡 À ÉTUDIER"

        else:
            niveau = "🔴 PEU INTÉRESSANTE"

        st.markdown(
            f"## {niveau}"
        )

        col1, col2 = st.columns(
            [3, 1]
        )

        with col1:

            st.markdown(
                f"### {article['Article']}"
            )

            st.write(
                f"🏷️ **Marque :** {article['Marque']}"
            )

            st.write(
                f"📦 **Catégorie :** {article['Categorie']}"
            )

            st.write(
                f"📏 **Taille :** {article['Taille']}"
            )

            st.write(
                f"✨ **État :** {article['Etat']}"
            )

            if article["URL"]:

                st.link_button(
                    "🔗 Voir l'annonce",
                    article["URL"]
                )

        with col2:

            st.metric(
                "Prix achat",
                f"{article['Prix']:.2f} €"
            )

            st.metric(
                "Revente estimée",
                f"{article['Revente']:.2f} €"
            )

            st.metric(
                "Marge",
                f"{article['Marge']:.2f} €"
            )

            st.metric(
                "ROI",
                f"{article['ROI']:.0f} %"
            )

            st.metric(
                "Score",
                f"{article['Score']}/100"
            )

        if article["À vérifier"]:

            st.warning(
                "⚠️ Cette annonce contient un élément "
                "qui mérite une vérification supplémentaire "
                "avant achat."
            )

        st.divider()

# ============================================================
# TABLEAU COMPLET
# ============================================================

with st.expander("📋 Voir toutes les données"):

    colonnes = [
        "Article",
        "Marque",
        "Categorie",
        "Prix",
        "Revente",
        "Marge",
        "ROI",
        "Etat",
        "Taille",
        "Score",
        "À vérifier"
    ]

    st.dataframe(
        resultats[colonnes],
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# EXPORT CSV
# ============================================================

if len(resultats):

    csv = resultats.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Télécharger les opportunités",
        data=csv,
        file_name="vinted_opportunites.csv",
        mime="text/csv"
    )

# ============================================================
# INFOS
# ============================================================

st.divider()

st.caption(
    "⚠️ Les prix de revente sont des estimations. "
    "Vérifie toujours l'état réel, l'authenticité, "
    "la demande et les coûts éventuels avant tout achat."
)

st.caption(
    "Vinted Finder V2 — outil d'analyse et de recherche."
)
