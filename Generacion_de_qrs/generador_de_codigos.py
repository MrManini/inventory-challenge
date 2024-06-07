import tkinter
import customtkinter as ctk
import segno
from PIL import Image, ImageTk

def generar_qr():
    informacion = entrada_texto.get()
    if informacion:
        qrcode = segno.make_qr(informacion)
        qrcode.save("imagen_generada.png", scale=8)
        label_resultado.configure(text="El código QR se ha generado correctamente.")

        # Mostrar la imagen del código QR
        qr_image = Image.open("imagen_generada.png")
        qr_photo = ctk.CTkImage(light_image=qr_image, size=(200, 200))
        label_qr.configure(image=qr_photo, text="")

# Aqui se hace la creacion de la imagen princip
app = ctk.CTk()
app.geometry("400x400")
app.title("Generador de Códigos QR")

# Configurar el tema oscuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Aqui se crea el cuadro de texto
entrada_texto = ctk.CTkEntry(app, width=300, height=40, corner_radius=10, font=ctk.CTkFont(family="Roboto", size=14))
entrada_texto.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# Crear un botón para generar el código QR
boton_generar = ctk.CTkButton(app, text="Generar Código QR", command=generar_qr, fg_color="#4287f5", corner_radius=10, font=ctk.CTkFont(family="Roboto", size=14))
boton_generar.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
# Crear una etiqueta para mostrar el resultado
label_resultado = ctk.CTkLabel(app, text="", font=ctk.CTkFont(family="Roboto", size=14))
label_resultado.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

# Crear una etiqueta para mostrar el código QR
label_qr = ctk.CTkLabel(app, text="")
label_qr.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

app.mainloop()