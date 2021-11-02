#============== Modules ======================#

import cv2 
import numpy as np
import face_recognition as fr
import os

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






    









