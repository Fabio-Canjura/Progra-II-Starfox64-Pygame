import pygame
import os
import random
from constantes import ANCHO, ALTO

class power_up(pygame.sprite.Sprite):

    def __init__(self, tipo, Pos_X=None, Pos_y=None):
        super().__init__()

        self.tipo = tipo   # "mejora_disparo", "escudo", "bomba", etc.

        # --- Imagen (placeholder simple por ahora) ---
        self.image = pygame.Surface((25, 25))
        
        if tipo == "mejora_disparo":
            ruta_powerup = os.path.join("assets", "images", "proyectiles", "aro_amarillo1.png")
            try:
                self.image = pygame.image.load(ruta_powerup).convert_alpha()
                self.image = pygame.transform.scale(self.image, (35, 35))
            except:
                # Creación de placeholder en caso de falla.
                self.image = pygame.Surface((25, 25))
                self.image.fill((255, 215, 0))

        elif tipo == "escudo":
            self.image.fill((0, 150, 255))   # Azul claro
        elif tipo == "bomba":
            self.image.fill((255, 50, 50))   # Rojo
        else:
            self.image.fill((200, 200, 200)) # Gris neutro

        # --- Posición ---
        self.rect = self.image.get_rect()

        if Pos_X is None: Pos_X = random.randint(40, ANCHO - 40)
        if Pos_y is None: Pos_y = -50  # Aparece desde arriba

        self.rect.center = (Pos_X, Pos_y)

        # Velocidad de caída del powerup
        self.velocidad = 130

    def update(self, segundos_por_frame):
        self.rect.y += self.velocidad * segundos_por_frame

        # Si sale de la pantalla desaparece
        if self.rect.top > ALTO:
            self.kill()
