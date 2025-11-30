import random
import pygame
import os

from entities.Entidad_hostil import EntidadHostil
from entities.proyectiles import Proyectil
from constantes import ANCHO, ALTO


class Enemigos(EntidadHostil):
    def __init__(self, pos_x, pos_y, velocidad):
    
        self.tipo = "enemigo"
        # Cargar imagen
        ruta_naves_enemigas = os.path.join("assets", "images", "enemies", "Enemigo_rojo_no_fondo.png")
        imagen = pygame.image.load(ruta_naves_enemigas).convert_alpha()
        imagen = pygame.transform.scale(imagen, (50, 50))

        # Llamada a clase madre
        super().__init__(
            pos_x=pos_x,
            pos_y=pos_y,
            velocidad_y=velocidad,
            danio=20,
            vida=100,
            imagen=imagen,
            usar_movimiento_base=False
        )

        # Disparo enemigo
        self.tiempo_ultimo_disparo = 0
        self.cadencia = 1.2  # segundos entre disparos
        self.danio_disparo = 10

        # Movimiento
        self.objetivo_actual = None
        self.tiempo_cambio_objetivo = 0
        self.delay_objetivo = 1200  # ms antes de camboar objetivo

    def llego_a_objetivo(self):
        if self.objetivo_actual is None:
            return True

        objetivo_x, objetivo_y = self.objetivo_actual
        distancia = abs(self.rect.x - objetivo_x) + abs(self.rect.y - objetivo_y)
        return distancia < 40

    def mover(self, segundos_por_frame):
        tiempo_actual = pygame.time.get_ticks()

        # Elegir nuevo objetivo solo cuando se cumple el tiempo
        if self.objetivo_actual is None or (
            self.llego_a_objetivo() and
            tiempo_actual - self.tiempo_cambio_objetivo > self.delay_objetivo
        ):
            self.objetivo_actual = (
                random.randint(60, ANCHO - 60),
                random.randint(40, int(ALTO * 0.45))
            )
            self.tiempo_cambio_objetivo = tiempo_actual

        objetivo_x, objetivo_y = self.objetivo_actual

        # Movimiento hacia el objetivo
        factor = 3 * segundos_por_frame
        self.rect.x += (objetivo_x - self.rect.x) * factor
        self.rect.y += (objetivo_y - self.rect.y) * factor

        # Límites
        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, int(ALTO * 0.5)))

    def disparar(self, grupo_balas):
        tiempo_actual = pygame.time.get_ticks() / 1000  # segundos
        # Control de cadencia
        if tiempo_actual - self.tiempo_ultimo_disparo < self.cadencia:
            return

        self.tiempo_ultimo_disparo = tiempo_actual

        bala = Proyectil(
            x=self.rect.centerx,
            y=self.rect.bottom,
            velocidad_y=300,   # hacia abajo
            danio=self.danio_disparo,
            color=(255, 50, 50),   # rojo enemigo
            ancho=6,
            alto=18
        )

        grupo_balas.add(bala)

    def update(self, segundos_por_frame, grupo_balas_enemigo=None):
        self.mover(segundos_por_frame)
        if grupo_balas_enemigo is not None:
            self.disparar(grupo_balas_enemigo)
