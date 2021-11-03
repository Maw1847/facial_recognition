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


# add form
'''l = tk.Label(root, text = "Nom et prénom")
e = tk.Entry(root)
b = tk.Button(root ,text="Submit")
l.grid(column=2, row=3)
e.grid(column=2)
b.grid(column=2)'''











    









