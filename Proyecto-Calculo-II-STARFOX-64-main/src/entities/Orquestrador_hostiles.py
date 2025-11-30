import random

class OrquestadorHostiles:

    def __init__(self, lista_objetos):
        self.lista_objetos = lista_objetos
        self.generador = self.generador_hostiles()

    def generador_hostiles(self):
        for objeto in self.lista_objetos:
            pos_x = random.randint(0, 760)
            pos_y = -25
            velocidad = random.randint(2, 5)
            enemigo = objeto(pos_x, pos_y, velocidad)
            yield enemigo

