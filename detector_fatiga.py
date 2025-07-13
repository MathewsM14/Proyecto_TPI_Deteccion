
import cv2
import dlib
import csv
import datetime
import time
import threading
from scipy.spatial import distance
from playsound import playsound

def calcular_EAR(ojo):
    A = distance.euclidean(ojo[1], ojo[5])
    B = distance.euclidean(ojo[2], ojo[4])
    C = distance.euclidean(ojo[0], ojo[3])
    return (A + B) / (2.0 * C)

def reproducir_alarma():
    playsound("alarma.mp3")

def iniciar_detector():
    UMBRAL_EAR = 0.25
    FRAMES_CONSEC = 20
    contador = 0
    alarma_activa = False

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    OJOS_IZQ = list(range(36, 42))
    OJOS_DER = list(range(42, 48))
    cam = cv2.VideoCapture(0)

    with open("historial_alertas.csv", mode="a", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["Fecha", "Hora", "Nivel EAR", "Alerta"])

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostros = detector(gris)

            for rostro in rostros:
                landmarks = predictor(gris, rostro)
                coords = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)]

                ojo_izq = [coords[i] for i in OJOS_IZQ]
                ojo_der = [coords[i] for i in OJOS_DER]

                ear_izq = calcular_EAR(ojo_izq)
                ear_der = calcular_EAR(ojo_der)
                ear_prom = (ear_izq + ear_der) / 2.0

                ahora = datetime.datetime.now()
                fecha = ahora.strftime("%Y-%m-%d")
                hora = ahora.strftime("%H:%M:%S")
                alerta = ""

                if ear_prom < UMBRAL_EAR:
                    contador += 1
                    if contador >= FRAMES_CONSEC:
                        alerta = "FATIGA DETECTADA"
                        cv2.putText(frame, alerta, (30, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                        writer.writerow([fecha, hora, round(ear_prom, 3), alerta])
                        if not alarma_activa:
                            threading.Thread(target=reproducir_alarma, daemon=True).start()
                            alarma_activa = True
                else:
                    if contador >= FRAMES_CONSEC:
                        writer.writerow([fecha, hora, round(ear_prom, 3), "RECUPERACIÓN"])
                    contador = 0
                    alarma_activa = False

                cv2.putText(frame, f"EAR: {ear_prom:.2f}", (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("Detección de fatiga (con historial)", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

            time.sleep(0.05)

    cam.release()
    cv2.destroyAllWindows()
