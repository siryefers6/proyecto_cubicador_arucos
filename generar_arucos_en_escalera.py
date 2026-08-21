import sys

import cv2
import numpy as np

# ============================================================
# ARGUMENTOS
# ============================================================

if len(sys.argv) != 7:
    print(
        "Uso: python generar_arucos.py "
        "<columnas> <arucos_por_columna> "
        "<separacion> <desfase> "
        "<id_inicio> <id_fin>"
    )
    sys.exit(1)


columnas = int(sys.argv[1])
arucos_por_columna = int(sys.argv[2])
separacion = int(sys.argv[3])
desfase = int(sys.argv[4])
id_inicio = int(sys.argv[5])
id_fin = int(sys.argv[6])


# ============================================================
# VALIDACIONES
# ============================================================

if columnas <= 0:
    print("La cantidad de columnas debe ser mayor que 0.")
    sys.exit(1)

if arucos_por_columna <= 0:
    print("La cantidad de ArUcos por columna debe ser mayor que 0.")
    sys.exit(1)

if separacion < 0:
    print("La separación no puede ser negativa.")
    sys.exit(1)

if desfase < 0:
    print("El desfase no puede ser negativo.")
    sys.exit(1)

if id_inicio < 0:
    print("El ID inicial no puede ser negativo.")
    sys.exit(1)

if id_fin < id_inicio:
    print("El ID final debe ser mayor o igual al ID inicial.")
    sys.exit(1)

if id_fin > 999:
    print("DICT_4X4_1000 permite IDs desde 0 hasta 999.")
    sys.exit(1)


# ============================================================
# CANTIDAD DE ARUCOS
# ============================================================

cantidad_arucos = columnas * arucos_por_columna

cantidad_ids = id_fin - id_inicio + 1


# ============================================================
# VALIDAR QUE EL RANGO COINCIDA CON LA DISTRIBUCIÓN
# ============================================================

if cantidad_ids != cantidad_arucos:
    print()
    print("ERROR: La cantidad de IDs no coincide con la distribución.")
    print()
    print(f"Columnas:             {columnas}")
    print(f"ArUcos por columna:   {arucos_por_columna}")
    print(f"Posiciones disponibles: {cantidad_arucos}")
    print()
    print(f"ID inicial:           {id_inicio}")
    print(f"ID final:             {id_fin}")
    print(f"IDs solicitados:      {cantidad_ids}")
    print()
    print(
        "El rango de IDs debe contener exactamente "
        "la cantidad de posiciones disponibles."
    )
    sys.exit(1)


# ============================================================
# CONFIGURACIÓN
# ============================================================

TAMANO_ARUCO = 201
MARGEN = 40

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)


# ============================================================
# DIMENSIONES
# ============================================================

ancho = MARGEN * 2 + columnas * TAMANO_ARUCO + (columnas - 1) * separacion


alto_base = arucos_por_columna * TAMANO_ARUCO + (arucos_por_columna - 1) * separacion


alto = MARGEN * 2 + alto_base + (columnas - 1) * desfase


# ============================================================
# CREAR IMAGEN
# ============================================================

imagen = np.full((alto, ancho), 255, dtype=np.uint8)


# ============================================================
# GENERAR ARUCOS
# ============================================================

for columna in range(columnas):
    for fila in range(arucos_por_columna):
        # ----------------------------------------------------
        # ID
        # ----------------------------------------------------

        posicion = columna * arucos_por_columna + fila

        marker_id = id_inicio + posicion

        # ----------------------------------------------------
        # POSICIÓN X
        # ----------------------------------------------------

        x = MARGEN + columna * (TAMANO_ARUCO + separacion)

        # ----------------------------------------------------
        # POSICIÓN Y
        # ----------------------------------------------------

        y = MARGEN + fila * (TAMANO_ARUCO + separacion) + columna * desfase

        # ----------------------------------------------------
        # GENERAR ARUCO
        # ----------------------------------------------------

        marker = cv2.aruco.generateImageMarker(dictionary, marker_id, TAMANO_ARUCO)

        # ----------------------------------------------------
        # COLOCAR ARUCO
        # ----------------------------------------------------

        imagen[y : y + TAMANO_ARUCO, x : x + TAMANO_ARUCO] = marker


# ============================================================
# GUARDAR
# ============================================================

cv2.imwrite("output/arucos_escalera.png", imagen)


# ============================================================
# INFORMACIÓN
# ============================================================

print()
print("========================================")
print("       GENERADOR DE ARUCOS")
print("========================================")
print()

print(f"Columnas:              {columnas}")
print(f"ArUcos por columna:    {arucos_por_columna}")
print(f"Total de ArUcos:       {cantidad_arucos}")
print(f"ID inicial:            {id_inicio}")
print(f"ID final:              {id_fin}")
print(f"Separación:            {separacion}px")
print(f"Desfase:               {desfase}px")
print(f"Tamaño ArUco:          {TAMANO_ARUCO}px")
print(f"Tamaño imagen:         {ancho} x {alto}px")
print()

print("Imagen generada: arucos.png")
print()

"""

# Ejemplo de uso:
python generar_arucos.py 6 20 20 10 0 119
python generar_arucos.py <columnas> <arucos_por_columna> <separacion> <desfase> <id_inicio> <id_fin>

"""
