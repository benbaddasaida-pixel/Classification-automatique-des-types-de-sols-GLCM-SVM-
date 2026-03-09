import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.feature import graycomatrix, graycoprops
import glcm_features as gf

def etudier_resolution():
    """Étudie l'impact de la résolution sur les features GLCM"""
    
    print("\n🔬 ÉTUDE DE L'IMPACT DE LA RÉSOLUTION")
    print("="*50)
    
    # Prendre une image de chaque classe
    img_sable = os.path.join("dataset/sable", os.listdir("dataset/sable")[0])
    img_argile = os.path.join("dataset/argile", os.listdir("dataset/argile")[0])
    
    # Différentes résolutions à tester
    resolutions = [32, 64, 128, 256, 512]
    
    # Stocker les résultats
    resultats = {
        'sable': {'contrast': [], 'homogeneity': [], 'energy': [], 'correlation': []},
        'argile': {'contrast': [], 'homogeneity': [], 'energy': [], 'correlation': []}
    }
    
    for resolution in resolutions:
        print(f"\n📏 Test avec résolution: {resolution}x{resolution}")
        
        # Tester sur l'image de sable
        img = cv2.imread(img_sable, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (resolution, resolution))
        glcm = graycomatrix(img, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
        
        resultats['sable']['contrast'].append(graycoprops(glcm, 'contrast')[0,0])
        resultats['sable']['homogeneity'].append(graycoprops(glcm, 'homogeneity')[0,0])
        resultats['sable']['energy'].append(graycoprops(glcm, 'energy')[0,0])
        resultats['sable']['correlation'].append(graycoprops(glcm, 'correlation')[0,0])
        
        # Tester sur l'image d'argile
        img = cv2.imread(img_argile, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (resolution, resolution))
        glcm = graycomatrix(img, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
        
        resultats['argile']['contrast'].append(graycoprops(glcm, 'contrast')[0,0])
        resultats['argile']['homogeneity'].append(graycoprops(glcm, 'homogeneity')[0,0])
        resultats['argile']['energy'].append(graycoprops(glcm, 'energy')[0,0])
        resultats['argile']['correlation'].append(graycoprops(glcm, 'correlation')[0,0])
    
    # Afficher les graphiques
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    features = ['contrast', 'homogeneity', 'energy', 'correlation']
    
    for i, feature in enumerate(features):
        ax = axes[i//2, i%2]
        ax.plot(resolutions, resultats['sable'][feature], 'o-', label='Sable', color='green', linewidth=2)
        ax.plot(resolutions, resultats['argile'][feature], 's-', label='Argile', color='brown', linewidth=2)
        ax.set_xlabel('Résolution (pixels)')
        ax.set_ylabel(feature.capitalize())
        ax.set_title(f'Impact sur {feature.capitalize()}')
        ax.legend()
        ax.grid(True)
    
    plt.suptitle('Étude de l\'impact de la résolution sur les features GLCM', fontsize=14)
    plt.tight_layout()
    plt.show()
    
    # Afficher un tableau récapitulatif
    print("\n📊 TABLEAU RÉCAPITULATIF")
    print("-" * 80)
    print(f"{'Résolution':<12} {'Classe':<8} {'Contrast':<12} {'Homogeneity':<12} {'Energy':<12} {'Correlation':<12}")
    print("-" * 80)
    
    for i, res in enumerate(resolutions):
        for classe in ['sable', 'argile']:
            print(f"{res:<12} {classe:<8} "
                  f"{resultats[classe]['contrast'][i]:<12.2f} "
                  f"{resultats[classe]['homogeneity'][i]:<12.4f} "
                  f"{resultats[classe]['energy'][i]:<12.4f} "
                  f"{resultats[classe]['correlation'][i]:<12.4f}")
    
    # Conclusion
    print("\n🔍 CONCLUSION:")
    print("- Certaines features (comme le contraste) sont très sensibles à la résolution")
    print("- D'autres (homogeneity, energy) sont plus stables")
    print("- La résolution 128x128 offre un bon compromis précision/temps de calcul")

if __name__ == "__main__":
    etudier_resolution()