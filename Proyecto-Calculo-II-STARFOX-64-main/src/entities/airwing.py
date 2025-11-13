# Este archivo configura los comportamientos propios del Arwing de Fox McCloud
import pygame
import os
from constantes import (
    ANCHO, ALTO, POS_INICIO_X, POS_INICIO_Y,
    vida_inicial_airwing, velocidad_inicial_airwing, velocidad_maxima_airwing,
    aceleracion, danio_disparo_normal
)
from entities.Objetos_Madre import ObjetoJuego


class Arwing(ObjetoJuego):

    def __init__(self):
        super().__init__(pos_x=POS_INICIO_X, pos_y=POS_INICIO_Y, vida_inicial=vida_inicial_airwing)
        # Cargar sprite real del Airwing
        ruta_airwing = os.path.join("assets", "images", "player", "nave_fox.png")
        try:
            self.image = pygame.image.load(ruta_airwing).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except Exception as e:
            print("Error al cargar sprite del Arwing, usando placeholder.")
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))
            
        #self.rect = self.image.get_rect(center=(POS_INICIO_X, POS_INICIO_Y))
        
        # atributo para la vida del Airwing 
        self.salud = vida_inicial_airwing

        # Atributos de modificación propios de movimiento.
        self.velocidad_actual = velocidad_inicial_airwing
        self.aceleracion = aceleracion

       # ESTA ES LA QUE IMPORTA:
    def update(self, segundos_por_frame):
        self.mover(segundos_por_frame)

    # Movimiento del Arwing
    def mover(self, segundos_por_frame):
        keys = pygame.key.get_pressed()
        desplazamiento = int(self.velocidad_actual * segundos_por_frame)
        if keys[pygame.K_LEFT]:
            self.rect.x -= desplazamiento
        if keys[pygame.K_RIGHT]:
            self.rect.x += desplazamiento
        if keys[pygame.K_UP]:
            self.rect.y -= desplazamiento
        if keys[pygame.K_DOWN]:
            self.rect.y += desplazamiento

        # Limitar dentro de pantalla
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)
        limite_superior = ALTO * 0.2
        self.rect.top = max(limite_superior, self.rect.top)
        self.rect.bottom = min(ALTO, self.rect.bottom)

    # Disparo con control de cadencia
    def disparar(self, grupo_balas):
        tiempo_actual = pygame.time.get_ticks()
        laser = self.armas["disparo_normal"]
        intervalo_disparo = 1000 / laser["cadencia_max"]

        if tiempo_actual - self.tiempo_ultimo_disparo > intervalo_disparo:
            # Placeholder, se cargara luego el sprite de disparo.
            self.tiempo_ultimo_disparo = tiempo_actual


    # Metodo para recibir dano
    def recibir_dano(self, dano):
        self.salud = self.salud - dano # Resta el daño a la salud
        if self.salud <= 0:
            self.explotar() # explota cuando salud < 0

    # Metodo para eliminar naves al morir
    def explotar(self):
        # Nota: hay que cargar la animacion cuando explota
        self.kill() # metodo de pygames que elimina el sprite del grupo de sprites

    # Metodo para reducir velocidad al colisionar