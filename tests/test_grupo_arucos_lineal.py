from grupo_arucos_lineal import GrupoArucosLineal

def test_inicializar_clase_grupo_arucos_lineal():
    """
    Probar instancia de clase GrupoArucosLineal
    """
    # Arrange
    id_inicial = 0
    id_final = 10
    milimetros_pared_a_primer_aruco = 5
    tamanio_aruco_milimetros = 20
    separacion_arucos_en_milimetros = 5
    esquina_referencia_medicion = 0

    # Act
    grupo_arucos_lineal = GrupoArucosLineal(
        id_inicial,
        id_final,
        milimetros_pared_a_primer_aruco,
        tamanio_aruco_milimetros,
        separacion_arucos_en_milimetros,
        esquina_referencia_medicion
        )

    # Assert
    assert grupo_arucos_lineal.id_inicial == 0
