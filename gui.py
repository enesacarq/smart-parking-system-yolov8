import tkinter as tk
import json
from PIL import Image,ImageTk
import cv2

class Gui:
    def __init__(self,pencere,park_yerleri):
        self.pencere=pencere
        self.pencere.title("Smart Parking System")
        self.pencere.geometry("1024x720+250+50")


        self.park_yerleri = self.park_yerlerini_yukle(park_yerleri)
        self.butonlari_olustur()
        self.sag_frame_olustur()
        self.park_alanlarini_olustur()
        

    def butonlari_olustur(self):
        self.buton1=tk.Button(self.pencere,text="Kamera1",fg="white",bg="#234C6A",activebackground="#327093")
        self.buton1.place(x=10,y=15,width=200)

        self.buton2=tk.Button(self.pencere,text="Kamera2",fg="white",bg="#234C6A",activebackground="#327093")
        self.buton2.place(x=220,y=15,width=200)

        self.buton3=tk.Button(self.pencere,text="Kamera3",fg="white",bg="#234C6A",activebackground="#327093")
        self.buton3.place(x=430,y=15,width=200)
    
    def park_yerlerini_yukle(self, dosya_adi):
        with open(dosya_adi, "r") as f:
            data = json.load(f)
        return data
    
    def sag_frame_olustur(self):

        dolu_sayisi = sum(1 for yer in self.park_yerleri if yer["durum"] == "true")
        bos_sayisi = sum(1 for yer in self.park_yerleri if yer["durum"] == "false")
        toplam = bos_sayisi + dolu_sayisi
        doluluk = int((dolu_sayisi / toplam) * 100) if toplam > 0 else 0  # ZeroDivision koruması
        doluluk = f"%{doluluk}"

        self.frame1=tk.Frame(self.pencere,bg="#86C0E9",width=374,height=700)
        self.frame1.place(x=640,y=15)
        #Bilgi ekranı frame
        self.frame2=tk.Frame(self.frame1,bg="white",width=354,height=50,relief="solid",borderwidth=2)
        self.frame2.place(x=10,y=10)

        #Bilgi ekranı labeli
        self.bilgiekranlabel=tk.Label(self.frame2,text="BİLGİ EKRANI",font=("Arial",26),bg="white")
        self.bilgiekranlabel.place(relx=0.5,rely=0.5,anchor="center")
        #Dolu frame
        self.frame3=tk.Frame(self.frame1,bg="white",width=172,height=140,relief="solid",borderwidth=2)
        self.frame3.place(x=10,y=70)

        #Dolu labeli
        self.dolulabel=tk.Label(self.frame3,bg="white",text="DOLU",font=("Arial",30))
        self.dolulabel.place(relx=0.5,anchor="n")

        #Dolu sayısı
        self.dolusayi=tk.Label(self.frame3,bg="white",text=str(dolu_sayisi),font=("Arial",40))
        self.dolusayi.place(relx=0.5,rely=0.90,anchor="s")

        #Boş frame
        self.frame4=tk.Frame(self.frame1,bg="white",width=172,height=140,relief="solid",borderwidth=2)
        self.frame4.place(x=192,y=70)

        #Boş labeli
        self.boslabel=tk.Label(self.frame4,bg="white",text="BOŞ",font=("Arial",30))
        self.boslabel.place(relx=0.5,anchor="n")

        #Boş sayısı
        self.bossayi=tk.Label(self.frame4,bg="white",text=str(bos_sayisi),font=("Arial",40))
        self.bossayi.place(relx=0.5,rely=0.90,anchor="s")
        #Doluluk frame
        self.frame5=tk.Frame(self.frame1,bg="white",width=354,height=50,relief="solid",borderwidth=2)
        self.frame5.place(x=10,y=220)

        #Doluluk labeli
        self.doluluklabel=tk.Label(self.frame5,text=doluluk,font=("Arial",26),bg="white")
        self.doluluklabel.place(relx=0.5,rely=0.5,anchor="center")

        #Sol label 
        self.cikti_label=tk.Label(self.pencere,bg="black")
        self.cikti_label.place(x=10,y=45,width=630,height=580)
        self.cikti_label.lift()

    def park_alanlarini_olustur(self):
        sutun = 4
        satir = 6
        boyut = 50
        bosluk = 10
        for i, yer in enumerate(self.park_yerleri):
            renk = "red" if yer["durum"] == "true" else "green"
            alanframe = tk.Frame(self.frame1, bg=renk, width=boyut, height=boyut, borderwidth=2, relief="solid")
            x = 10 + (i % satir) * (boyut + bosluk)
            y = 270 + (i // satir) * (boyut + bosluk)+bosluk
            alanframe.place(x=x, y=y)
            alanlabel = tk.Label(alanframe, text=str(yer["park_id"]), font=("Arial", 20), bg=renk)
            alanlabel.place(relx=0.5, rely=0.5, anchor="center")
            
    def ciktiyi_goster(self, frame, park_regions=None):
        if frame is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img = img.resize((630, 580), Image.LANCZOS)
            imgtk = ImageTk.PhotoImage(img)
            self.cikti_label.configure(image=imgtk)
            self.cikti_label.imgtk = imgtk

        if park_regions is not None:
            self.paneli_guncelle(park_regions)
                
    def paneli_guncelle(self, park_regions):
        # Dolu/boş sayılarını güncelle
        dolu_sayisi = sum(1 for yer in park_regions if yer["durum"] == "true")
        bos_sayisi = sum(1 for yer in park_regions if yer["durum"] == "false")
        toplam = dolu_sayisi + bos_sayisi
        doluluk = int((dolu_sayisi / toplam) * 100) if toplam > 0 else 0

        self.dolusayi.config(text=str(dolu_sayisi))
        self.bossayi.config(text=str(bos_sayisi))
        self.doluluklabel.config(text=f"%{doluluk}")

        # Park kutucuklarını güncelle
        for widget in self.frame1.winfo_children():
            info = widget.place_info()
            if info.get("y") and int(info["y"]) >= 270:  # park alanları bölgesi
                widget.destroy()

        self.park_yerleri = park_regions
        self.park_alanlarini_olustur()               


