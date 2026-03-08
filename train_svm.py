import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import glcm_features as gf

def load_dataset(dataset_path):
    X = []
    y = []
    classes = {'sable': 0, 'argile': 1}
    
    print("📂 Chargement des images...")
    
    for class_name, label in classes.items():
        class_path = os.path.join(dataset_path, class_name)
        if not os.path.exists(class_path):
            print(f"⚠️ Dossier introuvable: {class_path}")
            continue
            
        images = os.listdir(class_path)
        print(f"   {class_name}: {len(images)} images")
        
        for img_name in images:
            img_path = os.path.join(class_path, img_name)
            features = gf.extract_glcm_features(img_path)
            
            if features is not None:
                X.append(features)
                y.append(label)
    
    return np.array(X), np.array(y)

def train_svm(X, y):
    if len(X) == 0:
        print("❌ Aucune image chargée!")
        return None
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Division des données:")
    print(f"   Train: {len(X_train)} images")
    print(f"   Test: {len(X_test)} images")
    
    svm = SVC(kernel='linear', random_state=42)
    svm.fit(X_train, y_train)
    
    y_pred = svm.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")
    
    print("\n📋 Rapport de classification:")
    print(classification_report(y_test, y_pred, target_names=['Sable', 'Argile']))
    
    return svm

if __name__ == "__main__":
    print("🚀 Début de l'entraînement...\n")
    X, y = load_dataset("dataset")
    
    if len(X) > 0:
        print(f"\n✅ Total images chargées: {len(X)}")
        print(f"   Sable: {sum(y==0)} images")
        print(f"   Argile: {sum(y==1)} images")
        
        svm_model = train_svm(X, y)
    else:
        print("❌ Aucune image n'a pu être chargée!")