from utils.functions import calcular_distancia_grupo_arucos


def test_calcular_distancia_grupo_arucos():
    """
    Comprobar la función calcular_distancia_grupo_arucos
    """
    # Arrange
    lista_distancias = [20.5, 15.0, 17.5, 16.0]
    lista_distancias_vacia = []

    # Act
    distancia = calcular_distancia_grupo_arucos(lista_distancias)
    distancias_vacia = calcular_distancia_grupo_arucos(lista_distancias_vacia)

    # Assert
    assert distancia == 15.0
    assert distancias_vacia == 0.0
