# Sistema de Detección de Fatiga en Conductores

Este proyecto implementa un sistema accesible y funcional que detecta signos de fatiga en conductores en tiempo real, utilizando visión por computador. Está diseñado para prevenir accidentes de tránsito causados por la somnolencia mediante análisis facial, alertas auditivas/visuales y registro de eventos.


##  Características

- Análisis en tiempo real de parpadeo y cierre de ojos.
- Cálculo de EAR (Eye Aspect Ratio) usando landmarks faciales.
- Alertas visuales en pantalla y sonoras mediante `playsound`.
- Registro automático en archivo CSV de todos los eventos críticos.
- Interfaz gráfica simple para iniciar/detener el monitoreo.
- Código abierto y adaptable a contextos de bajo costo.

---

##  Motivación

Este sistema responde al Objetivo de Desarrollo Sostenible **ODS 3 (Salud y Bienestar)** y **ODS 11 (Ciudades sostenibles)**, brindando una herramienta económica que mejora la seguridad vial y previene accidentes asociados a la fatiga.

---

##  Capturas de pantalla

*(Opcional: agregar imágenes del sistema en ejecución)*

---

## ⚙️ Instalación

### Requisitos

- Python 3.11 o superior
- Archivo `shape_predictor_68_face_landmarks.dat` de Dlib  
  ➤ [Descargar desde Dlib.net](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

### Clonar el repositorio

```bash
git clone https://github.com/MarquezM14/Proyecto_TPI_Deteccion.git
cd deteccion-fatiga
````

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

1. Ejecuta el archivo de interfaz:

```bash
python interfaz.py
```

2. Haz clic en **"Iniciar Monitoreo"** para comenzar.
3. Presiona **`q`** o **`ESC`** para detener el monitoreo desde la ventana de video.
4. El sistema creará o actualizará el archivo `historial_alertas.csv` con los eventos detectados.

---

## 📁 Estructura del Proyecto

```
deteccion-fatiga/
│
├── detector_fatiga.py        # Lógica del sistema de detección
├── interfaz.py               # Interfaz gráfica con botones
├── alarma.mp3                # Sonido de alerta
├── historial_alertas.csv     # Registro de eventos detectados
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── shape_predictor_68_face_landmarks.dat  # Modelo Dlib (no incluido por defecto)
```

---

## 🛠️ Tecnologías utilizadas

* Python 3
* OpenCV
* Dlib
* Playsound
* Tkinter
* Scipy

---

## 📌 Estado del Proyecto

✅ Detección de fatiga funcionando
✅ Alerta sonora integrada
✅ Interfaz gráfica básica
🔜 Integración con IoT / Aplicación móvil
🔜 Exportación a Raspberry Pi o dispositivos embebidos

## 📄 Licencia

Este proyecto se distribuye bajo una [licencia de código abierto](LICENSE).


## 📬 Contacto

¿Tienes ideas para mejorar este proyecto o quieres contribuir?
Puedes contactarme o enviar un pull request. ¡Toda colaboración es bienvenida!

