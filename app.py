#=============== Modules ======================#

import tkinter as tk
from tkinter import messagebox, Menu
import cv2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import face_recognition as fr
import os
import numpy as np

#=============================================#


# fenêtre principale : root
root = tk.Tk()

# personnalisation de la fenetre
root.title('FaceRec')
root.geometry("1280x720")
root.minsize(640, 480)
root.iconbitmap("logo.ico")

canvas = tk.Canvas(root, width=1280, height=720)
canvas.grid(columnspan=3, rowspan=9)

# logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)


# fonction permettant de charger une image et de comparer les feces dessus aux faces de la base...
def compare():
    browse_text.set("Chargement...")
    file = askopenfile(parent=root, mode='rb', title="Choisir un fichier", filetypes=[
                       ("Fichier image", "*.jpg")])
    if file:
        browse_text.set("Parcourir")
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
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: compare(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Parcourir")
browse_btn.grid(column=0, row=2)


# instructions
instructions = tk.Label(
    root, text="La reconnaissance en temps réel utilise votre webcam \n pour identifier les personnes sur les différentes \n images que vous lui montrez. \n \n Appuyez sur 'q' pour arrêter la webcam!", font="Cambria")
instructions.grid(column=1, row=1)

# fonction pour la reconnaisssance en realtime...
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




# browse button2
browse2_text = tk.StringVar()
browse2_btn = tk.Button(root, textvariable=browse2_text, command=lambda: addToBase(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse2_text.set("Parcourir")
browse2_btn.grid(column=2, row=2)


        

# function 3...
def addToBase():
    browse2_text.set("Chargement...")
    file = askopenfile(parent=root, mode='rb', title="Choisir un fichier", filetypes=[
                       ("Fichier image", "*.jpg")])
    if file:
        browse2_text.set("Parcourir")

        myEntry = tk.Entry(root, width=40)
        myEntry.grid(column=2, row=3)

        def addImage():
            res = myEntry.get()
            img = Image.open(file)
            response = messagebox.askquestion('Validation', 'Êtes-vous sûr de l\'image et du nom ?')
            if response == "yes":
                img.save(f'DataBase/{res}.jpg') 
                messagebox.showinfo('Succès', 'Ajout effectué avec succès!')
                myEntry.destroy()
                add_btn.destroy()
            
            

        add_text = tk.StringVar()
        add_btn = tk.Button(root, textvariable=add_text, command=addImage, font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
        add_text.set("Ajouter")
        add_btn.grid(column=2, row=4)


#function...
def afficheAide():
    helpMessage = f'Comparer : ......\n\nAjouter : .....\n\nWebcam : .....'
    messagebox.showinfo('Aide', helpMessage)

# Barre de menus
menu_bar = Menu(root)

# fichier
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Comparer', command=compare)
file_menu.add_command(label='Ajouter', command=addToBase)

menu_bar.add_cascade(label='Fichier', menu=file_menu)
menu_bar.add_cascade(label='Test avec Webcam', command=realTime)
menu_bar.add_cascade(label='Aide', command=afficheAide)
menu_bar.add_cascade(label='Quitter',command=root.quit)


# affichage menu
root.config(menu=menu_bar)


# display app
root.mainloop()
