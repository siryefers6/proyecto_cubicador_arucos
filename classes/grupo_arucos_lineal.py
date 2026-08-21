class GrupoArucosLineal():
    def __init__(
        self,
        id_inicial: int,
        id_final: int,
        milimetros_pared_a_primer_aruco: int,
        tamanio_aruco_milimetros: int,
        separacion_arucos_en_milimetros: int,
        esquina_referencia_medicion: int
        ):
        self.id_inicial = id_inicial
        self.id_final = id_final
        self.milimetros_pared_a_primer_aruco = milimetros_pared_a_primer_aruco
        self.tamanio_aruco_milimetros = tamanio_aruco_milimetros
        self.separacion_arucos_en_milimetros = separacion_arucos_en_milimetros
        self.esquina_referencia_medicion = esquina_referencia_medicion
