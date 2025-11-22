# Este archivo configura los comportamientos propios del Arwing de Fox McCloud
import pygame
import os
from constantes import (ANCHO, ALTO, POS_INICIO_X, POS_INICIO_Y)
from entities.Objetos_Madre import ObjetoJuego
from entities.proyectiles import Proyectil
from entities.Explosion import Explosion
from decorador import registrar_evento


class Arwing(ObjetoJuego):

    def __init__(self):
        # Llamamos al constructor de la clase base
        super().__init__(pos_x=POS_INICIO_X, pos_y=POS_INICIO_Y)
        # Configuraciones del Airwing
        self.disparos_para_powerup = 25 # Cantidad de disparos para generar un objeto powerup
        self.estadisticas = {}
        self.salud = 100
        self.velocidad_base = 180
        self.velocidad_actual = self.velocidad_base
        self.velocidad_maxima = 350   # Aceleración
        self.velocidad_minima = 150    # Desaceleración
        self.potencia_aceleracion = 300 # Para acelerar paulatinamente
        self.niveles_disparo = ["disparo_normal", "disparo_doble", "disparo_laser"] # Para intercambiar disparos al coger powerup
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

        # Estado de lentitud por colisión con meteoritos
        self.esta_lenta = False
        self.tiempo_lentitud = 0
        self.duracion_lentitud = 1500  # milisegundos (1.5 segundos)
        self.penalizacion_velocidad = 120  # velocidad cuando está lenta    

        #  Valores para disparar
        self.cargar_disparo = True
        self.tiempo_ultimo_disparo = 0  # Acumulador de tiempo para cálculo entre disparos 
        self.danio_disparo = 10         # Daño base del disparo
        self.disparo_actual = "disparo_normal"

        # Diccionario de armas del airwing
        self.armas = {
            "disparo_normal": {
                "color": (0, 255, 255),  # Azul celeste
                "velocidad": -600,
                "danio": 10,
                "tamanio": (6, 18),
                "cantidad_balas": 1,
                "cadencia": 0.20
            },
            "disparo_doble": {
                "color": (0, 255, 0),  # Verde
                "velocidad": -650,
                "danio": 12,
                "tamanio": (6, 20),
                "cantidad_balas": 2,
                "cadencia": 0.30
            },
            "disparo_laser": {
                "color": (255, 50, 50),  # Rojo brillante
                "velocidad": -700,
                "danio": 15,
                "tamanio": (7, 22),
                "cantidad_balas": 1,
                "cadencia": 0.40
            },
            "disparo_cargado": {
                "color": (0, 255, 100),  # Bomba verde al cargar
                "velocidad": -500,
                "danio": 40,
                "tamanio": (4, 45),
                "explosion_radio": 50,
                "cantidad_balas": 1,
                "cadencia": 0.50
            }
        }


    # metodo para aplicar la lentitud de la nave al colisionar
    def aplicar_lentitud(self):
        if not self.esta_lenta:
            self.esta_lenta = True
            self.tiempo_lentitud = pygame.time.get_ticks()
            self.velocidad_actual = self.penalizacion_velocidad

    def update(self, segundos_por_frame, meteoritos):
        self.tiempo_ultimo_disparo += segundos_por_frame
        # Recuperar velocidad luego del impacto con meteoritos
        if self.esta_lenta:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_lentitud >= self.duracion_lentitud:
                self.esta_lenta = False
                self.velocidad_actual = self.velocidad_base

        # Detectar colisión con meteoritos
        colisiones = pygame.sprite.spritecollide(self, meteoritos, False)
        """
        # prints para detectar si hay colisiones // esto es temporal
        print("Arwing rect:", self.rect)
        for m in meteoritos:
            print("Meteorito rect:", m.rect)

        if colisiones:
            print("///  COLISIÓN DETECTADA!")
            self.aplicar_lentitud()
        """
        
        # Mover nave
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


    #Decorador aplicado a funcion de disparo para generación de powerups
    @registrar_evento("disparos")
    def disparar(self, grupo_balas):

        cadencia = self.armas[self.disparo_actual]["cadencia"]

        # Si no ha pasado el tiempo suficiente no se dispara
        if self.tiempo_ultimo_disparo < cadencia:
            return False   # NO contamos el disparo (evento)

        disparo = self.armas[self.disparo_actual]

        vel_y = disparo["velocidad"]
        danio = disparo["danio"]
        ancho, alto = disparo["tamanio"]
        cantidad = disparo["cantidad_balas"]

        x_base = self.rect.centerx
        y_base = self.rect.top

        if cantidad == 1:
            bala = Proyectil(
                x=x_base, y=y_base,
                velocidad_y=vel_y, danio=danio,
                color=disparo["color"], ancho=ancho, alto=alto
            )
            grupo_balas.add(bala)

        elif cantidad == 2:
            offset = 15
            bala_izq = Proyectil(
                x=x_base - offset, y=y_base,
                velocidad_y=vel_y, danio=danio,
                color=disparo["color"], ancho=ancho, alto=alto
            )
            bala_der = Proyectil(
                x=x_base + offset, y=y_base,
                velocidad_y=vel_y, danio=danio,
                color=disparo["color"], ancho=ancho, alto=alto
            )
            grupo_balas.add(bala_izq, bala_der)

        # Reiniciar el temporizador
        self.tiempo_ultimo_disparo = 0

        return True  # Contar el disparo



    # Método para recibir daño
    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.explotar()

    # Método para eliminar la nave
    def explotar(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        #todos_los_sprites.add(explosion)
        self.kill()
