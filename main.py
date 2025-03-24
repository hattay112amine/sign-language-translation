import cv2
import mediapipe as mp
from tkinter import Entry, OptionMenu, StringVar, Tk, Button, Label,Toplevel
from PIL import Image, ImageTk
import numpy as np

# Initialiser MediaPipe pour la détection des mains
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Fonction pour capturer l'image
def capture_image():
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de capturer l'image.")
        return
    
    # Convertir l'image en RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Détection des mains
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        # Trouver les coordonnées de la boîte englobante de la main
        for hand_landmarks in results.multi_hand_landmarks:
            # Extraire les coordonnées x et y des points clés de la main
            x_coords = [landmark.x * frame.shape[1] for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y * frame.shape[0] for landmark in hand_landmarks.landmark]
            
            # Calculer les coordonnées de la boîte englobante
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            
            # Ajouter une marge autour de la main (optionnel)
            margin = 20  # Marge en pixels
            x_min = max(0, x_min - margin)
            x_max = min(frame.shape[1], x_max + margin)
            y_min = max(0, y_min - margin)
            y_max = min(frame.shape[0], y_max + margin)
            
            # Dessiner un cadre autour de la main dans l'affichage en direct
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            
            # Recadrer l'image autour de la main
            hand_cropped = frame[y_min:y_max, x_min:x_max]
            
            # Convertir l'image recadrée en format compatible avec Tkinter
            img = Image.fromarray(cv2.cvtColor(hand_cropped, cv2.COLOR_BGR2RGB))
            img_tk = ImageTk.PhotoImage(image=img)
            
            # Afficher l'image recadrée dans une nouvelle fenêtre
            new_window = Toplevel()
            new_window.title("Main Capturée")
            # Garder une référence à l'image dans la nouvelle fenêtre
            new_window.img_tk = img_tk  # <-- Ajoutez cette ligne
            label_image = Label(new_window, image=img_tk)
            # Afficher l'image dans un label avec une taille d'affichage spécifique
            label_image = Label(new_window, image=img_tk, width=400, height=400)  # Taille d'affichage
            label_image.pack()
             # Ajouter un menu déroulant pour sélectionner la langue
            langues = ["Français", "Anglais", "Arabe"]
            langue_var = StringVar(new_window)
            langue_var.set(langues[0])  # Langue par défaut

            drop_langue = OptionMenu(new_window, langue_var, *langues)
            drop_langue.pack()

            # Fonction pour afficher le champ de saisie lorsque la langue est sélectionnée
            def afficher_champ_saisi(*args):
                if langue_var.get() != "":
                    champ_saisi.pack()
                    bouton_enregistrer.pack()

            # Associer la fonction à la sélection de la langue
            langue_var.trace("w", afficher_champ_saisi)

            # Champ de saisie pour l'étiquette
            champ_saisi =Entry(new_window)
            champ_saisi.pack_forget()  # Caché par défaut

            # Bouton pour enregistrer l'image avec l'étiquette
            def enregistrer_image():
                langue = langue_var.get()
                texte = champ_saisi.get()
                print(f"Langue : {langue}, Texte : {texte}")
                # Ici, vous pouvez ajouter le code pour enregistrer l'image avec l'étiquette
                # Par exemple, sauvegarder l'image dans un dossier avec un nom de fichier basé sur l'étiquette
                # ou envoyer les données à une base de données.

            bouton_enregistrer = Button(new_window, text="Enregistrer", command=enregistrer_image)
            bouton_enregistrer.pack_forget()  # Caché par défaut
    else:
        print("Aucune main détectée.")

# Fonction pour mettre à jour l'affichage de la caméra
def update_camera():
    ret, frame = cap.read()
    if ret:
        # Convertir l'image en RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Détection des mains
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            # Dessiner les points clés des mains
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                  # Extraire les coordonnées x et y des points clés de la main
            x_coords = [landmark.x * frame.shape[1] for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y * frame.shape[0] for landmark in hand_landmarks.landmark]
            
            # Calculer les coordonnées de la boîte englobante
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            
            # Ajouter une marge autour de la main (optionnel)
            margin = 20  # Marge en pixels
            x_min = max(0, x_min - margin)
            x_max = min(frame.shape[1], x_max + margin)
            y_min = max(0, y_min - margin)
            y_max = min(frame.shape[0], y_max + margin)
            
            # Dessiner un cadre autour de la main dans l'affichage en direct
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        
        # Convertir l'image en format compatible avec Tkinter
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        label_camera.config(image=img_tk)
        label_camera.image = img_tk  # Garder une référence pour éviter la suppression par le garbage collector
    
    # Mettre à jour l'affichage toutes les 10 ms
    label_camera.after(10, update_camera)

# Initialiser Tkinter
root = Tk()
root.title("Capture de Gestes de la Main")

# Bouton pour capturer l'image
button_capture = Button(root, text="Capturer", command=capture_image)
button_capture.pack()

# Label pour afficher la caméra
label_camera = Label(root)
label_camera.pack()

# Capturer la vidéo depuis la caméra
cap = cv2.VideoCapture(0)

# Démarrer la mise à jour de l'affichage de la caméra
update_camera()

# Démarrer l'interface Tkinter
root.mainloop()

# Libérer la caméra à la fermeture
cap.release()