from yerleri_cizme import ParkIsaretleyici
from arac_tanima import tanima
from ultralytics import YOLO
from gui import Gui
import tkinter as tk
import threading

modelcv="otopark_arac_tespit.pt"
model = YOLO(modelcv)
model.overrides['conf'] = 0.25
model.overrides['imgsz'] = 640

def main():
    video="otopark1.mp4"
    park_yerleri_dosyasi="park_yerleri.json"

    while True:
        deger=input("*****Menü*****\n1-Yerleri yeniden çiz.\n2-Mevcut yerleri kullan\n\t")
        if deger =="1":
            isaretleyici=ParkIsaretleyici(video)
            isaretleyici.calistir()
            isaretleyici.kaydet(park_yerleri_dosyasi)
            break
        elif deger=="2":
            break
        else :
            print("!!!Gecersiz deger girdiniz.Tekrar deneyiniz!!!\n")


    pencere=tk.Tk()
    app=Gui(pencere,park_yerleri_dosyasi)

    def guvenli_goster(frame, park_regions=None):
        pencere.after(0, app.ciktiyi_goster, frame, park_regions)


    threading.Thread(
        target=tanima,
        args=(video, park_yerleri_dosyasi, model),
        kwargs={"callback": guvenli_goster},
        daemon=True
    ).start()

    pencere.mainloop()


    

if __name__=="__main__":
    main()
