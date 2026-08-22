import time
from statistics import mode

import cv2

from classes.grupo_arucos_lineal import GrupoArucosLineal
from utils.functions import calcular_distancia_grupo_arucos

# Cargar cámaras con preferencias
camera_0 = cv2.VideoCapture(0, cv2.CAP_V4L2)
camera_0.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# camera_0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camera_0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera_0.set(cv2.CAP_PROP_FPS, 15)


camera_2 = cv2.VideoCapture(2, cv2.CAP_V4L2)
camera_2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# camera_2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camera_2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera_2.set(cv2.CAP_PROP_FPS, 15)


camera_4 = cv2.VideoCapture(4, cv2.CAP_V4L2)
camera_4.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# camera_4.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camera_4.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera_4.set(cv2.CAP_PROP_FPS, 15)


camera_6 = cv2.VideoCapture(6, cv2.CAP_V4L2)
camera_6.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# camera_6.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camera_6.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera_6.set(cv2.CAP_PROP_FPS, 15)

# Configurar y medir filas de arucos
# Grupo de ArUcos camera_0
arucos_camara_0_fila_1 = GrupoArucosLineal(
    id_inicial=0,
    id_final=19,
    milimetros_pared_a_primer_aruco=20,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_0_fila_2 = GrupoArucosLineal(
    id_inicial=20,
    id_final=39,
    milimetros_pared_a_primer_aruco=25,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_0_fila_3 = GrupoArucosLineal(
    id_inicial=40,
    id_final=59,
    milimetros_pared_a_primer_aruco=30,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_0_fila_4 = GrupoArucosLineal(
    id_inicial=60,
    id_final=79,
    milimetros_pared_a_primer_aruco=35,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_0_fila_5 = GrupoArucosLineal(
    id_inicial=80,
    id_final=99,
    milimetros_pared_a_primer_aruco=40,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

# Grupo de ArUcos camera_2
arucos_camara_2_fila_1 = GrupoArucosLineal(
    id_inicial=100,
    id_final=119,
    milimetros_pared_a_primer_aruco=20,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_2_fila_2 = GrupoArucosLineal(
    id_inicial=120,
    id_final=139,
    milimetros_pared_a_primer_aruco=25,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_2_fila_3 = GrupoArucosLineal(
    id_inicial=140,
    id_final=159,
    milimetros_pared_a_primer_aruco=30,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_2_fila_4 = GrupoArucosLineal(
    id_inicial=160,
    id_final=179,
    milimetros_pared_a_primer_aruco=35,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_2_fila_5 = GrupoArucosLineal(
    id_inicial=180,
    id_final=199,
    milimetros_pared_a_primer_aruco=40,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

# Grupo de ArUcos camera_4
arucos_camara_4_fila_1 = GrupoArucosLineal(
    id_inicial=200,
    id_final=219,
    milimetros_pared_a_primer_aruco=20,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_4_fila_2 = GrupoArucosLineal(
    id_inicial=220,
    id_final=239,
    milimetros_pared_a_primer_aruco=25,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_4_fila_3 = GrupoArucosLineal(
    id_inicial=240,
    id_final=259,
    milimetros_pared_a_primer_aruco=30,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_4_fila_4 = GrupoArucosLineal(
    id_inicial=260,
    id_final=279,
    milimetros_pared_a_primer_aruco=35,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_4_fila_5 = GrupoArucosLineal(
    id_inicial=280,
    id_final=299,
    milimetros_pared_a_primer_aruco=40,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

# Grupo de ArUcos camera_6
arucos_camara_6_fila_1 = GrupoArucosLineal(
    id_inicial=300,
    id_final=319,
    milimetros_pared_a_primer_aruco=20,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_6_fila_2 = GrupoArucosLineal(
    id_inicial=320,
    id_final=339,
    milimetros_pared_a_primer_aruco=25,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_6_fila_3 = GrupoArucosLineal(
    id_inicial=340,
    id_final=359,
    milimetros_pared_a_primer_aruco=30,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_6_fila_4 = GrupoArucosLineal(
    id_inicial=360,
    id_final=379,
    milimetros_pared_a_primer_aruco=35,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

arucos_camara_6_fila_5 = GrupoArucosLineal(
    id_inicial=380,
    id_final=399,
    milimetros_pared_a_primer_aruco=40,
    tamanio_aruco_milimetros=20,
    separacion_arucos_en_milimetros=5,
    esquina_referencia_medicion=0,
)

# Configuración del detector de ArUcos
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# fps a mostrar
fps_por_segundo = 3

lista_ancho = []
lista_largo = []
lista_alto = []
lista_volumen = []

while True:
    # Inicializar variables de medidas objeto
    ancho = 0
    largo_1 = 0
    largo_2 = 0
    alto = 0
    volumen = 0

    # Verificar que se reciben frames de las 4 camaras
    ok_0, frame_cam_0 = camera_0.read()
    ok_2, frame_cam_2 = camera_2.read()
    ok_4, frame_cam_4 = camera_4.read()
    ok_6, frame_cam_6 = camera_6.read()

    if not ok_0 and not ok_2 and not ok_4 and not ok_6:
        print("No se pudo leer el frame de una de las cámaras")
        break

    start_time = time.time()

    # Detectar ArUcos
    corners_cam_0, ids_cam_0, _ = detector.detectMarkers(frame_cam_0)
    corners_cam_2, ids_cam_2, _ = detector.detectMarkers(frame_cam_2)
    corners_cam_4, ids_cam_4, _ = detector.detectMarkers(frame_cam_4)
    corners_cam_6, ids_cam_6, _ = detector.detectMarkers(frame_cam_6)

    # Dibujar ArUcos y almacenar medidas de las 3 dimenciones
    if ids_cam_0 is not None:
        cv2.aruco.drawDetectedMarkers(frame_cam_0, corners_cam_0, ids_cam_0)
        ancho = calcular_distancia_grupo_arucos(
            [
                arucos_camara_0_fila_1.medir(ids_cam_0.flatten()),
                arucos_camara_0_fila_2.medir(ids_cam_0.flatten()),
                arucos_camara_0_fila_3.medir(ids_cam_0.flatten()),
                arucos_camara_0_fila_4.medir(ids_cam_0.flatten()),
                arucos_camara_0_fila_5.medir(ids_cam_0.flatten()),
            ]
        )

    if ids_cam_2 is not None:
        cv2.aruco.drawDetectedMarkers(frame_cam_2, corners_cam_2, ids_cam_2)
        largo_1 = calcular_distancia_grupo_arucos(
            [
                arucos_camara_2_fila_1.medir(ids_cam_2.flatten()),
                arucos_camara_2_fila_2.medir(ids_cam_2.flatten()),
                arucos_camara_2_fila_3.medir(ids_cam_2.flatten()),
                arucos_camara_2_fila_4.medir(ids_cam_2.flatten()),
                arucos_camara_2_fila_5.medir(ids_cam_2.flatten()),
            ]
        )

    if ids_cam_4 is not None:
        cv2.aruco.drawDetectedMarkers(frame_cam_4, corners_cam_4, ids_cam_4)
        largo_2 = calcular_distancia_grupo_arucos(
            [
                arucos_camara_4_fila_1.medir(ids_cam_4.flatten()),
                arucos_camara_4_fila_2.medir(ids_cam_4.flatten()),
                arucos_camara_4_fila_3.medir(ids_cam_4.flatten()),
                arucos_camara_4_fila_4.medir(ids_cam_4.flatten()),
                arucos_camara_4_fila_5.medir(ids_cam_4.flatten()),
            ]
        )

    if ids_cam_6 is not None:
        cv2.aruco.drawDetectedMarkers(frame_cam_6, corners_cam_6, ids_cam_6)
        alto = calcular_distancia_grupo_arucos(
            [
                arucos_camara_6_fila_1.medir(ids_cam_6.flatten()),
                arucos_camara_6_fila_2.medir(ids_cam_6.flatten()),
                arucos_camara_6_fila_3.medir(ids_cam_6.flatten()),
                arucos_camara_6_fila_4.medir(ids_cam_6.flatten()),
                arucos_camara_6_fila_5.medir(ids_cam_6.flatten()),
            ]
        )

    # Calcular largo final
    largo = largo_1 + largo_2 - 5

    # Calcular volumen
    volumen = largo * alto * ancho

    # Almacenar en una lista las medidas para sacar la moda
    lista_alto.append(alto)
    lista_alto = lista_alto[-30:]
    lista_largo.append(largo)
    lista_largo = lista_largo[-30:]
    lista_ancho.append(ancho)
    lista_ancho = lista_ancho[-30:]
    lista_volumen.append(volumen)
    lista_volumen = lista_volumen[-30:]

    # Mostrar imagenes de las camaras
    cv2.imshow("Camara 0", frame_cam_0)
    cv2.imshow("Camara 2", frame_cam_2)
    cv2.imshow("Camara 4", frame_cam_4)
    cv2.imshow("Camara 6", frame_cam_6)

    # Mostrar medidas
    print(f"Alto: {mode(lista_alto) / 10:.1f}")
    print(f"Largo: {mode(lista_largo) / 10:.1f}")
    print(f"Ancho: {mode(lista_ancho) / 10:.1f}")
    print(f"Volumen: {mode(lista_volumen) / 10:.1f}")

    # Calcular espera para fps
    elapsed_time = time.time() - start_time
    time_to_wait = max(0, 1 / fps_por_segundo - elapsed_time)
    time.sleep(time_to_wait)

    # --------------------------------------------------------
    # Salir con Q
    # --------------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# 6. LIBERAR RECURSOS
# ============================================================

camera_0.release()
camera_2.release()
camera_4.release()
camera_6.release()

cv2.destroyAllWindows()
