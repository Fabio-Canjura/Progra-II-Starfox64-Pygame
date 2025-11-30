import pygame
import os
from entities.Entidad_hostil import EntidadHostil

class Meteorito(EntidadHostil):
    def __init__(self, pos_x, pos_y, velocidad):
        
        self.tipo = "meteorito"
        ruta_meteoritos = os.path.join("assets", "images", "enemies", "Asteroid_2_minerals.png")
        imagen = pygame.image.load(ruta_meteoritos).convert_alpha()
        imagen = pygame.transform.scale(imagen, (45, 45))

        super().__init__(
            pos_x=pos_x,
            pos_y=pos_y,
            velocidad_y=velocidad,
            danio=25,
            vida=30,
            imagen=imagen,
            usar_movimiento_base=True  # El meteorito cae recto en eje y
        )
