# Classification automatique des types de sols (GLCM + SVM)

Ce projet consiste à classifier automatiquement des images de sols (sable vs argile) en utilisant l’analyse de texture (GLCM) et la classification avec SVM. L’objectif est d’appliquer des techniques de machine learning à un problème agricole concret.

## 📁 Contenu
- glcm_features.py : extraction des caractéristiques GLCM
- train_svm.py : entraînement et évaluation du modèle SVM
- projet_audio.py : interface interactive avec synthèse vocale
- etude_resolution.py : étude de l’impact de la résolution
- etude_parametres.py : étude de l’impact des paramètres
- dataset/ : dossier contenant les images de sols

## Dataset

Le dataset utilisé dans ce projet est disponible sur Kaggle :

https://www.kaggle.com/datasets/jhislainematchouath/soil-types-dataset

Téléchargez le dataset puis placez-le dans le dossier suivant :

dataset/
 ├── train/
 ├── test/
 ├── sable/
 └── argile/

## Auteur
Saida Benbadda – Projet Intelligence Artificielle
