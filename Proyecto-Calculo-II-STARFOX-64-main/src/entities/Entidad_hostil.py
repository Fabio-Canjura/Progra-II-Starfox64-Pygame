import pygame

class EntidadHostil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, velocidad_y, danio, vida, imagen, usar_movimiento_base=True):
        super().__init__()

        self.image = imagen
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        # Atributos
        self.velocidad_y = velocidad_y
        self.danio = danio
        self.vida = vida
        self.viva = True

        self.usar_movimiento_base = usar_movimiento_base

    def update(self, segundos_por_frame, grupo_balas_enemigo=None):
        if self.usar_movimiento_base:
            self.rect.y += self.velocidad_y * segundos_por_frame * 60
    
        if self.rect.top > 900 or self.rect.bottom < -100:
            self.kill()

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.morir()

    def colisionar_con_arwing(self, arwing):
        arwing.recibir_dano(self.danio)
        arwing.aplicar_lentitud()
        arwing.degradar_disparo()
        self.morir()

    def morir(self):
        self.viva = False
        self.kill()
