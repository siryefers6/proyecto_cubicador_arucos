import csv
from datetime import datetime
from pathlib import Path

import cv2


class RegistroMedicion:
    def __init__(
        self,
        archivo_csv: str = "mediciones_200.csv",
        carpeta_fotos: str = "fotos",
    ):
        self.archivo_csv = Path(archivo_csv)
        self.carpeta_fotos = Path(carpeta_fotos)

        self.carpeta_fotos.mkdir(parents=True, exist_ok=True)

        self._crear_csv()

    def _crear_csv(self):
        if self.archivo_csv.exists():
            return

        with self.archivo_csv.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)

            escritor.writerow(
                [
                    "id",
                    "fecha_registro",
                    "foto_cam_0",
                    "foto_cam_1",
                    "largo_mm",
                    "alto_mm",
                    "ancho_mm",
                    "volumen_mm3",
                ]
            )

    def guardar(
        self,
        frame_cam_0,
        frame_cam_1,
        largo: float,
        alto: float,
        ancho: float,
        volumen: float,
    ):
        fecha = datetime.now()

        id_medicion = fecha.strftime("%Y%m%d_%H%M%S_%f")

        nombres_fotos = {
            "cam_0": f"{id_medicion}_cam0.jpg",
            "cam_1": f"{id_medicion}_cam1.jpg",
        }

        frames = {
            "cam_0": frame_cam_0,
            "cam_1": frame_cam_1,
        }

        for camara, frame in frames.items():
            ruta = self.carpeta_fotos / nombres_fotos[camara]
            cv2.imwrite(str(ruta), frame)

        with self.archivo_csv.open("a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)

            escritor.writerow(
                [
                    id_medicion,
                    fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    nombres_fotos["cam_0"],
                    nombres_fotos["cam_1"],
                    largo,
                    alto,
                    ancho,
                    volumen,
                ]
            )
