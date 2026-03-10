import cv2
import json
import numpy as np
from ultralytics import YOLO
import threading

def tanima(video,park_yerleri,model,callback=None):

    with open(park_yerleri, "r") as f:
        park_regions = json.load(f)

    park_memory = {}

    for park in park_regions:
        park_memory[park["park_id"]] = {
            "counter": 0,
            "status": False
        }

    cap = cv2.VideoCapture(video)

    frame_skip = 3
    frame_count = 0
    last_centers = []

    def thread_loop():
        nonlocal last_centers,frame_count
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("goruntu veri okunamadi-threadloop")
                break
            print(f"Video frame okundu: ret={ret}, frame={frame.shape}")
            frame = cv2.resize(frame, (1080, 720))
            frame_count += 1

            if frame_count % frame_skip == 0:
                results = model.predict(
                    source=frame,
                    classes=[3, 4, 5, 9],
                    verbose=False
                )

                boxes = results[0].boxes.xyxy.cpu().numpy()

                car_centers = []
                for box in boxes:
                    x1, y1, x2, y2 = box
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    car_centers.append((cx, cy))

                last_centers = car_centers

            else:
                car_centers = last_centers

            for cx, cy in car_centers:
                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

            for park in park_regions:
                pts = np.array(park['pts'], np.int32)
                park_id = park['park_id']

                dolu_mu = False

                for cx, cy in car_centers:
                    if cv2.pointPolygonTest(pts, (float(cx), float(cy)), False) >= 0:
                        dolu_mu = True
                        break

                memory = park_memory[park_id]


                if dolu_mu:
                    memory["counter"] += 1
                else:
                    memory["counter"] -= 1

                memory["counter"] = max(0, min(memory["counter"], 10))

                if memory["counter"] >= 4:
                    memory["status"] = True
                elif memory["counter"] <= 1:
                    memory["status"] = False

                park["durum"] = "true" if memory["status"] else "false"

                renk = (0, 0, 255) if memory["status"] else (0, 255, 0)
                

                cv2.polylines(frame, [pts], True, renk, 2)

                cv2.putText(
                    frame,
                    f"ID:{park_id}",
                    (pts[0][0], pts[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    renk,
                    2
                )
            if callback:
                callback(frame.copy())#güvenlik için kopya

            if cv2.waitKey(20) & 0xFF == 27:
                break
    

    with open(park_yerleri, "w") as f:
        json.dump(park_regions, f, indent=4)
    cap.release()
    cv2.destroyAllWindows()
    t=threading.Thread(target=thread_loop,daemon=True)
    t.start()
    

