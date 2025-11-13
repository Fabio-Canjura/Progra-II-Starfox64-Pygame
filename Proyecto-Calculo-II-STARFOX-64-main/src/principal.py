#Ventana Principal del juego

#Imports necesarios para la conexión entre clases
import pygame
from constantes import ANCHO, ALTO, FPS, NEGRO
from entities.airwing import Arwing
from entities.Enemigos import Enemigos
from fondo import fondo
import os

# Iniciar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("StarFox 2D")
clock = pygame.time.Clock()

#Creación del fondo y dibujar en ventana
ruta_fondo = os.path.join("assets", "images", "backgrounds", "Ciudad arriba.png")
fondo_juego = fondo(ruta_imagen=ruta_fondo, velocidad=120)

# Agrupar los Sprites a dibujar
todos_los_sprites = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()

# Creación de nave Airwing
arwing = Arwing()
todos_los_sprites.add(arwing)

# Creacion de nave enemiga
#ruta_imagen_enemigo = os.path.join("assets", "images", "enemies", "cuadradorojo.png")
#enemigo = Enemigos (pos_x=100, pos_y=50, velocidad=5, ruta_imagen_enemigo) # parametros de prueba
#todos_los_sprites.add(enemigo)


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

    fondo_juego.actualizar(segundos_por_frame)
    todos_los_sprites.update()
    arwing.mover()
    
    # mover los enemigos
    for enemigo in todos_los_sprites:
        if isinstance(enemigo, Enemigos):  # Mover solo los enemigos # hay que modificar la condicion para que se mueva diferente
            enemigo.mover()
            
    fondo_juego.dibujar_en(ventana)
    todos_los_sprites.draw(ventana)
    pygame.display.flip()

pygame.quit()
