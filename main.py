from yerleri_cizme import ParkIsaretleyici
from arac_tanima import tanima
from ultralytics import YOLO

modelcv="a.pt"
model = YOLO(modelcv)
model.overrides['conf'] = 0.25
model.overrides['imgsz'] = 1024

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

    tanima(video,park_yerleri_dosyasi,model)

if __name__=="__main__":
    main()
