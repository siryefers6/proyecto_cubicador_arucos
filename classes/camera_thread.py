import platform
import threading
import time

import cv2

# =========================
# Configuración
# =========================

WIDTH = 640
HEIGHT = 480
FPS = 15


# =========================
# Captura de cámara
# =========================


class CameraThread:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.frame = None
        self.running = False

        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._capture, daemon=True)

        # Usar backend apropiado para cada sistema
        if platform.system() == "Windows":
            backend = cv2.CAP_DSHOW
        else:
            backend = cv2.CAP_ANY

        self.camera = cv2.VideoCapture(camera_id, backend)

        if not self.camera.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara {camera_id}")

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.camera.set(cv2.CAP_PROP_FPS, FPS)

        # Reducir frames almacenados por el backend
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def start(self):
        self.running = True
        self.thread.start()
        return self

    def _capture(self):
        while self.running:
            ret, frame = self.camera.read()

            if not ret:
                time.sleep(0.01)
                continue

            # Conservar solamente el frame más reciente
            with self.lock:
                self.frame = frame

    def read(self):
        with self.lock:
            if self.frame is None:
                return None

            return self.frame.copy()

    def stop(self):
        self.running = False

        if self.thread.is_alive():
            self.thread.join(timeout=1)

        self.camera.release()
