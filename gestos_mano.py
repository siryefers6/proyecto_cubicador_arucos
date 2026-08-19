import functions_landmarks as fnl

class GestosMano:
    def __init__(self, hand_landmarks) -> None:
        self.hand_landmarks = hand_landmarks
        # Verificar si hay suficientes landmarks
        if len(self.hand_landmarks.landmark) < 21:
            raise ValueError("No se encontraron suficientes puntos de referencia")

        # Asignar todos los puntos de referencia en una lista
        self.hand_points = [self.hand_landmarks.landmark[i] for i in range(21)]


    def get_point(self, indice):
        """Devuelve el punto de referencia dado un índice."""
        if 0 <= indice < len(self.hand_points):
            return self.hand_points[indice]
        else:
            raise IndexError("Índice fuera de rango")


    def obtener_coordenadas(self, indice) -> tuple:
        """Devuelve las coordenadas (x, y, z) del punto dado un índice."""
        punto = self.get_point(indice)
        return punto.x, punto.y, punto.z


    def dedo_pulgar_extendido(self) -> bool:
        """
        Determina si el dedo pulgar está extendido.

        Returns:
            bool: True si el dedo está extendido, False si está recogido.
        """
        angulo = fnl.angle_landmarks(self.get_point(2), self.get_point(3), self.get_point(4))
        dist_point4_point17 = fnl.dist_landmarks(self.get_point(4), self.get_point(17))
        dist_point3_point17 = fnl.dist_landmarks(self.get_point(3), self.get_point(17))

        return dist_point3_point17 < dist_point4_point17 and angulo > 138


    def dedo_indice_extendido(self) -> bool:
        """
        Determina si el dedo índice está extendido.

        Returns:
            bool: True si el dedo está extendido, False si está recogido.
        """
        angulo_indice = fnl.angle_landmarks(self.get_point(8), self.get_point(6), self.get_point(5))

        # Distancias entre puntos de la mano
        dist_point8_point0 = fnl.dist_landmarks(self.get_point(8), self.get_point(0))
        dist_point7_point0 = fnl.dist_landmarks(self.get_point(7), self.get_point(0))
        dist_point6_point0 = fnl.dist_landmarks(self.get_point(6), self.get_point(0))

        return (dist_point8_point0 > dist_point7_point0 or dist_point7_point0 > dist_point6_point0) and angulo_indice > 110


    def dedo_corazon_extendido(self) -> bool:
        """
        Determina si el dedo corazón está extendido.

        Returns:
            bool: True si el dedo está extendido, False si está recogido.
        """
        angulo_corazon = fnl.angle_landmarks(self.get_point(12), self.get_point(10), self.get_point(9))

        # Distancias entre puntos de la mano
        dist_point12_point0 = fnl.dist_landmarks(self.get_point(12), self.get_point(0))
        dist_point11_point0 = fnl.dist_landmarks(self.get_point(11), self.get_point(0))
        dist_point10_point0 = fnl.dist_landmarks(self.get_point(10), self.get_point(0))

        return (dist_point12_point0 > dist_point11_point0 or dist_point11_point0 > dist_point10_point0) and angulo_corazon > 110


    def dedo_anular_extendido(self) -> bool:
        """
        Determina si el dedo anular está extendido.

        Returns:
            bool: True si el dedo está extendido, False si está recogido.
        """
        angulo_anular = fnl.angle_landmarks(self.get_point(16), self.get_point(14), self.get_point(13))

        # Distancias entre puntos de la mano
        dist_point16_point0 = fnl.dist_landmarks(self.get_point(16), self.get_point(0))
        dist_point15_point0 = fnl.dist_landmarks(self.get_point(15), self.get_point(0))
        dist_point14_point0 = fnl.dist_landmarks(self.get_point(14), self.get_point(0))

        return (dist_point16_point0 > dist_point15_point0 or dist_point15_point0 > dist_point14_point0) and angulo_anular > 110


    def dedo_menique_extendido(self) -> bool:
        """
        Determina si el dedo meñique está extendido.

        Returns:
            bool: True si el dedo está extendido, False si está recogido.
        """
        angulo_menique = fnl.angle_landmarks(self.get_point(20), self.get_point(18), self.get_point(17))

        # Distancias entre puntos de la mano
        dist_point20_point0 = fnl.dist_landmarks(self.get_point(20), self.get_point(0))
        dist_point19_point0 = fnl.dist_landmarks(self.get_point(19), self.get_point(0))
        dist_point18_point0 = fnl.dist_landmarks(self.get_point(18), self.get_point(0))

        return (dist_point20_point0 > dist_point19_point0 or dist_point19_point0 > dist_point18_point0) and angulo_menique > 110


    def mano_abierta(self) -> bool:
        """
        Determina si una mano está abierta si todos los dedos están extendidos.

        Returns:
            bool: True si la mano está abierta, False si está cerrada.
        """
        dedos_extendidos = sum([
            self.dedo_menique_extendido(),
            self.dedo_anular_extendido(),
            self.dedo_corazon_extendido(),
            self.dedo_indice_extendido(),
            self.dedo_pulgar_extendido()
        ])
        
        return dedos_extendidos > 3


    def like_pulgar(self) -> bool:
        """
        Determina si se está haciendo el gesto "like" (pulgar arriba).

        Returns:
            bool: True si el gesto like está presente, False si no.
        """
        dedos_correctos = all([
            not self.dedo_menique_extendido(),
            not self.dedo_anular_extendido(),
            not self.dedo_corazon_extendido(),
            not self.dedo_indice_extendido(),
            self.dedo_pulgar_extendido()
        ])

        angle_points_4_0_5 = fnl.angle_landmarks(self.get_point(4), self.get_point(0), self.get_point(5))

        return self.get_point(4).y < self.get_point(5).y and angle_points_4_0_5 > 16 and dedos_correctos


    def dislike_pulgar(self) -> bool:
        """
        Determina si se está haciendo el gesto "dislike" (pulgar abajo).

        Returns:
            bool: True si el gesto dislike está presente, False si no.
        """
        dedos_correctos = all([
            not self.dedo_menique_extendido(),
            not self.dedo_anular_extendido(),
            not self.dedo_corazon_extendido(),
            not self.dedo_indice_extendido(),
            self.dedo_pulgar_extendido()
        ])

        angle_points_4_0_5 = fnl.angle_landmarks(self.get_point(4), self.get_point(0), self.get_point(5))

        return self.get_point(4).y > self.get_point(5).y and angle_points_4_0_5 > 16 and dedos_correctos
