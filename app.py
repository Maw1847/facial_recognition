import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import face_recognition


root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=400)
canvas.grid(columnspan=3, rowspan=3)

# logo
logo = Image.open('images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)


# instructions
instructions = tk.Label(
    root, text="Choisissez une image et comparer là à notre base pour tenter d'identifier le(s) personnes présente(s) dessus", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)


# function...
def open_file():
    browse_text.set("chargement...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[
                       ("Fichier iamge", "*.jpg")])
    if file:
        ronaldo_image = face_recognition.load_image_file('total/Ronaldo.jpg')
        ronaldo_image_encoding = face_recognition.face_encodings(ronaldo_image)[
            0]

        messi_image = face_recognition.load_image_file('total/Messi.jpg')
        messi_image_encoding = face_recognition.face_encodings(messi_image)[0]

        mbappe_image = face_recognition.load_image_file('total/Mbappe.jpg')
        mbappe_image_encoding = face_recognition.face_encodings(mbappe_image)[
            0]

        unknown_image = face_recognition.load_image_file(file)
        unkown_image_encoding = face_recognition.face_encodings(unknown_image)[
            0]

        knownfaces = [
            ronaldo_image_encoding,
            messi_image_encoding,
            mbappe_image_encoding
        ]

        results = face_recognition.compare_faces(
            knownfaces, unkown_image_encoding)
        results = str(results)

        text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
        text_box.insert(1.0, results)
        text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=1, row=3)

        browse_text.set("Parcourir")


# browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: open_file(
), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Parcourir")
browse_btn.grid(column=1, row=2)

canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3)

root.mainloop()
