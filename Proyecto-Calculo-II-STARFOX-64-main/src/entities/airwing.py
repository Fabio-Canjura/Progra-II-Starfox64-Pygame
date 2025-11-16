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
        self.cargar_disparo = True
        self.cadencia_disparo = 0.0    # 5 disparos * segundo
        self.tiempo_ultimo_disparo = 0  #Acumulador de tiempo para calculo entre disparos 
        self.danio_disparo = 10         # daño base del disparo
        self.disparo_actual = "disparo_laser"
        #Diccionario de armas del airwing
        self.armas = {
                "disparo_normal": {
                        "color": (0, 255, 255),   # azul celeste
                        "velocidad": -600,
                        "danio": 10,
                        "tamanio": (6, 18),
                        "cantidad_balas": 1,
                        "cadencia": 0.20
                            },
                "disparo_doble": {
                        "color": (0, 255, 0),     # verde
                        "velocidad": -650,
                        "danio": 12,
                        "tamanio": (6, 20),
                        "cantidad_balas": 2,
                        "cadencia": 0.30
                            },
                "disparo_laser": {
                        "color": (255, 50, 50),   # Rojo brillante
                        "velocidad": -700,
                        "danio": 15,
                        "tamanio": (7, 22),
                        "cantidad_balas": 1,
                        "cadencia": 0.40
                            },
                "disparo_cargado": {
                        "color": (0, 255, 100),   # bomba verde al cargar
                        "velocidad": -500,
                        "danio": 40,
                        "tamanio": (4, 45),
                        "explosion_radio": 50,
                        "cantidad_balas": 1,
                        "cadencia": 0.50
                            }
                        }

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
        cadencia_disparo = self.armas[self.disparo_actual]["cadencia"] #Obtener la cadencia de disparo del arma actual
        if self.tiempo_ultimo_disparo < cadencia_disparo:
            return  # Tiempo de espera entre disparos 

        disparo = self.armas[self.disparo_actual]

        # Parámetros desde diccionario
        vel_y = disparo["velocidad"]
        danio = disparo["danio"]
        ancho, alto = disparo["tamanio"]
        cantidad = disparo["cantidad_balas"]

        # Posición base (centro del Arwing)
        x_base = self.rect.centerx
        y_base = self.rect.top

        # Disparo a utilizar
        if cantidad == 1:
            # Un solo proyectil
            bala = Proyectil(
                x=x_base,
                y=y_base,
                velocidad_y=vel_y,
                danio=danio,
                color=disparo["color"],
                ancho=ancho,
                alto=alto
            )
            grupo_balas.add(bala)

        elif cantidad == 2:
            offset = 15  # separación horizontal entre los dos láseres

            bala_izq = Proyectil(
                x=x_base - offset,
                y=y_base,
                velocidad_y=vel_y,
                danio=danio,
                color=disparo["color"],
                ancho=ancho,
                alto=alto
            )

            bala_der = Proyectil(
                x=x_base + offset,
                y=y_base,
                velocidad_y=vel_y,
                danio=danio,
                color=disparo["color"],
                ancho=ancho,
                alto=alto
            )

            grupo_balas.add(bala_izq, bala_der)

        # Disparo cargado
        if self.disparo_actual == "disparo_cargado":
            # Añadir efecto de explosión 
            pass

        # Reinicio del tiempo del ultimo disparo
        self.tiempo_ultimo_disparo = 0

    # Método para recibir daño
    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.explotar()

    # Método para eliminar la nave
    def explotar(self):
        self.kill()
