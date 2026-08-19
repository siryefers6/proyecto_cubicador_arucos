import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gestos_mano import GestosMano


# ============================================================
# CONFIGURACIÓN
# ============================================================

MODEL_PATH = "hand_landmarker.task"


# ============================================================
# CONFIGURAR MEDIAPIPE
# ============================================================

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

detector = vision.HandLandmarker.create_from_options(options)


# ============================================================
# CÁMARA
# ============================================================

cap = cv2.VideoCapture(0)


try:

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break


        # ====================================================
        # BGR → RGB
        # ====================================================

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # ====================================================
        # CONVERTIR A MEDIAPIPE IMAGE
        # ====================================================

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )


        # ====================================================
        # DETECTAR MANOS
        # ====================================================

        result = detector.detect(mp_image)


        # ====================================================
        # PROCESAR MANOS
        # ====================================================

        for idx, hand_landmarks in enumerate(
            result.hand_landmarks
        ):

            # -----------------------------------------------
            # Obtener tipo de mano
            # -----------------------------------------------

            handedness = result.handedness[idx]

            hand_type = handedness[0].category_name

            print(f"Mano detectada: {hand_type}")


            # -----------------------------------------------
            # Crear GestosMano
            # -----------------------------------------------

            gestos = GestosMano(hand_landmarks)


            # -----------------------------------------------
            # Detectar gestos
            # -----------------------------------------------

            dislike_pulgar = gestos.dislike_pulgar()
            like_pulgar = gestos.like_pulgar()
            mano_abierta = gestos.mano_abierta()


            # -----------------------------------------------
            # Acciones
            # -----------------------------------------------

            if hand_type == "Left":

                if dislike_pulgar:
                    print("Mano izquierda: Dando dislike")

                if mano_abierta:
                    print("Mano izquierda: Mano abierta")


            elif hand_type == "Right":

                if like_pulgar:
                    print("Mano derecha: Dando like")

                if mano_abierta:
                    print("Mano derecha: Mano abierta")


            # =================================================
            # DIBUJAR LANDMARKS
            # =================================================

            height, width, _ = frame.shape

            for landmark in hand_landmarks:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 0),
                    -1
                )


    # ========================================================
    # MOSTRAR
    # ========================================================

        cv2.imshow(
            "MediaPipe Hands",
            frame
        )


        if cv2.waitKey(1) & 0xFF == 27:
            break


finally:

    cap.release()

    detector.close()

    cv2.destroyAllWindows()