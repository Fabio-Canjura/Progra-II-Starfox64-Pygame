# en esta clase estaran todos los obstaculos del mapa

import random


class Obstaculos(ObjetoJuego):

    def __init__(self, pos_x, pos_y, velocidad, imagen):
        super().__init__(pos_x, pos_y, velocidad, imagen)

        # configuracion de caida de los objetos

        self.veloc_caida_y = velocidad
        self.rect.y = random.randint(-100, -40)  # Aparece fuera de la pantalla en la parte superior

    
    def update(self, dt):
        # Mover el meteorito hacia abajo
        self.rect.y = self.rect.y + self.velocidad_y  # Mueve el meteorito hacia abajo
        
        # Si el meteorito toca el borde inferior, eliminarlo // logica factiable a cambiar
        if self.rect.top >= ALTO:
            self.kill()  # Elimina el meteorito cuando se sale de la pantalla    

    # Metodo para crear los meteoriotos, pensado a implementarse con random para que vengan y se vayan solos
    # def crear_meteoritos(): 