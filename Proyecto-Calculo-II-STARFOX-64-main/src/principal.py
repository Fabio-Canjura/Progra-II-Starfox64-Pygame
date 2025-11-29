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
from entities.meteoritos import OrquestrarMeteoritos
from Recursiva import contar_recursivo


import os

# Iniciar Pygame
pygame.init()
pygame.mixer.init() #Iniciar ost del juego
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("StarFox 2D")
clock = pygame.time.Clock()

#Creación del fondo y dibujar en ventana
ruta_fondo = os.path.join("assets", "images", "backgrounds", "Espacio_exterior_1.png")
fondo_juego = fondo(ruta_imagen=ruta_fondo, velocidad=120)

# Agrupar los Sprites a dibujar
todos_los_sprites = pygame.sprite.Group()
grupo_balas_arwing = pygame.sprite.Group()
grupo_balas_enemigo = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()


# Creación de nave Airwing
arwing = Arwing()
todos_los_sprites.add(arwing)

# Creacion de meteoritos
gestor_meteoritos = OrquestrarMeteoritos() # unir los meteoritos al sprite de pygame
meteoritos = pygame.sprite.Group()

#Creación de powerups
grupo_powerups = pygame.sprite.Group()

# Creacion de nave enemiga

ruta_imagen_enemigo = os.path.join("assets", "images", "enemies", "Enemigo_rojo_no_fondo.png")
enemigo = Enemigos(ruta_imagen=ruta_imagen_enemigo, pos_x= 100, pos_y= 50, velocidad=5)  
todos_los_sprites.add(enemigo)
grupo_enemigos.add(enemigo)


# Metodo para detectar la colision de la nave
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

    # color según el estado de vida
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

def reproducir_musica_inicio():
    ruta_musica = os.path.join("assets", "audio","Fondos audio", "StarFox_title_ost.mp3")
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)

def reproducir_musica_juego():
    ruta_musica = os.path.join("assets", "audio","Fondos audio", "space_sound.mp3")
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)
    

# Metodo para crear la pantalla de inicio
def pantalla_inicio():
    ejecutando_inicio = True

    # Cargar fondo de pantalla de inicio
    ruta_fondo_start = os.path.join("assets", "images", "backgrounds", "pantalla_inicio_1.png")

    try:
        fondo_start = pygame.image.load(ruta_fondo_start)
        fondo_start = pygame.transform.scale(fondo_start, (ANCHO, ALTO))
    except:
        
        fondo_start = pygame.Surface((ANCHO, ALTO))
        fondo_start.fill((0, 0, 50))

    # Fuente del texto 
    fuente = pygame.font.Font(None, 48) 

    while ejecutando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ejecutando_inicio = False

        # Dibujar fondo
        ventana.blit(fondo_start, (0, 0))

        
        texto = fuente.render("PRESIONA ENTER PARA INICIAR", True, (255, 255, 255))

        texto_rect = texto.get_rect(center=(ANCHO // 2, int(ALTO * 0.80)))
        ventana.blit(texto, texto_rect)

        pygame.display.update()

# activar musica pantalla de inicio
reproducir_musica_inicio()

# llamar a la pantalla de inicio
pantalla_inicio()

# Cambiar música a la del juego
ruta = os.path.join("assets", "audio","Fondos audio", "space_sound.mp3")
pygame.mixer.music.load(ruta)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)


# Bucle principal del juego.
ejecutando = True
while ejecutando:
    segundos_por_frame = clock.tick(FPS) / 1000
    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False  

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                resultado = arwing.disparar(grupo_balas_arwing)
                for bala in grupo_balas_arwing:
                    if bala not in todos_los_sprites:
                        todos_los_sprites.add(bala)

                # PowerUp
                if arwing.estadisticas.get("disparos", 0) >= 25:
                    arwing.estadisticas["disparos"] = 0
                    crear_powerup()

    #Creación de meteoritos
    nuevo_meteorito = gestor_meteoritos.intentar_generar()
    if nuevo_meteorito:
        meteoritos.add(nuevo_meteorito)
        todos_los_sprites.add(nuevo_meteorito)
 
    # Actualización general de los elementos en pantalla
    arwing.update(segundos_por_frame, meteoritos)
    meteoritos.update(segundos_por_frame)
    grupo_balas_arwing.update(segundos_por_frame)
    grupo_balas_enemigo.update(segundos_por_frame)
    enemigo.update(segundos_por_frame, grupo_balas_enemigo)
    grupo_powerups.update(segundos_por_frame)

    # Conteo recursivo de meteoritos y enemigos en pantalla
    cantidad_meteoritos = contar_recursivo(list(meteoritos))
    cantidad_enemigos = contar_recursivo(list(grupo_enemigos))

    
    # Colisión de Arwing con powerups para mejora disparo
    colision_powerups = pygame.sprite.spritecollide(arwing, grupo_powerups, True)
    for powerup in colision_powerups:
        if powerup.tipo == "mejora_disparo":
            arwing.mejorar_disparo()
    
    # colision de balas, arwing recibe dano        
    colision_balas_enemigas = pygame.sprite.spritecollide(arwing, grupo_balas_enemigo, True)
    for bala in colision_balas_enemigas:
        arwing.recibir_dano(bala.danio)            

    # colision de balas, enemigo recibe dano
    colision_balas_jugador = pygame.sprite.spritecollide(enemigo, grupo_balas_arwing, True)
    for bala in colision_balas_jugador:
        try:
            enemigo.recibir_dano(bala.danio)
        except:
            pass

    # si el enemigo murio no dispara mas
    if not enemigo.alive():
        grupo_balas_enemigo.empty()  


    # Colisiones de meteoritos con nave
    if detectar_colision_nave_meteoritos(arwing, meteoritos) and arwing.puede_recibir_dano:
        arwing.aplicar_lentitud()
        arwing.degradar_disparo()
        
    # Carga de sprites en la pantalla de juego
    fondo_juego.actualizar(segundos_por_frame)
    fondo_juego.dibujar_en(ventana)

    todos_los_sprites.draw(ventana)
    grupo_balas_arwing.draw(ventana)
    grupo_balas_enemigo.draw(ventana)
    # barra de vida
    dibujar_barra_vida(ventana, ANCHO - 70, ALTO - 30, arwing.salud, 100)
    #fuente de texto
    fuente = pygame.font.Font(None, 26)

    # mostrar meteoritos en pantalla
    texto_mete = fuente.render(f"Meteoritos: {cantidad_meteoritos}", True, (255, 255, 255))
    ventana.blit(texto_mete, (10, 10))

    # mostrar enemigos en pantalla
    texto_enem = fuente.render(f"Enemigos: {cantidad_enemigos}", True, (255, 255, 255))
    ventana.blit(texto_enem, (10, 40))

    pygame.display.flip()

pygame.quit()
 