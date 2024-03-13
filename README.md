
# Système de Détection d'Intrusion Réseau

Ce projet utilise des techniques d'apprentissage automatique pour identifier les tentatives d'intrusion dans les réseaux informatiques. Il s'appuie sur un ensemble diversifié d'algorithmes de machine learning pour analyser les données de trafic réseau et distinguer les activités normales des tentatives d'intrusion.

Pour accéder à l'interface utilisateur du projet, veuillez visiter : [https://bdcc-ml-nids.streamlit.app/](https://bdcc-ml-nids.streamlit.app/)

## Caractéristiques Principales

- **Diversité des Algorithmes** : Le système emploie cinq algorithmes de machine learning différents, à savoir la Régression Logistique, Random Forest, Naive Bayes, KNN (K-Nearest Neighbors), et SVC (Support Vector Classification), afin d'optimiser la détection des intrusions.
- **Prétraitement des Données** : Implémentation de techniques de prétraitement pour adapter les données aux exigences spécifiques des modèles de machine learning, améliorant ainsi la précision de la détection.
- **Interface Utilisateur Intuitive** : Développement d'une interface utilisateur intuitive avec Streamlit, facilitant l'interaction avec le système à travers une manipulation aisée des fonctionnalités.
- **Traitement des Données en Temps Réel** : Capacité à traiter les données en temps réel, soit par le téléchargement de fichiers CSV, soit par la saisie manuelle des caractéristiques, pour une détection instantanée.

## Configuration de l'Environnement

Afin d'exécuter ce projet, il est nécessaire de préparer un environnement Python équipé des bibliothèques suivantes :

- pandas
- joblib
- scikit-learn
- streamlit

Ces dépendances peuvent être installées via pip en exécutant la commande suivante :

```sh
pip install pandas joblib scikit-learn streamlit
```

## Utilisation

Pour démarrer l'application, ouvrez un terminal, naviguez jusqu'au dossier du projet, et exécutez :

```sh
streamlit run app.py
```

## Structure du Projet

- `app.py` : Script principal de l'application Streamlit.
- `./joblib/` : Dossier contenant les modèles pré-entraînés au format Joblib.
- `Notebook-NIDS.ipynb` : Notebook Jupyter détaillant les étapes de développement du système.
- `Rapport-NIDS.pdf` : Rapport complet du projet, incluant l'analyse des résultats et les méthodologies utilisées.

## Contribution

Les contributions à ce projet sont vivement encouragées. Pour toute proposition d'amélioration ou de collaboration, veuillez nous contacter.

---

**Projet Machine Learning : Système de Détection d'Intrusion Réseau**

*Créé par Zaid EL MOUADDIBE & Soulaimane Cherkaoui | ENSET 2024*
