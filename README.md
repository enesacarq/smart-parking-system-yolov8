
# Akıllı Otopark Sistemi / Smart Parking System

**TR**  
Görüntü işleme ve yapay zeka algoritmaları kullanarak açık otoparklardaki park alanlarının doluluk analizini gerçekleştiren bir akıllı otopark sistemi.  

**EN**  
A smart parking system that performs occupancy analysis of parking spaces in open parking lots using image processing and artificial intelligence algorithms.  

 --- 

## Çıktı / Output  
![Demo](output.gif)
***
## Proje Hakkında / About the Project   
**TR**  
Bu sistem otoparkta yerlerin gerçek zamanlı (real time) olarak boş veya doluluk durumu hakkında bilgi sağlar.  
   
Amaçlar:  
- Açık otoparklardaki park yeri bulma sürecini kolaylaştırmak  
- Park alanlarının doluluk durumunu anlık olarak tespit etmek  
- Sürücülerin girişte boş park yerlerini görerek zaman kaybını azaltmasını sağlamak  
- Otopark içindeki trafik yoğunluğunu ve kargaşayı azaltmak  
- Olası kazaların önüne geçilmesini sağlamak
- Görüntü işleme ve yapay zeka teknolojilerinin gerçek dünya problemlerine uygulanmasını göstermek 

**EN**  
This system provides real-time information about whether parking spaces 
in a parking lot are available or occupied.
  
Objectives:
- To facilitate the process of finding a parking space in open parking lots
- To detect the occupancy status of parking spaces in real time
- To reduce time loss by allowing drivers to see available parking spaces at the entrance
- To reduce traffic congestion and chaos inside the parking lot
- To prevent possible accidents
- To demonstrate the application of image processing and 
  artificial intelligence technologies to real-world problems

  
---
## Teknolojiler / Technologies
- Python 3.8+  
- tkinter  (gui)
- opencv-python   
- YOLOv8 (ultralytics)  
- threading  
- json  
- numpy  
- torch  
- Pillow
 ---   
## Kurulum  / Installation
Repoyu klonla 
```bash
git clone https://github.com/enesacarq/smart-parking-system-yolov8.git
```
Klasöre git
```bash
cd smart-parking-system-yolov8
```
Sanal ortam oluştur(önerilen)
```bash
python -m venv venv
```
Sanal ortamı aktif et  

Windows:
```bash
venv\Scripts\activate
```
macOS/Linux:
```bash
source venv/bin/activate
```
Gerekli paketleri yükle
```bash
pip install -r requirements.txt
```
Projeyi çalştır
```bash
python main.py
```
  
---
## Referanslar / References
- AI Model: [yolov8s-visdrone](https://huggingface.co/mshamrai/yolov8s-visdrone) — mshamrai (OpenRAIL Lisansı)
- GUI: [OtoparkTakipSistemi](https://github.com/adilomrplt/OtoparkTakipSistemi) — adilomrplt
---  
## License
[MIT](https://choosealicense.com/licenses/mit/)



