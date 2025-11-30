# Este archivo configura los comportamientos propios del Arwing de Fox McCloud
import pygame
import os
from constantes import (ANCHO, ALTO, POS_INICIO_X, POS_INICIO_Y)
from entities.Objetos_Madre import ObjetoJuego
from entities.proyectiles import Proyectil
from entities.Explosion import Explosion
from entities.iterador_disparos import Iterador_disparos, Iterador_disparos_inverso
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
        self.delegados_disparo = {"disparo_normal": self.disparo_normal,"disparo_doble": self.disparo_doble,"disparo_laser": self.disparo_laser,}

        self.indice_disparo = 0 # Indice del arma actual de la lista.
        self.puede_recibir_dano = True
        self.tiempo_invulnerabilidad = 1300  # 1.3 segundos
        self.tiempo_parpadeo = 100 # parpadeo del airwing luego de recibir daño en milisegundos

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
        self.disparo_actual = self.niveles_disparo[self.indice_disparo]
        
        # Lambdas para acelerar y desacelerar
        self.acelerar = lambda velocidad, segundos_por_frame: min(velocidad + self.potencia_aceleracion * segundos_por_frame, self.velocidad_maxima)

        self.desacelerar = lambda velocidad, segundos_por_frame: max(velocidad - self.potencia_aceleracion * segundos_por_frame, self.velocidad_minima)


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
            }
        }

    # metodo para aplicar la lentitud de la nave al colisionar
    def aplicar_lentitud(self):
        if not self.esta_lenta and self.puede_recibir_dano:
            self.esta_lenta = True
            self.tiempo_lentitud = pygame.time.get_ticks()
            self.velocidad_actual = self.penalizacion_velocidad
             # Evitar múltiples daños en un solo choque
            self.puede_recibir_dano = False
            self.tiempo_ultima_colision = pygame.time.get_ticks()

    def update(self, segundos_por_frame, meteoritos):
        self.tiempo_ultimo_disparo += segundos_por_frame
        # Recuperar velocidad luego del impacto con meteoritos
        if self.esta_lenta:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_lentitud >= self.duracion_lentitud:
                self.esta_lenta = False
                self.velocidad_actual = self.velocidad_base
            
                
        # Invulneravilidad cuando recibe daño
        if not self.puede_recibir_dano:
            tiempo = pygame.time.get_ticks() - self.tiempo_ultima_colision
        
            if tiempo < self.tiempo_invulnerabilidad:
                # alterna la imagen en visible/invisible 
                if (tiempo // self.tiempo_parpadeo) % 2 == 0:
                    self.image.set_alpha(80)   # medio transparente
                else:
                    self.image.set_alpha(255)  # visible
            else:
                # Fin de invulnerabilidad y vuelve a recibir daño
                self.puede_recibir_dano = True
                self.image.set_alpha(255)
        else:
            # Normal sin invulnerabilidad
            self.image.set_alpha(255)
        
        # Mover nave
        self.mover(segundos_por_frame)           


    def mover(self, segundos_por_frame):

        keys = pygame.key.get_pressed()

        # Acelerar tecla A
        if keys[pygame.K_a]:
            self.velocidad_actual = self.acelerar(self.velocidad_actual, segundos_por_frame)
        # Descelerar tecla D
        elif keys[pygame.K_d]:
            self.velocidad_actual = self.desacelerar(self.velocidad_actual, segundos_por_frame)
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


    def crear_bala(self, pos_x, pos_y, arma):
        color = arma["color"]
        velocidad_y = arma["velocidad"]
        danio = arma["danio"]
        ancho, alto = arma["tamanio"]
        bala = Proyectil(
                x=pos_x,
                y=pos_y,
                velocidad_y=velocidad_y,
                danio=danio,
                color=color,
                ancho=ancho,
                alto=alto
            )
        return bala

    def disparo_normal(self, pos_disparo_x, pos_disparo_y):
        arma = self.armas["disparo_normal"]
        bala = self.crear_bala(pos_disparo_x, pos_disparo_y, arma)
        return [bala] 
    
    def disparo_laser(self, pos_disparo_x, pos_disparo_y):
        arma = self.armas["disparo_laser"]
        bala = self.crear_bala(pos_disparo_x, pos_disparo_y, arma)
        return [bala] 
    
    def disparo_doble(self, pos_disparo_x, pos_disparo_y):
        arma = self.armas["disparo_doble"]
        offset = 15 # Separación horizontal de las balas
        bala1 = self.crear_bala(pos_disparo_x - offset, pos_disparo_y, arma)
        bala2 = self.crear_bala(pos_disparo_x + offset, pos_disparo_y, arma)
        return [bala1, bala2]  # lista con dos balas

    #Decorador aplicado a funcion de disparo para generación de powerups
    @registrar_evento("disparos")
    def disparar(self, grupo_balas):
        cadencia = self.armas[self.disparo_actual]["cadencia"]

        # Si no ha pasado el tiempo suficiente no se dispara
        if self.tiempo_ultimo_disparo < cadencia:
            return False   # NO contamos el disparo 

        pos_disparo_x = self.rect.centerx
        pos_disparo_y = self.rect.top
    
        delegado = self.delegados_disparo[self.disparo_actual]
        balas_generadas = delegado(pos_disparo_x, pos_disparo_y)
    
        for bala in balas_generadas:
                grupo_balas.add(bala)
    
        # Reiniciar el temporizador de disparo
        self.tiempo_ultimo_disparo = 0
        return True  # Contar el disparo
    
    def mejorar_disparo(self):
        iterador = Iterador_disparos(self.niveles_disparo, self.indice_disparo+1)
        try:
            self.disparo_actual = next(iterador)
            self.indice_disparo += 1
        except StopIteration:
            pass  # Ya está en el nivel máximo, no hacer nada
                
    def degradar_disparo(self):
        iterador = Iterador_disparos_inverso(self.niveles_disparo, self.indice_disparo - 1)
        try:
            self.disparo_actual = next(iterador)
            self.indice_disparo -= 1
        except StopIteration:
            pass  # Ya está en el nivel mínimo
            
    # Método para recibir daño
    def recibir_dano(self, cantidad):
        # si está en invulnerabilidad, ignorar el daño
        if not self.puede_recibir_dano:
            return

        # Aplicar daño a la salud
        self.salud -= cantidad
    
        # Degradar disparo al recibir daño
        self.degradar_disparo()
    
        # Activar invulnerabilidad y parpadeo
        self.puede_recibir_dano = False
        self.tiempo_ultima_colision = pygame.time.get_ticks()
    
        # Si muere, explota
        if self.salud <= 0:
            self.explotar()


    # Método para eliminar la nave
    def explotar(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        #todos_los_sprites.add(explosion)
        self.kill()
