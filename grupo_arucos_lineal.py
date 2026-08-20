class GrupoArucosLineal():
    def __init__(
        self,
        id_inicial,
        id_final,
        milimetros_pared_a_primer_aruco,
        tamanio_aruco_milimetros,
        separacion_arucos_en_milimetros,
        esquina_referencia_medicion
        ):
        self.id_inicial = id_inicial
        self.id_final = id_final
        self.milimetros_pared_a_primer_aruco = milimetros_pared_a_primer_aruco
        self.tamanio_aruco_milimetros = tamanio_aruco_milimetros
        self.separacion_arucos_en_milimetros = separacion_arucos_en_milimetros
        self.esquina_referencia_medicion = esquina_referencia_medicion
