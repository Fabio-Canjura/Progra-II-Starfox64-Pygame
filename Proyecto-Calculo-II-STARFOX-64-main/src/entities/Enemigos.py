# Este archivo configura los comportamientos de los enemigos/obstaculos
import random
import pygame

from entities.Objetos_Madre import ObjetoJuego

class Enemigos(ObjetoJuego):
    def __init__(self, pos_x, pos_y, velocidad, imagen= "assets/images/enemies/cuadrorojo.png"):
        # Llamamos al constructor de la clase base
        super().__init__(pos_x, pos_y, vida_inicial=100, imagen=imagen, tam=(50, 50))
        
        # Atributos para los enemigos

        self.velocidad = velocidad  # Velocidad de movimiento de los enemigos

        # cargar la imagen del enemigo ( temporal para pruebas )

        self.image = pygame.image.load("assets/images/enemies/cuadrorojo.png").convert_alpha()

        # movimiento aleatorio de las naves

        self.velocidad_aleatoria_y = random.randint(1,3) # rango de velocidad aleatoria en el eje Y
        self.movimiento_x = random.randint(-2, 2)  # movimiento aleatorio en el eje X (-2 a 2 píxeles por fotograma)


    #Metodo para dictar el movimiento de las naves enemigas
    def mover (self):
     
        self.rect.y = self.rect.y + self.velocidad_aleatoria_y # mover enemigo en eje y aleatoreamente

        self.rect.x = self.rect.x + self.movimiento_x # mover enemigo en el eje x aleatoreamente

        # ajustar limites de movimiento en el mapa
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)
        limite_superior = ALTO * 0.2
        self.rect.top = max(limite_superior, self.rect.top)
        self.rect.bottom = min(ALTO, self.rect.bottom)