import cv2
import numpy as np

# ============================================================
# CONFIGURACIÓN
# ============================================================

# IDs de los ArUco que se quieren generar
id_inicial = 240
id_final = 319

# Cantidad de ArUcos que habrá verticalmente en cada columna
cantidad_arucos_por_columna = 10

# Dimensiones de la hoja carta
ancho_hoja_milimetros = 215.9
alto_hoja_milimetros = 279.4

# Márgenes
margen_milimetros = 1.42

# Separación entre ArUcos
separacion_horizontal_milimetros = 5
separacion_vertical_milimetros = 5

# Tamaño de cada ArUco
tamanio_aruco_milimetros = 21

# Resolución de la imagen
DPI = 600

# Diccionario ArUco
diccionario_aruco = cv2.aruco.DICT_4X4_1000

# Nombre del archivo de salida
nombre_archivo = "output/arucos_hoja_carta_milimetrados.png"


# ============================================================
# CONVERSIÓN DE MILÍMETROS A PÍXELES
# ============================================================


def mm_a_pixeles(mm):
    return round(mm * DPI / 25.4)


ancho_hoja_px = mm_a_pixeles(ancho_hoja_milimetros)
alto_hoja_px = mm_a_pixeles(alto_hoja_milimetros)

margen_px = mm_a_pixeles(margen_milimetros)

separacion_horizontal_px = mm_a_pixeles(separacion_horizontal_milimetros)

separacion_vertical_px = mm_a_pixeles(separacion_vertical_milimetros)

tamanio_aruco_px = mm_a_pixeles(tamanio_aruco_milimetros)


# ============================================================
# CÁLCULO DE CANTIDAD DE COLUMNAS
# ============================================================

espacio_disponible_ancho = ancho_hoja_px - 2 * margen_px

ancho_por_aruco = tamanio_aruco_px + separacion_horizontal_px

cantidad_columnas = (
    espacio_disponible_ancho + separacion_horizontal_px
) // ancho_por_aruco


# ============================================================
# VALIDACIONES
# ============================================================

cantidad_ids = id_final - id_inicial + 1

cantidad_maxima_arucos = cantidad_columnas * cantidad_arucos_por_columna

if cantidad_ids > cantidad_maxima_arucos:
    raise ValueError(
        f"No caben todos los ArUcos.\n"
        f"Capacidad de la hoja: {cantidad_maxima_arucos}\n"
        f"ArUcos solicitados: {cantidad_ids}"
    )

if id_inicial < 0 or id_final >= 1000:
    raise ValueError("DICT_4X4_1000 permite IDs desde 0 hasta 999.")


# ============================================================
# CREAR HOJA BLANCA
# ============================================================

hoja = np.ones((alto_hoja_px, ancho_hoja_px), dtype=np.uint8) * 255


# ============================================================
# CREAR DICCIONARIO ARUCO
# ============================================================

dictionary = cv2.aruco.getPredefinedDictionary(diccionario_aruco)


# ============================================================
# GENERAR Y COLOCAR LOS ARUCOS
# ============================================================

id_actual = id_inicial

for columna in range(int(cantidad_columnas)):
    for fila in range(cantidad_arucos_por_columna):
        # Si ya colocamos todos los IDs, terminamos
        if id_actual > id_final:
            break

        # ----------------------------------------------------
        # Posición del ArUco
        # ----------------------------------------------------

        x = margen_px + columna * (tamanio_aruco_px + separacion_horizontal_px)

        y = margen_px + fila * (tamanio_aruco_px + separacion_vertical_px)

        # ----------------------------------------------------
        # Crear ArUco
        # ----------------------------------------------------

        aruco = cv2.aruco.generateImageMarker(dictionary, id_actual, tamanio_aruco_px)

        # ----------------------------------------------------
        # Colocar ArUco sobre la hoja
        # ----------------------------------------------------

        hoja[y : y + tamanio_aruco_px, x : x + tamanio_aruco_px] = aruco

        print(
            f"ArUco ID {id_actual}: "
            f"columna={columna + 1}, "
            f"fila={fila + 1}, "
            f"x={x}px, y={y}px"
        )

        id_actual += 1


# ============================================================
# GUARDAR IMAGEN
# ============================================================

cv2.imwrite(nombre_archivo, hoja)


# ============================================================
# INFORMACIÓN
# ============================================================

print("\n========================================")
print("HOJA GENERADA")
print("========================================")
print(f"Resolución: {DPI} DPI")
print(f"Hoja: {ancho_hoja_milimetros} x {alto_hoja_milimetros} mm")
print(f"Resolución: {ancho_hoja_px} x {alto_hoja_px} px")
print(f"Tamaño ArUco: {tamanio_aruco_milimetros} mm")
print(f"Margen: {margen_milimetros} mm")
print(f"Separación horizontal: {separacion_horizontal_milimetros} mm")
print(f"Separación vertical: {separacion_vertical_milimetros} mm")
print(f"Columnas: {cantidad_columnas}")
print(f"ArUcos por columna: {cantidad_arucos_por_columna}")
print(f"IDs: {id_inicial} - {id_final}")
print(f"Archivo: {nombre_archivo}")
print("========================================")
