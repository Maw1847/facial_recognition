#=============== Modules ======================#

import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import face_recognition as fr
import os
import numpy as np

#=============================================#


# fenêtre principale : root
root = tk.Tk()

canvas = tk.Canvas(root, width=1280, height=720)
canvas.grid(columnspan=3, rowspan=9)

# logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)


# function 1...
def open_file():
    browse_text.set("Chargement...")
    file = askopenfile(parent=root, mode='rb', title="Choisir un fichier", filetypes=[
                       ("Fichier image", "*.jpg")])
    if file:
        chemin = 'DataBase'
        images = []
        allNames = []

        # Liste de toutes les images de la BD
        lstImages = os.listdir(chemin)

        # Chargement des images, remplissage des listes des images et des personnes
        for element in lstImages:
            currentImage = fr.load_image_file(f'{chemin}/{element}')
            images.append(currentImage)
            singleName = os.path.splitext(element)[0]
            allNames.append(singleName)


        # Fonction permettant d'encoder toutes les images avec face_recognition
        def makeEncodings(imgs):
            encodeList = []
            for img in imgs:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = fr.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        # Liste des faces connues encodées
        known_faces_encoding = makeEncodings(images)

        # Traitement de l'image inconnue
        unknown_image = fr.load_image_file(file)
        unkown_image_encoding = fr.face_encodings(unknown_image)
        
        # Comparaison
        taille = len(unkown_image_encoding)
        matchesIndex = []
        results = ''

        for i in range(taille):
            result = fr.compare_faces(known_faces_encoding, unkown_image_encoding[i])
            for k in range(len(result)):
                if result[k] == True:
                    matchesIndex.append(k)


        for i in matchesIndex:
            results += allNames[i] + "\n" 

        # Affichage du résultat
        text_box = tk.Text(root, height=10, width=50, padx=15, pady=15, font="ALGERIAN")
        text_box.insert(1.0, f'Cette image contient : \n {results}')
        text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=0, row=3)

        browse_text.set("Parcourir")



# instructions
instructions = tk.Label(
    root, text="Choisissez une image et comparer là à notre \n base de données pour tenter d'identifier \n la(les) personne(s) présente(s) dessus", font="Cambria")
instructions.grid(column=0, row=1)


# browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Parcourir")
browse_btn.grid(column=0, row=2)


# instructions
instructions = tk.Label(
    root, text="La reconnaissance en temps réel utilise votre webcam \n pour identifier les personnes sur les différentes \n images que vous lui montrez. \n \n Appuyez sur 'q' pour arrêter la webcam!", font="Cambria")
instructions.grid(column=1, row=1)

# function 2...
def realTime():
    chemin = 'DataBase'
    images = []
    allNames = []

    # Liste de toutes les images de la BD
    lstImages = os.listdir(chemin)

    # Chargement des images, remplissage des listes des images et des personnes
    for element in lstImages:
        currentImage = fr.load_image_file(f'{chemin}/{element}')
        images.append(currentImage)
        singleName = os.path.splitext(element)[0]
        allNames.append(singleName)


    # Fonction permettant d'encoder toutes les images avec face_recognition
    def makeEncodings(imgs):
        encodeList = []
        for img in imgs:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    # Liste des faces connues encodées
    known_faces_encoding = makeEncodings(images)

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        # imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        currentLocations = fr.face_locations(imgS)
        currentEncode = fr.face_encodings(imgS, currentLocations)

        for encodeFace, faceLoc in zip(currentEncode, currentLocations):
            matches = fr.compare_faces(known_faces_encoding, encodeFace)
            nom = 'Inconnu'
            distance = fr.face_distance(known_faces_encoding, encodeFace)
            matchIndex = np.argmin(distance)

            if matches[matchIndex]:
                nom = allNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(img, (x1, y2 - 30), (x2, y2), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, nom, (x1+6, y1-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# live button
live_text = tk.StringVar()
live_btn = tk.Button(root, textvariable=live_text, command=lambda: realTime(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
live_text.set("Temps réel")
live_btn.grid(column=1, row=2)


# instructions
instructions = tk.Label(
    root, text="Ajouter des images de votre choix à notre \n base de données pour pouvoir mieux \n exploiter l'application", font="Cambria")
instructions.grid(column=2, row=1)

def addImage():
    top = tk.Toplevel()
    top.title('Formulaire d\'ajout')
    nomComplet = tk.Entry()
    btn = tk.Button(text='Valider', command=())


# add form
l = tk.Label(root, text = "Nom et prénom")
e = tk.Entry(root)
b = tk.Button(root ,text="Submit")
l.grid(column=2, row=2)
e.grid(column=2, row=3)
b.grid(column=2, row=4)


# add button
add_text = tk.StringVar()
add_btn = tk.Button(root, textvariable=add_text, command=lambda: addImage(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
add_text.set("Ajouter")
add_btn.grid(column=2, row=5)

root.mainloop()
