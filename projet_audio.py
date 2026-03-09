import os
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
from gtts import gTTS
import tempfile
import pygame
import threading

# Initialiser pygame mixer
pygame.mixer.init()

def parler(texte, langue='fr'):
    """Faire parler Google avec une vraie voix française"""
    print(f"🗣️  Google dit : {texte}")
    
    def jouer_audio():
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            temp_filename = f.name
        
        try:
            # Générer l'audio
            tts = gTTS(text=texte, lang=langue, slow=False)
            tts.save(temp_filename)
            
            # Jouer l'audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Attendre la fin
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
            
        finally:
            # Nettoyer
            try:
                os.unlink(temp_filename)
            except:
                pass
    
    # Lancer dans un thread pour ne pas bloquer
    thread = threading.Thread(target=jouer_audio)
    thread.daemon = True
    thread.start()
    time.sleep(0.5)  # Petit délai pour laisser l'audio démarrer

def afficher_image(chemin_dossier, nom_classe, couleur):
    """Affiche une image et fait parler"""
    
    images = os.listdir(chemin_dossier)
    if not images:
        print(f"❌ Aucune image dans {chemin_dossier}")
        return
    
    img_choisie = random.choice(images)
    chemin_complet = os.path.join(chemin_dossier, img_choisie)
    
    # Lire l'image
    img = mpimg.imread(chemin_complet)
    
    # Afficher
    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    plt.title(f"{nom_classe}\n{img_choisie}", fontsize=16, color=couleur)
    plt.axis('off')
    
    # Parler
    if "SABLE" in nom_classe:
        parler("Voici une image de sable")
    else:
        parler("Voici une image d'argile")
    
    plt.show()

def menu():
    """Menu principal"""
    
    print("\n" + "="*60)
    print("🔊 PROJET SOL - AVEC VRAIE VOIX GOOGLE")
    print("="*60)
    print(f"📂 Dossier sable : {len(os.listdir('dataset/sable'))} images")
    print(f"📂 Dossier argile : {len(os.listdir('dataset/argile'))} images")
    print("="*60)
    
    # Test de voix au démarrage
    parler("Bienvenue dans le projet de classification des sols")
    
    while True:
        print("\n📋 MENU PRINCIPAL")
        print("1. 🏝️  Voir une image de SABLE (avec voix)")
        print("2. 🧱  Voir une image d'ARGILE (avec voix)")
        print("3. ⚖️  Comparer SABLE vs ARGILE")
        print("4. 🎮  JEU : Devine le sol")
        print("5. ❌  Quitter")
        
        choix = input("\n👉 Ton choix (1-5) : ")
        
        if choix == "1":
            afficher_image("dataset/sable", "🌿 SABLE", "green")
            
        elif choix == "2":
            afficher_image("dataset/argile", "🧱 ARGILE", "brown")
            
        elif choix == "3":
            parler("Je vais vous montrer la différence entre le sable et l'argile")
            
            # Image sable
            img_sable = random.choice(os.listdir("dataset/sable"))
            sable = mpimg.imread(os.path.join("dataset/sable", img_sable))
            
            # Image argile
            img_argile = random.choice(os.listdir("dataset/argile"))
            argile = mpimg.imread(os.path.join("dataset/argile", img_argile))
            
            # Affichage côte à côte
            fig, axes = plt.subplots(1, 2, figsize=(15, 7))
            
            axes[0].imshow(sable)
            axes[0].set_title("🌿 SABLE", fontsize=18, color='green')
            axes[0].axis('off')
            
            axes[1].imshow(argile)
            axes[1].set_title("🧱 ARGILE", fontsize=18, color='brown')
            axes[1].axis('off')
            
            plt.suptitle("COMPARAISON DES SOLS", fontsize=20)
            plt.show(block=False)
            
            parler("À gauche, le sable. À droite, l'argile. Vous voyez la différence de texture ?")
            input("\nAppuie sur Entrée pour continuer...")
            plt.close()
            
        elif choix == "4":
            parler("Bienvenue dans le jeu. Je vais te montrer une image, à toi de deviner !")
            
            # Mélanger les images
            images = []
            for img in os.listdir("dataset/sable")[:3]:
                images.append((os.path.join("dataset/sable", img), "sable"))
            for img in os.listdir("dataset/argile")[:3]:
                images.append((os.path.join("dataset/argile", img), "argile"))
            
            random.shuffle(images)
            
            score = 0
            for i, (chemin, vraie_classe) in enumerate(images[:3], 1):
                # Afficher l'image
                img = mpimg.imread(chemin)
                plt.figure(figsize=(10, 8))
                plt.imshow(img)
                plt.title(f"Image {i}/3", fontsize=14)
                plt.axis('off')
                plt.show(block=False)
                
                parler("Est-ce que c'est du sable ou de l'argile ?")
                
                reponse = input("\n👉 Tape 's' pour sable, 'a' pour argile : ").lower()
                plt.close()
                
                if (reponse == 's' and vraie_classe == 'sable') or (reponse == 'a' and vraie_classe == 'argile'):
                    score += 1
                    parler("Bravo ! C'est correct !")
                else:
                    parler(f"Dommage, c'était {vraie_classe}")
            
            parler(f"Jeu terminé. Ton score est de {score} sur 3")
            
        elif choix == "5":
            parler("Merci d'avoir utilisé le programme. Au revoir !")
            break
        else:
            print("❌ Choix invalide")

# Point d'entrée principal
if __name__ == "__main__":
    menu()