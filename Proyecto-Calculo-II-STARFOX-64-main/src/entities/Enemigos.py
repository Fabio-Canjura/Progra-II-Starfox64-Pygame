# Este archivo configura los comportamientos de los enemigos
import random
import pygame

from entities.Objetos_Madre import ObjetoJuego
from constantes import ANCHO, ALTO
from entities.proyectiles import Proyectil


class Enemigos(ObjetoJuego):
    def __init__(self, ruta_imagen, pos_x, pos_y, velocidad):
        # Llamamos al constructor de la clase base primero
        super().__init__(pos_x, pos_y, imagen=ruta_imagen, tam=(50, 50))

        #Vida del enemigo

        self.vida = 100

        # Variables de danio
        self.tiempo_ultimo_disparo = 0
        self.cadencia = 1.2   # segundos entre disparos
        self.danio_disparo = 10

        self.objetivo_actual = None
        self.tiempo_cambio_objetivo = 0
        self.delay_objetivo = 1200  # 1.2 segundos antes de elegir nuevo objetivo
        
        # Cargar la imagen del enemigo
        self.image = pygame.image.load(ruta_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajustar tamaño de la imagen

        # Establecer la posición de rect después de cargar la imagen
        self.rect = self.image.get_rect()  # Inicializar rect de la imagen
        self.rect.x = ANCHO // 2  # Centrado en el eje X
        self.rect.y = ALTO // 100  # pixeles desde la parte inferior de la pantalla

        # Atributos específicos para el enemigo
        self.velocidad = velocidad
        self.velocidad_aleatoria_y = 0  # velocidad de caida en eje y

        #Movimiento en X,

        self.objetivo_actual = None

    # metodo para recibir dano
    
    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.kill()

    # Metodo para que enemigo dispare

    def disparar(self, grupo_balas):
        tiempo_actual = pygame.time.get_ticks() / 1000  # convertir a segundos

        if tiempo_actual - self.tiempo_ultimo_disparo < self.cadencia:
            return
        # control de cadencia de disparo enemigo
        self.tiempo_ultimo_disparo = tiempo_actual

        # Crear proyectil
        bala = Proyectil(
            x=self.rect.centerx,
            y=self.rect.bottom,
            velocidad_y=300,   # hacia abajo
            danio=self.danio_disparo,
            color=(255, 50, 50),   # rojo enemigo
            ancho=6,
            alto=18)

        grupo_balas.add(bala)

    def _llego_a_objetivo(self):
        if self.objetivo_actual is None:
            return True

        objetivo_x, objetivo_y = self.objetivo_actual
        distancia = abs(self.rect.x - objetivo_x) + abs(self.rect.y - objetivo_y)
        return distancia < 40 
    
    def mover(self, segundos_por_frame):

        tiempo_actual = pygame.time.get_ticks()

        # elegir nuevo objetivo solo cuando toca
        if self.objetivo_actual is None or (
            self._llego_a_objetivo() and 
            tiempo_actual - self.tiempo_cambio_objetivo > self.delay_objetivo
        ):
            self.objetivo_actual = (
                random.randint(60, ANCHO - 60),
                random.randint(40, int(ALTO * 0.45))
            )
            self.tiempo_cambio_objetivo = tiempo_actual

        objetivo_x, objetivo_y = self.objetivo_actual

        # mvimiento del enemigo
        factor = 3 * segundos_por_frame 
        self.rect.x += (objetivo_x - self.rect.x) * factor
        self.rect.y += (objetivo_y - self.rect.y) * factor

        # Limites
        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, int(ALTO * 0.5)))   

    def update(self, segundos_por_frame, grupo_balas_enemigo):
        self.mover(segundos_por_frame)
        self.disparar(grupo_balas_enemigo)

