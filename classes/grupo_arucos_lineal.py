class GrupoArucosLineal:
    """
    Clase que representa un grupo de arucos dispuestos en línea.
    """
    def __init__(
        self,
        id_inicial: int,
        id_final: int,
        milimetros_pared_a_primer_aruco: int,
        tamanio_aruco_milimetros: int,
        separacion_arucos_en_milimetros: int,
        esquina_referencia_medicion: int,
    ):
        self.id_inicial = id_inicial
        self.id_final = id_final
        self.milimetros_pared_a_primer_aruco = milimetros_pared_a_primer_aruco
        self.tamanio_aruco_milimetros = tamanio_aruco_milimetros
        self.separacion_arucos_en_milimetros = separacion_arucos_en_milimetros
        self.esquina_referencia_medicion = esquina_referencia_medicion

    def calcular_distancia_aruco(self, id_aruco: int) -> int:
        """
        Calcula la distancia desde la pared hasta el aruco con el id dado.
        """
        if id_aruco < self.id_inicial or id_aruco > self.id_final:
            raise ValueError("ID de aruco fuera del rango permitido.")

        # Calcular la distancia desde la pared hasta el primer aruco
        distancia = self.milimetros_pared_a_primer_aruco

        # Calcular la distancia adicional para los arucos posteriores
        if id_aruco > self.id_inicial:
            num_arucos_anteriores = id_aruco - self.id_inicial
            distancia += num_arucos_anteriores * (
                self.tamanio_aruco_milimetros + self.separacion_arucos_en_milimetros
            )

        return distancia
