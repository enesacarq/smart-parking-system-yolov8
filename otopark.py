import cv2
import numpy as np
import json


class ParkYeri:
    def __init__(self,park_id,pts):
        self.park_id=park_id
        self.pts=pts



def park_yerlerini_isaretle(video):
    noktalar=[]
    son_dortgen=None
    park_yerleri=[]
    park_id=1
    def noktalari_sirala(noktalar):
        noktalar=np.array(noktalar)
        toplam=noktalar.sum(axis=1)
        fark=np.diff(noktalar,axis=1).flatten()
        
        sol_ust=noktalar[np.argmin(toplam)]
        sag_alt=noktalar[np.argmax(toplam)]
        sol_alt=noktalar[np.argmin(fark)]
        sag_ust=noktalar[np.argmax(fark)]

        return [sol_ust,sag_ust,sag_alt,sol_alt]

    def mouse(event ,x,y,flags,params):
        nonlocal noktalar, son_dortgen, park_id, park_yerleri
        if event == cv2.EVENT_LBUTTONDOWN:
            noktalar.append((x,y))
            cv2.circle(img,(x,y),3,(255,0,0),-1)

            if len(noktalar) == 4:
                sirali=noktalari_sirala(noktalar)
                pts= np.array(sirali,np.int32).reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(0,0,255),2)
                son_dortgen= pts.copy()
                noktalar.clear()
                park_yerleri.append(ParkYeri(park_id,pts.copy()))

                sol_alt=pts[1][0]
                yazi_konum=(int(sol_alt[0])+ 5, int(sol_alt[1])-7)
                cv2.putText(img,str(park_id),yazi_konum,cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)
                park_id+=1

        elif event ==cv2.EVENT_RBUTTONDOWN:
            if son_dortgen is not None:
                offset = np.array([x - son_dortgen[0][0][0], y - son_dortgen[0][0][1]])
                yeni_pts=son_dortgen +offset
                cv2.polylines(img,[yeni_pts],True,(0,0,255),2)

                park_yerleri.append(ParkYeri(park_id,yeni_pts))

                sol_alt=yeni_pts[1][0]
                yazi_konum=(int(sol_alt[0])+5,int(sol_alt[1])-7)
                cv2.putText(img, str(park_id), yazi_konum, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
                park_id+=1


    cap=cv2.VideoCapture(video)
    ret,img=cap.read()
    if ret is False:
        print("okunamadi")
        return []
    img=cv2.resize(img,(1080,720))
    cap.release()

    cv2.namedWindow("isaret")
    cv2.setMouseCallback("isaret",mouse)

    while True:
        cv2.imshow("isaret",img)
        key=cv2.waitKey(1) & 0xFF
        if key==27:
            break
    cv2.destroyAllWindows()
    return park_yerleri
def park_yerleri_kaydet(park_yerleri):
    park_data=[]
    for p in park_yerleri:
        pts_list=p.pts.reshape(-1,2).tolist()
        park_data.append({"park_id":p.park_id,"pts":pts_list})

    with open("park_yerleri.json","w") as f:
        json.dump(park_data,f,indent=4)

    print("Park yerleri json dosyasina kayit edildi.")


    
