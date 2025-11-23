# Iteradores personalizados para recorrer los niveles de disparo del Arwing
class Iterador_disparos:
    #Iterador normal: recorre los niveles en orden.

    def __init__(self, lista_niveles, indice_actual):
        self.lista = lista_niveles
        self.indice = indice_actual

    def __iter__(self):
        return self

    def __next__(self):
        if self.indice >= len(self.lista):
            raise StopIteration
        valor = self.lista[self.indice]
        self.indice += 1
        return valor

class Iterador_disparos_inverso:

    def __init__(self, lista_niveles, indice_actual):
        self.lista = lista_niveles
        self.indice = indice_actual

    def __iter__(self):
        return self

    def __next__(self):
        if self.indice < 0:
            raise StopIteration
        valor = self.lista[self.indice]
        self.indice -= 1
        return valor

