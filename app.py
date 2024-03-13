import streamlit as st
import numpy as np
from joblib import load
import pandas as pd

# 1. Chargement des modèles et préprocesseurs
models = {
    'SVC': load('./joblib/SVC_model.joblib'),
    'Random Forest': load('./joblib/Random_Forest_model.joblib'),
    'Logistic Regression': load('./joblib/Logistic_Regression_model.joblib'),
    'KNN': load('./joblib/KNN_model.joblib')
}
scaler = load('./joblib/scaler.joblib')
label_encoders = load('./joblib/label_encoders.joblib')

# Setup title and introduction
st.title('Système de Détection d’Intrusion Réseau')
st.markdown("""
Bienvenue sur notre système de détecter les intrusions réseau utilisant le machine learning. Sélectionnez le modèle de prédiction, fournissez les données via un formulaire intuitif ou téléchargez un fichier CSV pour une analyse rapide.
""")

# Model selection
model_choice = st.radio("Sélectionnez le modèle pour la prédiction:", list(models.keys()))

# Choose between CSV upload and manual input
option = st.radio("Méthode d'entrée des données:", ('Remplir manuellement les caractéristiques', 'Télécharger un fichier CSV'))

# Display CSV format instructions if CSV option is selected
if option == 'Télécharger un fichier CSV':
    st.markdown("""
    **Instructions pour le fichier CSV:**
    - Le fichier doit contenir les colonnes pour les caractéristiques suivantes, dans l'ordre spécifié.
    - Les noms des colonnes doivent correspondre exactement aux noms des caractéristiques.
    - Les données doivent être prétraitées conformément aux exigences du modèle.
    """)
    csv_file = st.file_uploader("Choisissez un fichier CSV", type=['csv'])
    if csv_file is not None:
        input_df = pd.read_csv(csv_file)

# Manual feature input setup
if option == 'Remplir manuellement les caractéristiques':
    with st.form(key='feature_form'):
        st.subheader('Veuillez entrer les valeurs pour les caractéristiques suivantes:')

        # Define feature inputs with descriptions and appropriate widgets
        feature_values = {
            "same_srv_rate": st.slider("Taux de connexions au même service", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "logged_in": st.radio("Est connecté ?", ('Oui', 'Non'), format_func=lambda x: '1' if x == 'Oui' else '0'),
            "srv_serror_rate": st.slider("Taux d'erreurs de service", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "flag": st.selectbox("État de la connexion", options=label_encoders['flag'].classes_),
            "dst_host_same_srv_rate": st.slider("Taux de connexion au même hôte de destination", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "dst_host_srv_count": st.number_input("Nombre de connexions au service de l'hôte de destination", min_value=0, max_value=100, value=50),
            "serror_rate": st.slider("Taux d'erreurs de connexion", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "protocol_type": st.selectbox("Type de protocole", options=label_encoders['protocol_type'].classes_),
            "last_flag": st.number_input("Dernier indicateur de la connexion", min_value=0, max_value=100, value=50),
            "dst_host_serror_rate": st.slider("Taux d'erreurs de l'hôte de destination", min_value=0.0, max_value=1.0, value=0.5, step=0.01),
            "dst_host_same_src_port_rate": st.slider("Taux de connexions au même port source de l'hôte", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        }
        submit_button = st.form_submit_button(label='Prédire')

# Initialize a full feature vector with neutral values
full_feature_vector = np.zeros(39)

# Data Preprocessing and Prediction
def preprocess_and_predict(input_df, model_choice):
    # Encode categorical features
    for col, encoder in label_encoders.items():
        if col in input_df:
            input_df[col] = encoder.transform(input_df[col])
    
    # Scale features
    scaled_features = scaler.transform(input_df)
    
    # Make prediction using the selected model
    model = models[model_choice]
    predictions = model.predict(scaled_features)
    prediction_probabilities = model.predict_proba(scaled_features)[:, 1]
    
    return predictions, prediction_probabilities

# Display prediction results
if st.button('Prédire'):
    if 'input_df' not in locals():  # Build input_df from feature_values if not from CSV
        input_df = pd.DataFrame([feature_values])
    predictions, prediction_probabilities = preprocess_and_predict(input_df, model_choice)
    
    # Display the prediction result
    result = "Normal" if predictions[0] == 0 else "Attaque"
    st.write(f"Le modèle **{model_choice}** prédit que le trafic est **{result}** avec une probabilité de **{prediction_probabilities[0] * 100:.2f}%**.")