import cv2
import dlib
import csv
import datetime
import time
import threading
from scipy.spatial import distance
import os
import subprocess
import platform

# Opción 1: Usar pygame para reproducir audio 
try:
    import pygame
    pygame.mixer.init()
    AUDIO_METHOD = "pygame"
except ImportError:
    AUDIO_METHOD = "subprocess"

def calcular_EAR(ojo):
    A = distance.euclidean(ojo[1], ojo[5])
    B = distance.euclidean(ojo[2], ojo[4])
    C = distance.euclidean(ojo[0], ojo[3])
    return (A + B) / (2.0 * C)

def reproducir_alarma():
    """
    Función mejorada para reproducir alarma con múltiples métodos de respaldo
    """
    archivo_audio = "alarma.mp3"
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo_audio):
        print(f"Advertencia: No se encontró el archivo {archivo_audio}")
        return
    
    try:
        if AUDIO_METHOD == "pygame":
            # Método 1: Usar pygame (más confiable)
            pygame.mixer.music.load(archivo_audio)
            pygame.mixer.music.play()
        else:
            # Método 2: Usar subprocess con el reproductor del sistema
            if platform.system() == "Windows":
                # En Windows, usar el reproductor multimedia integrado
                subprocess.run(['powershell', '-c', 
                              f'(New-Object Media.SoundPlayer "{os.path.abspath(archivo_audio)}").PlaySync()'], 
                              check=False, timeout=5)
            else:
                # En Linux/Mac
                subprocess.run(['mpg123', archivo_audio], check=False, timeout=5)
                
    except Exception as e:
        print(f"Error al reproducir alarma: {e}")
        # Método de respaldo: usar el beep del sistema
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(1000, 1000)  # Frecuencia 1000Hz por 1 segundo
            else:
                print("\a")  # Beep del terminal
        except:
            print("¡ALERTA DE FATIGA!")

def reproducir_alarma_alternativa():
    """
    Método alternativo usando winsound (solo Windows)
    """
    try:
        import winsound
        # Reproducir con winsound (más confiable en Windows)
        winsound.PlaySound("alarma.mp3", winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"Error con winsound: {e}")
        # Usar beep del sistema como último recurso
        try:
            import winsound
            winsound.Beep(1000, 1000)
        except:
            print("¡ALERTA DE FATIGA!")

def iniciar_detector():
    UMBRAL_EAR = 0.25
    FRAMES_CONSEC = 20
    contador = 0
    alarma_activa = False
    
    # Verificar archivos necesarios
    if not os.path.exists("shape_predictor_68_face_landmarks.dat"):
        print("Error: No se encontró el archivo shape_predictor_68_face_landmarks.dat")
        print("Descárgalo desde: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        return
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    OJOS_IZQ = list(range(36, 42))
    OJOS_DER = list(range(42, 48))
    
    cam = cv2.VideoCapture(0)
    
    # Verificar si la cámara se abrió correctamente
    if not cam.isOpened():
        print("Error: No se pudo acceder a la cámara")
        return
    
    # Crear directorio para logs si no existe
    os.makedirs("logs", exist_ok=True)
    
    with open("logs/historial_alertas.csv", mode="a", newline="", encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        
        # Escribir encabezado solo si el archivo está vacío
        if os.path.getsize("logs/historial_alertas.csv") == 0:
            writer.writerow(["Fecha", "Hora", "Nivel EAR", "Alerta"])
        
        print("Detector de fatiga iniciado. Presiona 'q' o ESC para salir.")
        
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error: No se pudo leer frame de la cámara")
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
                    cv2.putText(frame, f"Cerrando ojos: {contador}/{FRAMES_CONSEC}", 
                               (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    
                    if contador >= FRAMES_CONSEC:
                        alerta = "FATIGA DETECTADA"
                        cv2.putText(frame, alerta, (30, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                        writer.writerow([fecha, hora, round(ear_prom, 3), alerta])
                        archivo.flush()  # Asegurar que se escriba al archivo
                        
                        if not alarma_activa:
                            # Usar threading para no bloquear la detección
                            threading.Thread(target=reproducir_alarma, daemon=True).start()
                            alarma_activa = True
                else:
                    if contador >= FRAMES_CONSEC:
                        writer.writerow([fecha, hora, round(ear_prom, 3), "RECUPERACIÓN"])
                        archivo.flush()
                    contador = 0
                    alarma_activa = False
                
                # Mostrar información en pantalla
                cv2.putText(frame, f"EAR: {ear_prom:.3f}", (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Umbral: {UMBRAL_EAR}", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Dibujar los puntos de los ojos
                for (x, y) in ojo_izq + ojo_der:
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            
            cv2.imshow("Detector de Fatiga", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # ESC o 'q'
                break
            
            time.sleep(0.05)
    
    cam.release()
    cv2.destroyAllWindows()
    print("Detector de fatiga finalizado.")

if __name__ == "__main__":
    iniciar_detector()