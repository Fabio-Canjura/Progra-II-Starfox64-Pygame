import pygame
from constantes import ANCHO, ALTO

class ObjetoJuego(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, imagen=None, tam=(50, 50)):
        super().__init__()

        #Carga de sprite
        if imagen:
            try:
                self.image = pygame.image.load(imagen).convert_alpha()
            except Exception:
                self.image = pygame.Surface(tam)
                self.image.fill((255, 255, 255))
        else:
            self.image = pygame.Surface(tam)
            self.image.fill((255, 255, 255))

        # Rectangulo del objeto
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        
    def update(self, segundos_por_frame):
        """Método polimórfico para ser sobrescrito por subclases."""
        pass

    def mover(self, segundos_por_frame):
        """Método polimórfico que las subclases deben sobreescribir."""
        pass


