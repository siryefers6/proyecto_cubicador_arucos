def calcular_distancia_grupo_arucos(lista_distancias: list) -> float:
    """
    Retorna el valor mas bajo de la lista.

    Args:
        lista_distancias (list): Lista de distancias
    """
    if lista_distancias:
        return min(lista_distancias)
    else:
        return 0.0