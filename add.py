#============== Modules ======================#


import os
from PIL import Image

#==============================================#

#Initialisation de variables
chemin = 'DataBase'
images = []
allNames = []

# Liste de toutes les images de la BD
lstImages = os.listdir(chemin)

img = Image.open('test/1.jpg')

img.save('DataBase/Nom Prenom.jpg')











    









