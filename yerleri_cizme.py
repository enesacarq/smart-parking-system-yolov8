import cv2
import numpy as np
import json


class ParkYeri:
    def __init__(self, park_id, pts):
        self.park_id = park_id
        self.pts = pts


class ParkIsaretleyici:
    def __init__(self, video):
        self.video = video
        self.noktalar = []
        self.son_dortgen = None
        self.park_yerleri = []
        self.park_id = 1
        self.img = None

    def noktalari_sirala(self, noktalar):
        noktalar = np.array(noktalar)
        toplam = noktalar.sum(axis=1)
        fark = np.diff(noktalar, axis=1).flatten()

        sol_ust = noktalar[np.argmin(toplam)]
        sag_alt = noktalar[np.argmax(toplam)]
        sol_alt = noktalar[np.argmin(fark)]
        sag_ust = noktalar[np.argmax(fark)]

        return [sol_ust, sag_ust, sag_alt, sol_alt]

    def dortgen_ekle(self, pts):
        cv2.polylines(self.img, [pts], True, (0, 0, 255), 2)
        yazi_konum = (int(pts[1][0][0]) + 5, int(pts[1][0][1]) - 7)
        cv2.putText(self.img, str(self.park_id), yazi_konum,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
        self.park_yerleri.append(ParkYeri(self.park_id, pts.copy()))
        self.son_dortgen = pts.copy()
        self.park_id += 1

    def mouse(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.noktalar.append((x, y))
            cv2.circle(self.img, (x, y), 3, (255, 0, 0), -1)

            if len(self.noktalar) == 4:
                sirali = self.noktalari_sirala(self.noktalar)
                pts = np.array(sirali, np.int32).reshape((-1, 1, 2))
                self.dortgen_ekle(pts)
                self.noktalar.clear()

        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.son_dortgen is not None:
                offset = np.array([x - self.son_dortgen[0][0][0],
                                   y - self.son_dortgen[0][0][1]])
                yeni_pts = (self.son_dortgen + offset).astype(np.int32)
                self.dortgen_ekle(yeni_pts)

    def calistir(self):
        cap = cv2.VideoCapture(self.video)
        ret, self.img = cap.read()
        cap.release()

        if not ret:
            print("Okunamadi")
            return []

        self.img = cv2.resize(self.img, (1080, 720))
        cv2.namedWindow("isaret")
        cv2.setMouseCallback("isaret", self.mouse)

        while True:
            cv2.imshow("isaret", self.img)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return self.park_yerleri

    def kaydet(self, dosya):
        park_data = [
            {"park_id": p.park_id, "pts": p.pts.reshape(-1, 2).tolist()}
            for p in self.park_yerleri
        ]
        with open(dosya, "w") as f:
            json.dump(park_data, f, indent=4)
        print("Park yerleri json dosyasina kayit edildi.")


