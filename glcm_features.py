import os
import numpy as np
import cv2
from skimage.feature import graycomatrix, graycoprops

def extract_glcm_features(image_path):
    # Lire l'image en niveaux de gris
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Vérifier si l'image a été chargée correctement
    if img is None:
        print(f"❌ Impossible de lire: {image_path}")
        return None
    
    # Redimensionner pour uniformiser
    img = cv2.resize(img, (128, 128))
    
    # Calculer la matrice GLCM
    glcm = graycomatrix(img, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    
    # Extraire les 4 features
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    
    return [contrast, homogeneity, energy, correlation]

if __name__ == "__main__":
    # Tester avec la première image du dossier sable
    sable_files = os.listdir("dataset/sable")
    if sable_files:
        test_image = os.path.join("dataset/sable", sable_files[0])
        print(f"Test avec: {test_image}")
        features = extract_glcm_features(test_image)
        if features:
            print("✅ Features extraites:")
            print(f"   Contrast: {features[0]:.4f}")
            print(f"   Homogeneity: {features[1]:.4f}")
            print(f"   Energy: {features[2]:.4f}")
            print(f"   Correlation: {features[3]:.4f}")
    else:
        print("❌ Aucune image trouvée dans dataset/sable/")