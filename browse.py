#============== Modules ======================#

import cv2 
import numpy as np
import face_recognition as fr
import os
from PIL import Image

#==============================================#

#Initialisation de variables
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
unknown_image = fr.load_image_file('test/1.jpg')
unkown_image_encoding = fr.face_encodings(unknown_image)

# Comapraison
taille = len(unkown_image_encoding)
matchesIndex = []

for i in range(taille):
    result = fr.compare_faces(known_faces_encoding, unkown_image_encoding[i])
    for k in range(len(result)):
        if result[k] == True:
            matchesIndex.append(k)


for i in matchesIndex:
    print(allNames[i])









    









