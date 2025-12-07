# clase pensada para contar las partidas ganadas y perdidas 

class Contador_Partidas:
    def __init__(self):
        self.victorias = 0
        self.derrotas = 0

    def registrar_victoria(self):
        self.victorias += 1

    def registrar_derrota(self):
        self.derrotas += 1

    def texto(self):
        return f"Victorias: {self.victorias}  |  Derrotas: {self.derrotas}"
