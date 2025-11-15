# en esta clase estaran todos los obstaculos del mapa

import random
import pygame
from constantes import ALTO
from entities.Objetos_Madre import ObjetoJuego

class Obstaculos(ObjetoJuego):

    def __init__(self, pos_x, pos_y, velocidad, ruta_imagen):
        super().__init__(pos_x, pos_y, imagen=ruta_imagen, tam=(40, 40))

        # configuracion de caida de los objetos
        self.veloc_caida_y = velocidad
        #Aparece en parte superior de pantalla
        self.rect.y = random.randint(-100, -40)  

    
    def update(self, dt): #dt = delta time
        
        self.rect.y = self.rect.y + self.veloc_caida_y  # Mueve el meteorito hacia abajo
        
        # Si el meteorito toca el borde inferior, eliminarlo // logica factiable a cambiar
        if self.rect.top >= ALTO:
            self.kill()  # Elimina el meteorito cuando se sale de la pantalla    

 
            