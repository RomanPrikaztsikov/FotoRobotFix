import customtkinter as ctk
from tkinter import simpledialog, Canvas, filedialog
from PIL import Image, ImageTk

app = ctk.CTk()
app.geometry("800x500")
app.title("Näo koostaja nuppudega")

lõuend = Canvas(app, width=400, height=400, bg="gray")
lõuend.pack(side="right", padx=10, pady=10)

pildid = {}
objektid = {}
indeksid = {}  

taustad = ["face1.png", "face2.png", "face3.png", "face4.png", "face5.png"]
silmad_list = ["eyes1.png", "eyes2.png", "eyes3.png"]
nina_list = ["nose1.png", "nose2.png", "nose3.png"]
suu_list = ["mouth1.png", "mouth2.png", "mouth3.png"]
kõrvad_list = ["ears1.png", "ears2.png", "ears3.png"]

tausta_indeks = 0
tausta_id = None

def kuva_taust(indeks):
    global tausta_indeks, tausta_id
    tausta_indeks = indeks % len(taustad)
    pilt = Image.open(taustad[tausta_indeks]).convert("RGBA").resize((400, 400))
    tk_pilt = ImageTk.PhotoImage(pilt)
    pildid["taust"] = tk_pilt
    if tausta_id:
        lõuend.itemconfig(tausta_id, image=tk_pilt)
    else:
        tausta_id = lõuend.create_image(0, 0, image=tk_pilt, anchor="nw")

def järgmine_taust():
    kuva_taust(tausta_indeks + 1)

def kuva_osa(nimi, failid):
    indeks = indeksid.get(nimi, 0) % len(failid)
    fail = failid[indeks]
    indeksid[nimi] = (indeks + 1) % len(failid)

    if objektid.get(nimi):
        lõuend.delete(objektid[nimi])

    pilt = Image.open(fail).convert("RGBA").resize((400, 400))
    tk_pilt = ImageTk.PhotoImage(pilt)
    pildid[nimi] = tk_pilt
    objektid[nimi] = lõuend.create_image(200, 200, image=tk_pilt)

def salvesta_nagu():
    nimi = simpledialog.askstring("Salvesta pilt", "Sisesta faili nimi (ilma laiendita):")
    if not nimi:
        return

    pilt = Image.new("RGBA", (400, 400), (255, 255, 255, 255))
    taust = Image.open(taustad[tausta_indeks]).convert("RGBA").resize((400, 400))
    pilt.alpha_composite(taust)

    for osa in ["silmad", "nina", "suu", "kõrvad"]:
        if osa in objektid:
            aktiivne_indeks = (indeksid.get(osa, 0) - 1) % len(globals()[osa + "_list"])
            fail = globals()[osa + "_list"][aktiivne_indeks]
            kiht = Image.open(fail).convert("RGBA").resize((400, 400))
            pilt.alpha_composite(kiht)

    pilt.save(nimi + ".png")

def lisa_uus_taust():
    fail = filedialog.askopenfilename(title="Vali uus näo pilt", filetypes=[("PNG pildid", "*.png")])
    if fail:
        taustad.append(fail)
        kuva_taust(len(taustad)-1)

kuva_taust(0)

raam = ctk.CTkFrame(app)
raam.pack(side="left", padx=10, pady=10)

seaded = {
    "width": 150, "height": 40,
    "font": ("Segoe UI Emoji", 32),
    "fg_color": "#4CAF50",
    "text_color": "white",
    "corner_radius": 20
}

ctk.CTkLabel(raam, text="Vali näo osad:", **seaded).pack(pady=5)

ctk.CTkButton(raam, text="Nägu", command=järgmine_taust, **seaded).pack(pady=3)
ctk.CTkButton(raam, text="Silmad", command=lambda: kuva_osa("silmad", silmad_list), **seaded).pack(pady=3)
ctk.CTkButton(raam, text="Nina", command=lambda: kuva_osa("nina", nina_list), **seaded).pack(pady=3)
ctk.CTkButton(raam, text="Suu", command=lambda: kuva_osa("suu", suu_list), **seaded).pack(pady=3)
ctk.CTkButton(raam, text="Kõrvad", command=lambda: kuva_osa("kõrvad", kõrvad_list), **seaded).pack(pady=3)
ctk.CTkButton(raam, text="Lisa uus nägu", command=lisa_uus_taust, **seaded).pack(pady=10)
ctk.CTkButton(raam, text="Salvesta nägu", command=salvesta_nagu, **seaded).pack(pady=3)

app.mainloop()
