import streamlit as st
import pandas as pd
from joblib import load

# Fonction pour charger les modèles
def charger_modeles():
    modeles = {
        'Régression Logistique': load('./joblib/Logistic_Regression_model.joblib'),
        'Random Forest': load('./joblib/Random_Forest_model.joblib'),
        'Naive Bayes': load('./joblib/Naive_Bayes_model.joblib'),
        'KNN': load('./joblib/KNN_model.joblib'),
        'SVC': load('./joblib/SVC_model.joblib')
    }
    return modeles

# Fonction pour prétraiter les données d'entrée
def pretraiter_donnees_entree(input_df):
    input_df['protocol_type'] = input_df['protocol_type'].map({'tcp': 0, 'udp': 1, 'icmp': 2}).fillna(0)
    input_df['flag'] = input_df['flag'].map({'SF': 0, 'S0': 1, 'REJ': 2, 'RSTR': 3, 'RSTO': 4}).fillna(0)
    
    # Liste des colonnes nécessaires
    colonnes_necessaires = [
        'same_srv_rate', 'logged_in', 'dst_host_serror_rate',
        'dst_host_same_srv_rate', 'dst_host_srv_count',
        'dst_host_srv_serror_rate', 'flag', 'srv_serror_rate', 
        'protocol_type', 'last_flag', 'serror_rate'
    ]
    
    # Vérifier si toutes les colonnes nécessaires sont présentes
    colonnes_manquantes = [col for col in colonnes_necessaires if col not in input_df.columns]
    
    if colonnes_manquantes:
        for col in colonnes_manquantes:
            input_df[col] = 0

    return input_df[colonnes_necessaires]

# Fonction de prédiction qui choisit le modèle avec la probabilité la plus élevée
def predire_avec_meilleur_modele(modeles, input_df):
    meilleur_score = 0
    meilleures_predictions = None
    meilleures_proba_predictions = None
    modele_choisi = None
    for nom, modele in modeles.items():
        if hasattr(modele, "predict_proba"):
            proba_predictions = modele.predict_proba(input_df)[:, 1]
            max_proba = max(proba_predictions)
            if max_proba > meilleur_score:
                meilleur_score = max_proba
                predictions = modele.predict(input_df)
                meilleures_predictions = predictions
                meilleures_proba_predictions = proba_predictions
                modele_choisi = nom
    return meilleures_predictions, meilleures_proba_predictions, modele_choisi

# Configuration de l'interface utilisateur Streamlit
def configurer_interface_utilisateur():
    st.title('Système de Détection d\'Intrusion Réseau')
    st.markdown("""
    Ce projet utilise des techniques d'apprentissage automatique pour identifier les tentatives d'intrusion dans les réseaux informatiques. Il s'appuie sur cinq algorithmes différents : Régression Logistique, Random Forest, Naive Bayes, KNN et SVC. Le système évalue les données fournies et prédit si elles représentent une activité normale ou une attaque, en se basant sur le modèle qui donne la probabilité la plus élevée.
    """)

def saisie_manuelle_caracteristiques():
    with st.form(key='feature_form'):
        st.subheader('Veuillez entrer les valeurs pour les caractéristiques suivantes :')
        # Les entrées pour les caractéristiques ici sont basées sur les 11 caractéristiques attendues par les modèles
        valeurs_caracteristiques = {
			
			"logged_in": int(st.radio("Connecté ?", ('Oui', 'Non')) == 'Oui'),
            "dst_host_srv_count": st.number_input("Nombre de connexions au service de l'hôte", min_value=0, max_value=100, value=50),
            "same_srv_rate": st.slider("Taux de connexions au même service", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "dst_host_same_srv_rate": st.slider("Taux de connexion au même hôte", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "srv_serror_rate": st.slider("Taux d'erreur de service", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "dst_host_same_src_port_rate": st.slider("Taux de connexions au même port source de l'hôte", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "dst_host_serror_rate": st.slider("Taux d'erreur de l'hôte de destination", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "last_flag": st.number_input("Dernier drapeau de la connexion", min_value=0, max_value=100, value=50),
            "protocol_type": st.selectbox("Type de protocole", options=['tcp', 'udp', 'icmp']),
            "flag": st.selectbox("État de la connexion", options=['SF', 'S0', 'REJ', 'RSTR', 'RSTO']),
            "serror_rate": st.slider("Taux d'erreurs de connexion", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        }
        bouton_predire = st.form_submit_button('Prédire')
        return pd.DataFrame([valeurs_caracteristiques]) if bouton_predire else None

# Interface utilisateur pour le téléchargement de fichier CSV
def upload_csv_interface():
    uploaded_file = st.file_uploader("Ou téléchargez un fichier CSV", type=["csv"])
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

def main():
    modeles = charger_modeles()
    configurer_interface_utilisateur()
    option = st.radio("Méthode de saisie des données:", ['Remplir manuellement les caractéristiques', 'Télécharger un fichier CSV'])

    input_df = None
    if option == 'Télécharger un fichier CSV':
        input_df = upload_csv_interface()
    elif option == 'Remplir manuellement les caractéristiques':
        input_df = saisie_manuelle_caracteristiques()

    if input_df is not None:
        input_df = pretraiter_donnees_entree(input_df)
        predictions, proba_predictions, modele_choisi = predire_avec_meilleur_modele(modeles, input_df)
        # Déterminer le résultat de la prédiction et sa couleur en fonction du résultat
        resultat_prediction = 'une Attaque' if predictions[0] == 1 else 'Normal'
        couleur_resultat = 'red' if predictions[0] == 1 else 'green'

        # Construire le message HTML avec le style souhaité
        message_html = f"""
            <h3 style='color:{couleur_resultat};'>Le système prédit que le trafic est <strong>{resultat_prediction}</strong>.</h3>
        """
        st.markdown(message_html, unsafe_allow_html=True)
        
if __name__ == '__main__':
    main()