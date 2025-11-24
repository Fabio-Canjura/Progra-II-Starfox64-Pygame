# Clase encargada de manejar la funcion recursiva, se usa para contar meteoritos en pantalla

def contar_meteoritos(lista):
    if not lista:
        return 0
    # cuenta 1 y llama nuevamente a la función con el resto de la lista
    return 1 + contar_meteoritos(lista[1:])