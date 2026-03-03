import tkinter as tk
import json
import numpy as np


class Gui:
    def __init__(self, pencere, park_yerleri_dosyasi="park_yerleri.json"):
        self.pencere = pencere
        self.pencere.title("Smart Parking System")
        self.pencere.geometry("1024x720+250+50")

        self.park_yerleri_dosyasi = park_yerleri_dosyasi
        self.park_verileri = self.json_veri_yukle()

        self.butonlari_olustur()
        self.sag_frame_olustur()

    # -----------------------------
    # JSON OKUMA & DURUM EKLEME
    # -----------------------------
    def json_veri_yukle(self):
        with open(self.park_yerleri_dosyasi, "r", encoding="utf-8") as f:
            veriler = json.load(f)

        # Her park yerine varsayılan 'yok' durumu ekle
        for yer in veriler:
            if "durum" not in yer:
                yer["durum"] = "yok"

        return veriler

    # -----------------------------
    # BUTONLAR
    # -----------------------------
    def butonlari_olustur(self):
        self.buton1 = tk.Button(self.pencere, text="Kamera1",
                                fg="white", bg="#234C6A", activebackground="#327093")
        self.buton1.place(x=10, y=15, width=200)

        self.buton2 = tk.Button(self.pencere, text="Kamera2",
                                fg="white", bg="#234C6A", activebackground="#327093")
        self.buton2.place(x=220, y=15, width=200)

        self.buton3 = tk.Button(self.pencere, text="Kamera3",
                                fg="white", bg="#234C6A", activebackground="#327093")
        self.buton3.place(x=430, y=15, width=200)

    # -----------------------------
    # SAĞ PANEL
    # -----------------------------
    def sag_frame_olustur(self):
        self.frame1 = tk.Frame(self.pencere, bg="#86C0E9", width=374, height=700)
        self.frame1.place(x=640, y=15)

        self.bilgi_alanlarini_olustur()
        self.park_alanlarini_olustur()

    # -----------------------------
    # BİLGİ PANELİ
    # -----------------------------
    def bilgi_alanlarini_olustur(self):
        dolu_sayisi = sum(1 for yer in self.park_verileri if yer["durum"] == "var")
        bos_sayisi = sum(1 for yer in self.park_verileri if yer["durum"] == "yok")

        toplam = dolu_sayisi + bos_sayisi
        oran = int((dolu_sayisi / toplam) * 100) if toplam > 0 else 0

        # Dolu
        frame3 = tk.Frame(self.frame1, bg="white", width=172, height=140,
                          relief="solid", borderwidth=2)
        frame3.place(x=10, y=70)

        tk.Label(frame3, text="DOLU", font=("Arial", 30),
                 bg="white").place(relx=0.5, anchor="n")
        tk.Label(frame3, text=str(dolu_sayisi), font=("Arial", 40),
                 bg="white").place(relx=0.5, rely=0.90, anchor="s")

        # Boş
        frame4 = tk.Frame(self.frame1, bg="white", width=172, height=140,
                          relief="solid", borderwidth=2)
        frame4.place(x=192, y=70)

        tk.Label(frame4, text="BOŞ", font=("Arial", 30),
                 bg="white").place(relx=0.5, anchor="n")
        tk.Label(frame4, text=str(bos_sayisi), font=("Arial", 40),
                 bg="white").place(relx=0.5, rely=0.90, anchor="s")

        # Doluluk oranı
        frame5 = tk.Frame(self.frame1, bg="white", width=354, height=50,
                          relief="solid", borderwidth=2)
        frame5.place(x=10, y=220)

        tk.Label(frame5, text=f"Doluluk = %{oran}", font=("Arial", 26),
                 bg="white").place(relx=0.5, rely=0.5, anchor="center")

    # -----------------------------
    # PARK ALANLARI (JSON'DAN DİNAMİK)
    # -----------------------------
    def park_alanlarini_olustur(self):
        boyut = 50
        for yer in self.park_verileri:
            # renk: var -> kırmızı, yok -> yeşil
            renk = "red" if yer["durum"] == "var" else "green"

            # pts listesinden basitçe ilk koordinatları kullanıyoruz
            x = yer["pts"][0][0]
            y = yer["pts"][0][1]

            alanframe = tk.Frame(self.frame1, bg=renk, width=boyut, height=boyut,
                                 borderwidth=2, relief="solid")
            alanframe.place(x=x, y=y)

            alanlabel = tk.Label(alanframe, text=str(yer["park_id"]),
                                 font=("Arial", 20), bg=renk)
            alanlabel.place(relx=0.5, rely=0.5, anchor="center")


def main():
    pencere = tk.Tk()
    app = Gui(pencere)
    pencere.mainloop()


if __name__ == "__main__":
    main()