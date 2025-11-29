# Función recursiva para contar sprites
def contar_recursivo(lista_sprites):
    if not lista_sprites:
        return 0
    return 1 + contar_recursivo(lista_sprites[1:])
