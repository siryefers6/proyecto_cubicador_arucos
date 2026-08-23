import time

import cv2

from classes.camera_thread import CameraThread

# Configuración
CAMERA_IDS = (0, 1)

MOSTRAR_FRAME = True

# Detector ArUco
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(dictionary, parameters)


# Inicializar cámaras
print("Inicializando cámaras...")

camera_0 = CameraThread(CAMERA_IDS[0]).start()
camera_1 = CameraThread(CAMERA_IDS[1]).start()

print("Cámaras inicializadas.")
print("Esperando frames...")


try:
    while True:
        frame_0 = camera_0.read()
        frame_1 = camera_1.read()

        # Esperar hasta tener ambas imágenes
        if frame_0 is None or frame_1 is None:
            time.sleep(0.001)
            continue

        # Unir imágenes
        imagen_unida = cv2.hconcat([frame_0, frame_1])

        # Detectar sobre escala de grises
        gray = cv2.cvtColor(imagen_unida, cv2.COLOR_BGR2GRAY)

        corners, ids, rejects = detector.detectMarkers(gray)

        # Dibujar detecciones
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(imagen_unida, corners, ids)

        # Mostrar
        if MOSTRAR_FRAME:
            cv2.imshow("Imagen_unida", imagen_unida)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    print("Liberando cámaras...")

    camera_0.stop()
    camera_1.stop()

    cv2.destroyAllWindows()
