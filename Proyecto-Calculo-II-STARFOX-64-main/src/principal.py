#Ventana Principal del juego

#Imports necesarios para la conexión entre clases
import pygame
import random
from constantes import ANCHO, ALTO, FPS, NEGRO
from entities.airwing import Arwing
from entities.Enemigos import Enemigos
from entities.Obstaculos import Obstaculos
from fondo import fondo
from entities.power_up import power_up

import os

# Iniciar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("StarFox 2D")
clock = pygame.time.Clock()
 
#Creación del fondo y dibujar en ventana
ruta_fondo = os.path.join("assets", "images", "backgrounds", "Espacio_exterior_1.png")
fondo_juego = fondo(ruta_imagen=ruta_fondo, velocidad=120)

# Agrupar los Sprites a dibujar
todos_los_sprites = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()

# Creación de nave Airwing
arwing = Arwing()
todos_los_sprites.add(arwing)

# Creacion de meteoritos
meteoritos = pygame.sprite.Group() # unir los meteoritos al sprite de pygame

#Creación de powerups
grupo_powerups = pygame.sprite.Group()

# Creacion de nave enemiga
ruta_imagen_enemigo = os.path.join("assets", "images", "enemies", "Enemigo_rojo_no_fondo.png")
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

        ruta_imagen_meteorito = os.path.join("assets", "images", "enemies", "Asteroid_2_minerals.png")
        meteorito = Obstaculos(pos_x=random.randint(0, ANCHO - 40), pos_y=-40, velocidad=random.randint(2, 5),ruta_imagen=ruta_imagen_meteorito)
        meteoritos.add(meteorito)
        todos_los_sprites.add(meteorito)

# Meotodo para detectar la colision de la nave
def detectar_colision_nave_meteoritos(nave, grupo_meteoritos):
    colisiones = pygame.sprite.spritecollide(nave, grupo_meteoritos, False)
    if colisiones:
        return True
    return False

def crear_powerup():
    mejora = power_up(tipo="mejora_disparo")
    grupo_powerups.add(mejora)
    todos_los_sprites.add(mejora)

# Crear la barra de vida 
def dibujar_barra_vida(pantalla, x, y, vida, vida_maxima):
    ancho = 100
    alto = 10

    # porcentaje de vida
    ratio = vida / vida_maxima
    vida_actual = int(ancho * ratio)

    # color según el estado
    if ratio > 0.6:
        color = (0, 255, 0)      # verde
    elif ratio > 0.3:
        color = (255, 255, 0)    # amarillo
    else:
        color = (255, 0, 0)      # rojo

    # borde de la barra
    pygame.draw.rect(pantalla, (255,255,255), (x, y, ancho, alto), 1)
    # barra de vida
    pygame.draw.rect(pantalla, color, (x, y, vida_actual, alto))

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
                resultado = arwing.disparar(grupo_balas)
                #Momentaneo para verificar si se cuentan los disparos 
                print("🔵 DISPAROS REGISTRADOS:", arwing.estadisticas.get("disparos", 0))
                for bala in grupo_balas:
                    if bala not in todos_los_sprites:
                        todos_los_sprites.add(bala)
                
                # Verificar si se debe generar powerup
                if arwing.estadisticas.get("disparos", 0) >= 25:
                    print("💫 Se generó un PowerUp por 25 disparos!")
                    arwing.estadisticas["disparos"] = 0  # Reiniciar contador
                    crear_powerup()


    crear_meteoritos() # se llama la funcion para que este dentro del bucle del juego

     # Actualizamos la nave del jugador. Le pasamos el tiempo del frame y los meteoritos para que pueda detectar choques.
    arwing.update(segundos_por_frame, meteoritos)

    # Actualizamos TODOS los meteoritos. Solo necesitan saber cuánto duró el frame para moverse.
    meteoritos.update(segundos_por_frame)

    # Actualizamos las balas. Estas solo se mueven hacia arriba, no ocupan el tiempo del frame. Da error si no se colocan xD
    grupo_balas.update(segundos_por_frame)

    # Actualizamos al enemigo. También usa el tiempo del frame para moverse de forma más suave.
    enemigo.update(segundos_por_frame)
    
    # deteccion de colisiones
    if detectar_colision_nave_meteoritos(arwing, meteoritos):
        arwing.aplicar_lentitud()


    fondo_juego.actualizar(segundos_por_frame)
    
    """
    # mover los enemigos
    for enemigo in todos_los_sprites:
        if isinstance(enemigo, Enemigos):  # Mover solo los enemigos # hay que modificar la condicion para que se mueva diferente
            enemigo.mover()
    # LLamar los meteoritos
    """
            
    fondo_juego.dibujar_en(ventana)
    todos_los_sprites.draw(ventana)

    # Dibujar la barra de vida en la esquina inferior derecha
    dibujar_barra_vida(ventana,ANCHO - 70,ALTO - 30,arwing.salud,100)

    pygame.display.flip()

pygame.quit()
