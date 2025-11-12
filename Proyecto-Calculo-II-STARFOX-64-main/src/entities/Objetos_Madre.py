import pygame
from constantes import ANCHO, ALTO

class ObjetoJuego(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, vida_inicial=100, imagen=None, tam=(50, 50)):
        super().__init__()

        if imagen:
            try:
                self.image = pygame.image.load(imagen).convert_alpha()
            except Exception:
                self.image = pygame.Surface(tam)
                self.image.fill((255, 255, 255))
        else:
            self.image = pygame.Surface(tam)
            self.image.fill((255, 255, 255))

        # Configurar rect y salud
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidad = pygame.math.Vector2(0, 0)
        self.salud = vida_inicial

    def recibir_danio(self, cantidad):
        """Resta salud al objeto y lo elimina si llega a cero."""
        self.salud -= cantidad
        if self.salud <= 0:
            self.morir()

    def mover(self):
        """Método polimórfico que las subclases deben sobreescribir."""
        pass

    def morir(self):
        """Elimina el sprite del grupo."""
        self.kill()

    def actualizar_pantalla(self):
        """Llama al movimiento y actualiza la posición."""
        self.mover()
