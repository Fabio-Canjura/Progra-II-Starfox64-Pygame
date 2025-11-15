# Este archivo configura los comportamientos propios del Arwing de Fox McCloud
import pygame
import os
from constantes import (ANCHO, ALTO, POS_INICIO_X, POS_INICIO_Y)
from entities.Objetos_Madre import ObjetoJuego
from entities.proyectiles import Proyectil


class Arwing(ObjetoJuego):

    def __init__(self):
        # Configuraciones del Airwing
        self.salud = 100
        self.velocidad_base = 180
        self.velocidad_actual = self.velocidad_base
        self.velocidad_maxima = 350   # Aceleración
        self.velocidad_minima = 150    # Desaceleración
        self.potencia_aceleracion = 300 # Para acelerar paulatinamente
        # Valores para disparar
        self.cadencia_disparo = 0.20    # 5 disparos * segundo
        self.tiempo_ultimo_disparo = 0  #Acumulador de tiempo para calculo entre disparos 
        self.danio_disparo = 10         # daño base del disparo
        
        # Inicializar ObjetoJuego
        super().__init__(
            pos_x=POS_INICIO_X,
            pos_y=POS_INICIO_Y
        )
        # Cargar sprite del Airwing
        ruta_airwing = os.path.join("assets", "images", "player", "nave_fox.png")
        try:
            self.image = pygame.image.load(ruta_airwing).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except Exception:
            print("Error al cargar sprite del Airwing, usando placeholder.")
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))

        # Rect actualizado tras cambiar la imagen
        self.rect = self.image.get_rect(center=(POS_INICIO_X, POS_INICIO_Y))


    def update(self, segundos_por_frame):
        self.tiempo_ultimo_disparo += segundos_por_frame
        self.mover(segundos_por_frame)


    def mover(self, segundos_por_frame):
        keys = pygame.key.get_pressed()
        # Acelerar tecla A
        if keys[pygame.K_a]:
            self.velocidad_actual += self.potencia_aceleracion * segundos_por_frame
            if self.velocidad_actual > self.velocidad_maxima:
                self.velocidad_actual = self.velocidad_maxima
        # Descelerar tecla D
        elif keys[pygame.K_d]:
            self.velocidad_actual -= self.potencia_aceleracion * segundos_por_frame
            if self.velocidad_actual < self.velocidad_minima:
                self.velocidad_actual = self.velocidad_minima
        # Velocidad base si no se pulsa ningun boton
        else:
            if self.velocidad_actual > self.velocidad_base:
                self.velocidad_actual -= self.potencia_aceleracion * segundos_por_frame
                if self.velocidad_actual < self.velocidad_base:
                    self.velocidad_actual = self.velocidad_base

            elif self.velocidad_actual < self.velocidad_base:
                self.velocidad_actual += self.potencia_aceleracion * segundos_por_frame
                if self.velocidad_actual > self.velocidad_base:
                    self.velocidad_actual = self.velocidad_base

        # Movimiento del airwing
        desplazamiento = self.velocidad_actual * segundos_por_frame
        if keys[pygame.K_LEFT]:
            self.rect.x -= desplazamiento
        if keys[pygame.K_RIGHT]:
            self.rect.x += desplazamiento
        if keys[pygame.K_UP]:
            self.rect.y -= desplazamiento
        if keys[pygame.K_DOWN]:
            self.rect.y += desplazamiento

        # Limites dentro de la pantalla
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)

        limite_superior = ALTO * 0.2
        self.rect.top = max(limite_superior, self.rect.top)
        self.rect.bottom = min(ALTO, self.rect.bottom)

    #Método para disparar.
    def disparar(self, grupo_balas):
        if self.tiempo_ultimo_disparo >= self.cadencia_disparo:
            nuevo_disparo = Proyectil(x=self.rect.centerx, y=self.rect.top, velocidad_y=-600, danio=self.danio_disparo)
            grupo_balas.add(nuevo_disparo)
            self.tiempo_ultimo_disparo = 0

    # Método para recibir daño
    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.explotar()

    # Método para eliminar la nave
    def explotar(self):
        self.kill()
