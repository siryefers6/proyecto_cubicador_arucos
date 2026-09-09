import time
from statistics import mode

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from sqlmodel import Session

import config
from app.database import engine
from app.models import Pedido
from app.services.imagenes import guardar_imagen_medidas, guardar_imagen_respaldo
from app.services.pedidos import crear_pedido
from classes.camera_thread import CameraThread
from utils.functions import calcular_distancia_grupo_arucos

# Configuración
CAMERA_IDS = (0, 1)

MOSTRAR_FRAME = True

DIBUJAR_ARUCOS = True

CANTIDAD_MEDICIONES_VALIDAS = 30

# Configuración mediapipe detección manos
MODEL_PATH = "hand_landmarker.task"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.4,
    min_hand_presence_confidence=0.4,
    min_tracking_confidence=0.4,
)

detector_hands = vision.HandLandmarker.create_from_options(options)

# Cargar arucos medidos
arucos_alto = config.arucos_alto
arucos_largo = config.arucos_largo
arucos_ancho = config.arucos_ancho

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

# Contador de frames para detectar arucos y medir
frame_count = 0

# Inicializar listas para hayar la moda de mediciones
list_ancho = []
list_largo = []
list_alto = []

# Estados
medicion_realizada = False
mostrar_primer_mensaje = True

