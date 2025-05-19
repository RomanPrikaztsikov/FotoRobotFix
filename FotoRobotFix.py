import customtkinter as ctk
from tkinter import simpledialog,Canvas
from PIL import Image, ImageTk
import pygame

# pygame.mixer.init()
# pygame.mixer.music.load("music.mp3")

app=ctk.CTk()
app.geometry("800x500")
app.title("Nao koostaja nuppudega")

canvas=Canvas(app, width=400, height=400, bg="black")
canvas.pack(side="right", padx=10, pady=10)

pildid = {}
objektid = {}
olemas ={}

def toggle_osa(nimi, fail, x, y):
    if olemas.get(nimi):
        canvas.delete(objektid[nimi])
        olemas[nimi]=False
    else:
        pil_img=Image.open(fail).convert("RGBA").resize((400, 400))
        tk_img = ImageTk.PhotoImage(pil_img)
        pildid[nimi]=tk_img
        objektid[nimi]=canvas.create_image(x, y, image=tk_img)
        olemas[nimi]=True


# def mängi_muusika():
#     pygame.mixer.music.play(loops=-1)

# def peata_muusika():
#     pygame.mixer.music.stop()

def salvesta_nagu():
    failinimi=simpledialog.askstring("Salvesta pilt", "Sisesta faili nimi (ilma laiendita):")
    if not failinimi:
        return

    lõpp_pilt=Image.new("RGBA", (400, 400), (255, 255, 255, 255))

    for nimi in ["otsmik", "silmad", "nina", "suu", "korvad"]:
        if olemas.get(nimi):
            failitee = {
                "ostmik": "face1.png",
                "silmad": "silmad1.png",
                "nina": "nina1.png",
                "suu": "mouth1.png",
                "korvad": "ears1.png"
                }.get(nimi)
            if failitee:
                osa = Image.open(failitee).convert("RGBA").resize((400, 400))
                lõpp_pilt.alpha_composite(osa)


toggle_osa("nagu", "face3.png", 200, 200)
olemas["nagu"] = True
frame=ctk.CTkFrame(app)
frame.pack(side="left", padx=10, pady=10)

seaded ={
    "width":150, "height":40,
    "font": ("Segoe UI Emoji", 32),
    "fg_color": "#4CAF50",
    "text_color": "white",
    "corner_radius": 20 }

ctk.CTkLabel(frame, text="Vali näosad:", **seaded).pack(pady=5)

ctk.CTkButton(frame, text="Otsmik", command=lambda: toggle_osa("face1.png", "face2.png", 200, 200), **seaded).pack(pady=3)
ctk.CTkButton(frame, text="Silmad", command=lambda: toggle_osa("eyes1.png", "eyes2.png", 200, 200), **seaded).pack(pady=3)
ctk.CTkButton(frame, text="Nina", command=lambda: toggle_osa("nose1.png", "nose2.png", 200, 200), **seaded).pack(pady=3)
ctk.CTkButton(frame, text="Suu", command=lambda: toggle_osa("mouth1.png", "mouth2.png", 200, 200), **seaded).pack(pady=3)
ctk.CTkButton(frame, text="Korvad", command=lambda: toggle_osa("ears1.png", "ears2.png", 200, 200), **seaded).pack(pady=3)
nupp=ctk.CTkButton(frame, text="Salvesta nagu", command=salvesta_nagu,**seaded)
nupp.pack(side="bottom", pady=10)


frame_mus=ctk.CTkFrame(frame)
frame_mus.pack(side="bottom", padx=10, pady=10)
# ctk.CTkButton(frame_mus, text="Mängi muusika", fg_color="4CAF50", command=mängi_muusika).pack(side="left", pady=10)
# ctk.CTkButton(frame_mus, text="Peata muusika", fg_color="4CAF50", command=peata_muusika).pack(side="left", pady=10)

app.mainloop()
