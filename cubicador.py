import cv2

camera_number = int(input("Ingrese número de camara a utilizar (0, 1, 2, 3, 4): "))
# ============================================================
# CONFIGURACIÓN DE MEDIDAS
# ============================================================

dict_id_mm = {}

# Distancia entre la esquina 0 de un ArUco
# y la esquina 0 del siguiente ArUco
mm_entre_arucos = 12.2

# Rango de IDs utilizados
id_inicial = int(input("Digite ID inicial: "))
id_final = int(input("Digite ID final: "))

# Cantidad de ArUcos por bloque
arucos_por_bloque = 20

# Desfase de cada bloque
desfase_mm = 1.9

# Distancia inicial del primer ArUco
mm_inicial = 23


# ============================================================
# GENERAR DICCIONARIO ID → DISTANCIA
# ============================================================

for i in range(id_inicial, id_final + 1):

    # Convertir el ID absoluto en un índice relativo
    indice = i - id_inicial

    # Determinar bloque y posición dentro del bloque
    bloque = indice // arucos_por_bloque
    posicion = indice % arucos_por_bloque

    # Calcular el inicio del bloque
    mm_inicial_bloque = (
        mm_inicial
        + (bloque * desfase_mm)
    )

    # Calcular distancia correspondiente al ID
    dict_id_mm[i] = (
        mm_inicial_bloque
        + (posicion * mm_entre_arucos)
    )


# ============================================================
# MOSTRAR DICCIONARIO
# ============================================================

for marker_id, medida_mm in dict_id_mm.items():
    print(
        f"ID {marker_id}: "
        f"{medida_mm:.1f} mm "
        f"({medida_mm / 10:.1f} cm)"
    )


# ============================================================
# 1. SELECCIONAR DICCIONARIO ARUCO
# ============================================================

dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_1000
)


# ============================================================
# 2. CREAR PARÁMETROS DEL DETECTOR
# ============================================================

parameters = cv2.aruco.DetectorParameters()


# ============================================================
# 3. CREAR DETECTOR
# ============================================================

detector = cv2.aruco.ArucoDetector(
    dictionary,
    parameters
)


# ============================================================
# 4. ABRIR CÁMARA
# ============================================================

camera = cv2.VideoCapture(camera_number)

if not camera.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")


# ============================================================
# 5. BUCLE PRINCIPAL
# ============================================================

while True:

    ok, frame = camera.read()

    if not ok:
        print("No se pudo leer el frame")
        break


    # --------------------------------------------------------
    # Detectar ArUcos
    # --------------------------------------------------------

    corners, ids, rejected = detector.detectMarkers(frame)


    # --------------------------------------------------------
    # Procesar detecciones
    # --------------------------------------------------------

    if ids is not None:

        # Dibujar ArUcos detectados
        cv2.aruco.drawDetectedMarkers(
            frame,
            corners,
            ids
        )


        # Lista de medidas correspondientes
        # a los ArUcos detectados
        lista_medidas = []


        for marker_id in ids.flatten():

            if marker_id in dict_id_mm:

                medida_mm = dict_id_mm[marker_id]

                lista_medidas.append(medida_mm)


        # ----------------------------------------------------
        # Mostrar medida
        # ----------------------------------------------------

        if lista_medidas:

            # Tomar la menor medida detectada
            medida_mm = min(lista_medidas)

            # Convertir mm → cm
            medida_cm = medida_mm / 10


            print(
                "Medida detectada:",
                round(medida_cm, 1),
                "cm"
            )


    # --------------------------------------------------------
    # Mostrar imagen
    # --------------------------------------------------------

    cv2.imshow(
        "Detector ArUco",
        frame
    )


    # --------------------------------------------------------
    # Salir con Q
    # --------------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# 6. LIBERAR RECURSOS
# ============================================================

camera.release()

cv2.destroyAllWindows()