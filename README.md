# Système de Détection d'Intrusion Réseau

Ce projet utilise des techniques d'apprentissage automatique pour identifier les tentatives d'intrusion dans les réseaux informatiques. Il s'appuie sur plusieurs algorithmes de Machine Learning pour évaluer les données du trafic réseau et déterminer si elles représentent une activité normale ou une tentative d'intrusion.

## Caractéristiques Principales

- Utilisation de cinq algorithmes différents : Régression Logistique, Random Forest, Naive Bayes, KNN, et SVC.
- Prétraitement des données pour s'adapter aux exigences des modèles de Machine Learning.
- Interface utilisateur intuitive développée avec Streamlit pour une interaction facile avec le système.
- Capacité de traiter les données en temps réel via le téléchargement de fichiers CSV ou la saisie manuelle des caractéristiques.


## Configuration de l'Environnement

Pour exécuter ce projet, vous aurez besoin d'un environnement Python avec les bibliothèques suivantes :

- pandas
- joblib
- scikit-learn
- streamlit

Vous pouvez installer ces dépendances en utilisant pip :

```sh
pip install pandas joblib scikit-learn streamlit

Utilisation
Pour exécuter l'application, naviguez dans le dossier du projet et lancez :


streamlit run app.py

Structure du Projet
Structure du Projet
app.py : Script principal de l'application Streamlit.
./joblib/ : Dossier contenant les modèles pré-entraînés en format Joblib.
Notebook-NIDS.ipynb
Rapport-NIDS.pdf

Contribution
Les contributions à ce projet sont les bienvenues.

Projet Machine Learning : Système de Détection d'Intrusion Réseau Cree par Zaid EL MOUADDIBE & Soulaimane Cherkaoui| ENSET 2024