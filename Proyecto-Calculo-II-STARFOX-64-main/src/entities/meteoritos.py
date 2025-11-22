import random
import os
from entities.Obstaculos import Obstaculos
from constantes import ANCHO

class OrquestrarMeteoritos:

    def __init__(self):
        self.ruta_meteorito = os.path.join("assets", "images", "enemies", "Asteroid_2_minerals.png")
        self.generador = self.generador_meteoritos()

    # Función generadora de meteoritos
    def generador_meteoritos(self):
        while True:
            meteorito = Obstaculos(pos_x=random.randint(0, ANCHO - 40),pos_y=-40,velocidad=random.randint(2, 5),ruta_imagen=self.ruta_meteorito)
            yield meteorito 

    #
    def intentar_generar(self, probabilidad=0.02):
        if random.random() < probabilidad:
            return next(self.generador)
        return None