try:
    while True:
        frame_count += 1
        frame_0 = camera_0.read()
        frame_1 = camera_1.read()

        # Si todo esta correcto notificar que puede empezar a medir
        if mostrar_primer_mensaje:
            print("...Esperando un objeto para medir...")
            mostrar_primer_mensaje = False

        # Esperar hasta tener ambas imágenes
        if frame_0 is None or frame_1 is None:
            time.sleep(0.001)
            continue

        # Unir imágenes
        imagen_unida = cv2.hconcat([frame_0, frame_1])

        # Detectar ArUcos cada x frames
        if frame_count % 10 == 0:
            # Detectar sobre escala de grises
            gray = cv2.cvtColor(imagen_unida, cv2.COLOR_BGR2GRAY)

            corners, ids, rejects = detector.detectMarkers(gray)

            # Dibujar detecciones
            if ids is not None and DIBUJAR_ARUCOS:
                cv2.aruco.drawDetectedMarkers(imagen_unida, corners, ids)

            # Tomar medidas largo, alto, ancho, volumen
            if ids is not None:
                ids_detectados = ids.flatten()
                ancho = calcular_distancia_grupo_arucos(
                    [
                        arucos_ancho[0].medir(ids_detectados),
                        arucos_ancho[1].medir(ids_detectados),
                        arucos_ancho[2].medir(ids_detectados),
                        arucos_ancho[3].medir(ids_detectados),
                        arucos_ancho[4].medir(ids_detectados),
                    ]
                )
                largo = calcular_distancia_grupo_arucos(
                    [
                        arucos_largo[0].medir(ids_detectados),
                        arucos_largo[1].medir(ids_detectados),
                        arucos_largo[2].medir(ids_detectados),
                        arucos_largo[3].medir(ids_detectados),
                        arucos_largo[4].medir(ids_detectados),
                    ]
                )
                alto = calcular_distancia_grupo_arucos(
                    [
                        arucos_alto[0].medir(ids_detectados),
                        arucos_alto[1].medir(ids_detectados),
                        arucos_alto[2].medir(ids_detectados),
                        arucos_alto[3].medir(ids_detectados),
                        arucos_alto[4].medir(ids_detectados),
                    ]
                )

                # Verificar si hay manos en la imagen
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_0)
                result = detector_hands.detect(mp_image)

                # Registrar medidas en lista si no está a la vista el aruco id 0 y el 300 y no hay manos
                if (
                    (0 not in ids_detectados and 300 not in ids_detectados and 20 not in ids_detectados and 320 not in ids_detectados)
                    and not medicion_realizada
                    and not result.hand_landmarks
                ):
                    list_ancho.append(ancho)
                    list_ancho = list_ancho[-CANTIDAD_MEDICIONES_VALIDAS:]
                    list_largo.append(largo)
                    list_largo = list_largo[-CANTIDAD_MEDICIONES_VALIDAS:]
                    list_alto.append(alto)
                    list_alto = list_alto[-CANTIDAD_MEDICIONES_VALIDAS:]

                    # Mostrar medidas validas que serán registradas
                    print("----------")
                    print(f"ancho: {ancho} mm")
                    print(f"largo: {largo} mm")
                    print(f"alto: {alto} mm")
                    print("**********")
                    print(f"ancho: {ancho / 10:.2f} cm")
                    print(f"largo: {largo / 10:.2f} cm")
                    print(f"alto: {alto / 10:.2f} cm")
                    print("----------")

                    # Guardar medidas si ya hay x registros validos
                    if (
                        len(list_ancho) == CANTIDAD_MEDICIONES_VALIDAS
                        and len(list_largo) == CANTIDAD_MEDICIONES_VALIDAS
                        and len(list_alto) == CANTIDAD_MEDICIONES_VALIDAS
                    ):
                        moda_ancho = mode(list_ancho)
                        moda_largo = mode(list_largo)
                        moda_alto = mode(list_alto)
                        volumen = moda_ancho * moda_largo * moda_alto

                        # Guarda la información en la base de datos
                        pedido = Pedido(
                            num_pedido="PED-001", # falta implementación
                            cantidad_bultos=1, # falta implementación
                            num_bulto=1, # falta implementación
                            ancho_mm=moda_ancho,
                            largo_mm=moda_largo,
                            alto_mm=moda_alto,
                            volumen_mm=volumen,
                            peso=1, # falta implementación
                            valor_volumetrico=111, # falta implementación
                        )

                        ruta_imagen_medidas = guardar_imagen_medidas(imagen_unida, "PED-001")
                        pedido.imagen_medidas = ruta_imagen_medidas
                        ruta_imagen_respaldo = guardar_imagen_respaldo(imagen_unida, "PED-001")
                        pedido.imagen_respaldo = ruta_imagen_respaldo

                        with Session(engine) as session:
                            crear_pedido(session, pedido)

                        # Mostrar medidas almacenadas
                        print("\nMedidas registradas")
                        print("----------")
                        print(f"ancho: {moda_ancho} mm")
                        print(f"largo: {moda_largo} mm")
                        print(f"alto: {moda_alto} mm")
                        print(f"volumen: {volumen} mm3")
                        print("**********")
                        print(f"ancho: {moda_ancho / 10:.2f} cm")
                        print(f"largo: {moda_largo / 10:.2f} cm")
                        print(f"alto: {moda_alto / 10:.2f} cm")
                        print(f"volumen: {volumen / 1000} cm3")
                        print("----------")
                        print("<<<<<<<Ya puede retirar el objeto>>>>>>>\n")
                        medicion_realizada = True

                        

                elif 0 in ids_detectados or 300 in ids_detectados or 20 in ids_detectados or 320 in ids_detectados:
                    if medicion_realizada:
                        print("...Esperando un objeto para medir...")

                    if len(list_ancho) or len(list_largo) or len(list_alto):
                        print("listas de medición reiniciadas arucos iniciales detectados")
                    list_ancho.clear()
                    list_largo.clear()
                    list_alto.clear()

                    medicion_realizada = False

                elif result.hand_landmarks:
                    list_ancho.clear()
                    list_largo.clear()
                    list_alto.clear()
                    print("listas de medición reiniciadas manos detectadas")

        # Mostrar imagen de camaras
        if MOSTRAR_FRAME:
            cv2.imshow("Imagen_unida", imagen_unida)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    print("Liberando cámaras...")

    camera_0.stop()
    camera_1.stop()

    cv2.destroyAllWindows()
