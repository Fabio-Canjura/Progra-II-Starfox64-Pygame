#Ventana Principal del juego

#Imports necesarios para la conexión entre clases
import pygame
import random
from constantes import ANCHO, ALTO, FPS, NEGRO
from entities.airwing import Arwing
from entities.Enemigos import Enemigos
from entities.Obstaculos import Obstaculos
from fondo import fondo

import os

# Iniciar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("StarFox 2D")
clock = pygame.time.Clock()
 
#Creación del fondo y dibujar en ventana
ruta_fondo = os.path.join("assets", "images", "backgrounds", "Ciudad_arriba.png")
fondo_juego = fondo(ruta_imagen=ruta_fondo, velocidad=120)

# Agrupar los Sprites a dibujar
todos_los_sprites = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()

# Creación de nave Airwing
arwing = Arwing()
todos_los_sprites.add(arwing)

# Creacion de meteoritos
meteoritos = pygame.sprite.Group() # unir los meteoritos al sprite de pygame

# Creacion de nave enemiga
ruta_imagen_enemigo = os.path.join("Proyecto-Calculo-II-STARFOX-64-main/assets/images/enemies/Enemigo_rojo_no_fondo.png")
enemigo = Enemigos(ruta_imagen=ruta_imagen_enemigo, pos_x= 100, pos_y= 50, velocidad=5)  
todos_los_sprites.add(enemigo)

# Metodo para crear los meteoriotos, pensado a implementarse con random para que vengan y se vayan solos
def crear_meteoritos():
    if random.random() < 0.02:  # Probabilidad de aparición
        # notas para Fabio 
        # Aquí se creo un meteorito usando la clase Obstaculos
        # pos_x: le puse en una posición aleatoria horizontal dentro de la pantalla.
        # pos_y: le puse -40 para que aparezca arriba de la pantalla y caiga hacia abajo. ( calculo robado )
        # velocidad: un numero aleatorio entre 2 y 5 para que algunos caigan más rápido y otros más lento. ( calculo robado )
        # imagen: la imagen es solo de prueba, se puede usar una mejor si la tenemos

        meteorito = Obstaculos(
            pos_x=random.randint(0, ANCHO - 40),
            pos_y=-40,
            velocidad=random.randint(2, 5),
            imagen="Proyecto-Calculo-II-STARFOX-64-main/assets/images/enemies/Asteroid_2_minerals.png"
        )
        meteoritos.add(meteorito)
        todos_los_sprites.add(meteorito)


# Clase borrador de proyectil
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_y=-10, danio=10):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_y = velocidad_y
        self.danio = danio

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

# Bucle principal de la pantalla.
ejecutando = True
while ejecutando:
    segundos_por_frame=clock.tick(FPS) / 1000.0
    #Bucle que obtiene interacción con ventana.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nuevo_proyectil = Proyectil(
                    arwing.rect.centerx,
                    arwing.rect.top,
                    velocidad_y=-15,
                    danio=arwing.armas["disparo_normal"]["danio"]
                )
                grupo_balas.add(nuevo_proyectil)
                todos_los_sprites.add(nuevo_proyectil)


    crear_meteoritos() # se llama la funcion para que este dentro del bucle del juego


    fondo_juego.actualizar(segundos_por_frame)
    todos_los_sprites.update(segundos_por_frame)
    arwing.mover(segundos_por_frame)
    
    # mover los enemigos
    for enemigo in todos_los_sprites:
        if isinstance(enemigo, Enemigos):  # Mover solo los enemigos # hay que modificar la condicion para que se mueva diferente
            enemigo.mover()
    # LLamar los meteoritos
            
    fondo_juego.dibujar_en(ventana)
    todos_los_sprites.draw(ventana)
    pygame.display.flip()

pygame.quit()
