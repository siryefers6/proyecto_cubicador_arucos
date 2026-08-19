import math

def dist_landmarks(landmark1, landmark2):
    """Calcula la distancia euclidiana entre dos puntos usando solo las coordenadas x e y."""
    return math.sqrt(
        (landmark2.x - landmark1.x) ** 2 +
        (landmark2.y - landmark1.y) ** 2
    )


def angle_landmarks(landmark_p1, landmark_vertice, landmark_p2):
    """
    Calcula el ángulo entre los puntos landmark_p1, landmark_vertice y landmark_p2, usando el vértice como punto central,
    considerando solo las coordenadas x e y.
    
    Parámetros:
        puntos landmark_p1, landmark_vertice, landmark_p2: Objetos NormalizedLandmark con atributos x e y.
    
    Retorna:
        El ángulo en grados.
    """
    # Vectores entre los puntos (solo en 2D)
    v1 = (landmark_p1.x - landmark_vertice.x, landmark_p1.y - landmark_vertice.y)
    v2 = (landmark_p2.x - landmark_vertice.x, landmark_p2.y - landmark_vertice.y)
    
    # Producto punto
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    
    # Magnitud de los vectores
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    # Calcular ángulo en radianes y convertir a grados
    cos_theta = dot_product / (mag_v1 * mag_v2)
    angulo_radianes = math.acos(max(-1, min(1, cos_theta)))
    angulo_grados = math.degrees(angulo_radianes)
    
    return angulo_grados