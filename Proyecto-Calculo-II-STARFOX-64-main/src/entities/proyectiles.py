import os
import pygame
from constantes import ALTO

class Proyectil(pygame.sprite.Sprite):

    def __init__(self, x, y, velocidad_y=-600, danio=10, color=None, ancho=None, alto=None):
        super().__init__()
        #Carga de proyectiles en pantalla desde diccionario
        if color is not None and ancho is not None and alto is not None:
            # Proyectil generado desde el diccionario
            self.image = pygame.Surface((ancho, alto))
            self.image.fill(color)
        else:
            # Proyectil por defecto usando imagen
            ruta_proyectil = os.path.join("assets", "images", "player", "Airwing_bullet.png")
            try:
                self.image = pygame.image.load(ruta_proyectil).convert_alpha()
                self.image = pygame.transform.scale(self.image, (12, 24))
            except Exception:
                self.image = pygame.Surface((5, 15))
                self.image.fill((0, 200, 255))
                
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_y = velocidad_y
        self.danio = danio

    def update(self, segundos_por_frame):
        #Movimiento en eje Y sin interrumpir.
        self.rect.y += self.velocidad_y * segundos_por_frame
        # Si sale de la pantalla se elimina.
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill()
