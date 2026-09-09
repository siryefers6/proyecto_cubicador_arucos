from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = BASE_DIR / "media"

MEDIDAS_DIR = MEDIA_DIR / "medidas"
RESPALDO_DIR = MEDIA_DIR / "respaldo"

MEDIDAS_DIR.mkdir(parents=True, exist_ok=True)
RESPALDO_DIR.mkdir(parents=True, exist_ok=True)


def guardar_imagen_medidas(imagen, nombre: str) -> str:
    ruta = MEDIDAS_DIR / f"{nombre}.webp"

    cv2.imwrite(
        str(ruta),
        imagen,
        [cv2.IMWRITE_WEBP_QUALITY, 80],
    )

    return str(ruta)


def guardar_imagen_respaldo(imagen, nombre: str) -> str:
    ruta = RESPALDO_DIR / f"{nombre}.webp"

    cv2.imwrite(
        str(ruta),
        imagen,
        [cv2.IMWRITE_WEBP_QUALITY, 80],
    )

    return str(ruta)