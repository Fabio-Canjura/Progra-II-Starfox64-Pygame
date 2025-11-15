# Este archivo configura los comportamientos de los enemigos
import random
import pygame

from entities.Objetos_Madre import ObjetoJuego
from constantes import ANCHO, ALTO

class Enemigos(ObjetoJuego):
    def __init__(self, ruta_imagen, pos_x, pos_y, velocidad):
        # Llamamos al constructor de la clase base primero
        super().__init__(pos_x, pos_y, imagen=ruta_imagen, tam=(50, 50))
        
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
        self.direccion_x = -2  # Moviento de direccion: -2 = izquierda, 2 = derecha
        self.movimiento_x = 2  # Movimiento constante en el eje X

    def mover(self, segundos_por_frame):
        # Mover enemigo hacia abajo
        self.rect.y = self.rect.y + self.velocidad_aleatoria_y  # Mueve el enemigo hacia abajo

        # Mover enemigo de izquierda a derecha
        self.rect.x += self.direccion_x * self.movimiento_x  # Mueve el enemigo en X

        # Cambiar la dirección cuando llegue a los límites de la pantalla
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
           self.direccion_x *= -1  # Cambiar la dirección al llegar a los límites de la pantalla
        else: 
            self.rect.y += 0.7  # Bajar un espacio en Y cuando toca el borde

        # Eliminar el enemigo o reinciar su poscion
        if self.rect.bottom >= ALTO:
            self.rect.y = 0  # reinicia la posicion del enemigo cuando toca el limite inferior
             #self.kill()  # otra opcion es self.kill que elimina el enemigo cuando llega al límite inferior de la pantalla
        
        # Ajustar límites de movimiento
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)
        limite_superior = ALTO * 0.2
        self.rect.top = max(limite_superior, self.rect.top)
        self.rect.bottom = min(ALTO, self.rect.bottom)
        
    def update(self, segundos_por_frame):
        self.mover(segundos_por_frame)

