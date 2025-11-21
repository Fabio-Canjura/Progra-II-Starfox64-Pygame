import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        ruta = os.path.join("assets", "images", "effects", "explosion.png")
        self.image = pygame.image.load(ruta).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect(center=(x, y))

        self.duracion = 300
        self.inicio = pygame.time.get_ticks()

    def update(self, segundos_por_frame):
        if pygame.time.get_ticks() - self.inicio > self.duracion:
            self.kill()
