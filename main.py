import re
import time

import cv2
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

DIBUJAR_ARUCOS = False

CANTIDAD_MEDICIONES_VALIDAS = 20

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
num_pedido = 0

try:
    while True:
        # Input de entrada digitar pedido:
        num_pedido = re.search(r"(3\d{7})", input("Escanea caja para medir: ")).group()
        if num_pedido:
            num_pedido = int(num_pedido)

        time.sleep(1)

        while True:

            frame_count += 1
            frame_0 = camera_0.read()
            frame_1 = camera_1.read()

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
                        min_ancho = min(list_ancho)
                        min_largo = min(list_largo)
                        min_alto = min(list_alto)
                        volumen = min_ancho * min_largo * min_alto

                        # Guarda la información en la base de datos
                        pedido = Pedido(
                            num_pedido=num_pedido, # falta implementación
                            cantidad_bultos=1, # falta implementación
                            num_bulto=1, # falta implementación
                            ancho_mm=min_ancho,
                            largo_mm=min_largo,
                            alto_mm=min_alto,
                            volumen_mm=volumen,
                            peso=1, # falta implementación
                            valor_volumetrico=111, # falta implementación
                        )

                        ruta_imagen_medidas = guardar_imagen_medidas(imagen_unida, num_pedido)
                        pedido.imagen_medidas = ruta_imagen_medidas
                        ruta_imagen_respaldo = guardar_imagen_respaldo(imagen_unida, num_pedido)
                        pedido.imagen_respaldo = ruta_imagen_respaldo

                        with Session(engine) as session:
                            crear_pedido(session, pedido)

                        # Mostrar medidas almacenadas
                        print("\nMedidas registradas")
                        print("----------")
                        print(f"ancho: {min_ancho} mm")
                        print(f"largo: {min_largo} mm")
                        print(f"alto: {min_alto} mm")
                        print(f"volumen: {volumen} mm3")
                        print("**********")
                        print(f"ancho: {min_ancho / 10:.2f} cm")
                        print(f"largo: {min_largo / 10:.2f} cm")
                        print(f"alto: {min_alto / 10:.2f} cm")
                        print(f"volumen: {volumen / 1000} cm3")
                        print("----------")
                        print("<<<<<<<Ya puede retirar el objeto>>>>>>>\n")

                        list_ancho.clear()
                        list_largo.clear()
                        list_alto.clear()

                        cv2.destroyAllWindows()
                        break
                            

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
