# Ventana Principal del juego

# Imports necesarios para la conexión entre clases
import pygame
import os

from constantes import ANCHO, ALTO, FPS
from entities.airwing import Arwing
from entities.Orquestrador_hostiles import OrquestadorHostiles
from entities.Contador_Partidas import Contador_Partidas


from fondo import fondo
from entities.power_up import power_up
from Recursiva import contar_recursivo
from entities.Logros import SistemaLogros


# Iniciar Pygame
pygame.init()
pygame.mixer.init()  # Iniciar ost del juego
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Programación II StarFox 2D")
clock = pygame.time.Clock()

# Creación del fondo y dibujar en ventana
ruta_fondo = os.path.join("assets", "images", "backgrounds", "Espacio_exterior_1.png")
fondo_juego = fondo(ruta_imagen=ruta_fondo, velocidad=120)

# Agrupar los Sprites a dibujar
todos_los_sprites = pygame.sprite.Group()
grupo_balas_arwing = pygame.sprite.Group()
grupo_balas_enemigo = pygame.sprite.Group()

# Grupos específicos de hostiles
meteoritos = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()

# Crear sistema de logros
sistema_logros = SistemaLogros()

# crear contador de partidas
contador_partidas = Contador_Partidas()

# Creación de nave Airwing
arwing = Arwing(sistema_logros) # agregar los logros al arwing
todos_los_sprites.add(arwing)

# Creación del orquestrador del nivel
orquestador = OrquestadorHostiles(grupo_enemigos)

# Creación de powerups
grupo_powerups = pygame.sprite.Group()

def crear_powerup():
    mejora = power_up()
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
    pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho, alto), 1)
    # barra de vida
    pygame.draw.rect(pantalla, color, (x, y, vida_actual, alto))

def reproducir_musica_inicio():
    ruta_musica = os.path.join("assets", "audio", "Fondos audio", "StarFox_title_ost.mp3")
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)

def reproducir_musica_juego():
    ruta_musica = os.path.join("assets", "audio", "Fondos audio", "space_sound.mp3")
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
        
# Pantalla de muerte

def pantalla_muerte(): 
    ejecutando_muerte = True

    ruta_fondo_muerte = os.path.join("assets", "images", "backgrounds", "pantalla_muerte.png")

    try:
        fondo_muerte = pygame.image.load(ruta_fondo_muerte)
        fondo_muerte = pygame.transform.scale(fondo_muerte, (ANCHO, ALTO))
    except:
        fondo_muerte = pygame.Surface((ANCHO, ALTO))
        fondo_muerte.fill((20, 0, 0))

    fuente_texto = pygame.font.Font(None, 40)

    # Registrar derrota
    contador_partidas.registrar_derrota()

    while ejecutando_muerte:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "reiniciar"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        ventana.blit(fondo_muerte, (0, 0))

        # Mensajes en pantalla
        mensaje1 = fuente_texto.render("ENTER para reiniciar", True, (255, 255, 255))
        mensaje2 = fuente_texto.render("ESC para salir", True, (200, 200, 200))

        mensaje1_rect = mensaje1.get_rect(center=(ANCHO // 2, int(ALTO * 0.70)))
        mensaje2_rect = mensaje2.get_rect(center=(ANCHO // 2, int(ALTO * 0.80)))

        ventana.blit(mensaje1, mensaje1_rect)
        ventana.blit(mensaje2, mensaje2_rect)

        
        # mensaje del contador de derrotas
        contador_texto = fuente_texto.render(contador_partidas.texto(), True, (255,255,255))
        ventana.blit(contador_texto, (10, 10))

        pygame.display.update()

def pantalla_victoria(): 
    ejecutando_victoria = True

    ruta_fondo_victoria = os.path.join("assets", "images", "player", "Pantalla_Victoria.png")
    try:
        fondo_victoria = pygame.image.load(ruta_fondo_victoria)
        fondo_victoria = pygame.transform.scale(fondo_victoria, (ANCHO, ALTO))
    except:
        fondo_victoria = pygame.Surface((ANCHO, ALTO))
        fondo_victoria.fill((0, 40, 0))

    fuente_texto = pygame.font.Font(None, 50)

    # Registrar victoria
    contador_partidas.registrar_victoria()

    while ejecutando_victoria:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "reiniciar"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        ventana.blit(fondo_victoria, (0, 0))

        mensaje_vic1 = fuente_texto.render("¡VICTORIA!", True, (255, 215, 0))
        mensaje_vic2 = fuente_texto.render("ENTER para jugar otra vez", True, (255, 255, 255))
        mensaje_vic3 = fuente_texto.render("ESC para salir", True, (200, 200, 200))

        ventana.blit(mensaje_vic1, mensaje_vic1.get_rect(center=(ANCHO // 2, int(ALTO * 0.75))))
        ventana.blit(mensaje_vic2, mensaje_vic2.get_rect(center=(ANCHO // 2, int(ALTO * 0.82))))
        ventana.blit(mensaje_vic3, mensaje_vic3.get_rect(center=(ANCHO // 2, int(ALTO * 0.90))))

        # mensaje del contador de victorias
        contador_texto = fuente_texto.render(contador_partidas.texto(), True, (255,255,255))
        ventana.blit(contador_texto, (10, 10))

        pygame.display.update()

# activar musica pantalla de inicio
reproducir_musica_inicio()

# llamar a la pantalla de inicio
pantalla_inicio()

# Cambiar música a la del juego
reproducir_musica_juego()

# Contador de meteoritos eliminados para el sistema de logros
meteoritos_destruidos = 0

# Bucle principal del juego.
ejecutando = True
while ejecutando:
    segundos_por_frame = clock.tick(FPS) / 1000

    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

        elif event.type == pygame.KEYDOWN:
            # obtener logro al disparar
            if event.key == pygame.K_SPACE:
                sistema_logros.activar("primer_disparo")

            if event.key == pygame.K_SPACE:
                resultado = arwing.disparar(grupo_balas_arwing)
                for bala in grupo_balas_arwing:
                    if bala not in todos_los_sprites:
                        todos_los_sprites.add(bala)

                # PowerUp
                if arwing.estadisticas.get("disparos", 0) >= 25:
                    arwing.estadisticas["disparos"] = 0
                    crear_powerup()

    # Generación de hostiles (enemigos o meteoritos)
    nuevo_hostil = next(orquestador.generador, None)
    if nuevo_hostil:
        todos_los_sprites.add(nuevo_hostil)
        if nuevo_hostil.tipo == "meteorito":
            meteoritos.add(nuevo_hostil)
        else:
            grupo_enemigos.add(nuevo_hostil)


    # Actualización general de los elementos en pantalla
    arwing.update(segundos_por_frame)
    grupo_enemigos.update(segundos_por_frame, grupo_balas_enemigo)
    meteoritos.update(segundos_por_frame)
    grupo_balas_arwing.update(segundos_por_frame)
    grupo_balas_enemigo.update(segundos_por_frame)
    grupo_powerups.update(segundos_por_frame)

    # Conteo recursivo de meteoritos y enemigos en pantalla
    cantidad_meteoritos = contar_recursivo(list(meteoritos))
    cantidad_enemigos = contar_recursivo(list(grupo_enemigos))

    # Colisión de Arwing con powerups para mejora disparo
    colision_powerups = pygame.sprite.spritecollide(arwing, grupo_powerups, True)
    for power in colision_powerups:
        sistema_logros.activar("potenciado") # logro por tomar primer powerup
        arwing.mejorar_disparo()

    
    # Sistema de colisiones
    # Balas del jugador dañan a cualquier enemigo
    for hostil in list(meteoritos) + list(grupo_enemigos):
        colision_balas = pygame.sprite.spritecollide(hostil, grupo_balas_arwing, True)
        for bala in colision_balas:
            hostil.recibir_dano(bala.danio)

        # si de destruye el enemigo o meteorito
        if hostil.vida <= 0:

            # Logro primer enemigo eliminado
            if hostil.tipo == "enemigo":
                sistema_logros.activar("primer_kill")

            # Logro cazador de meteoritos (3 eliminados)
            if hostil.tipo == "meteorito":
                meteoritos_destruidos += 1
                if meteoritos_destruidos == 3:
                    sistema_logros.activar("cazador_meteoritos")
    
    # Balas enemigas dañan al Arwing
    colision_balas_enemigas = pygame.sprite.spritecollide(arwing, grupo_balas_enemigo, True)
    for bala in colision_balas_enemigas:
        arwing.recibir_dano(bala.danio)
    # Si la salud llega a 0 → Explosión
    if arwing.salud <= 0:
        arwing.muerto = True
        arwing.explotar(todos_los_sprites)

    # si arwing muere detener el loop y enviar a pantalla de muerte

    if arwing.muerto:
        pygame.time.delay(500)
        resultado = pantalla_muerte()

        if resultado == "reiniciar":

            # Limpiar grupos
            todos_los_sprites.empty()
            grupo_balas_arwing.empty()
            grupo_balas_enemigo.empty()
            grupo_enemigos.empty()
            meteoritos.empty()
            grupo_powerups.empty()

            # Reiniciar contadores
            meteoritos_destruidos = 0

            # Crear un Arwing nuevo
            arwing = Arwing(sistema_logros)
            todos_los_sprites.add(arwing)

            # Reiniciar orquestador
            orquestador = OrquestadorHostiles(grupo_enemigos)

            # Evitar que se quede el arwing en estado muerto
            arwing.muerto = False

            # Saltar al siguiente ciclo del loop principal
            continue   
    
    # Colisiones directas Arwing
    for hostil in list(meteoritos) + list(grupo_enemigos):
        if pygame.sprite.collide_rect(arwing, hostil):
            hostil.colisionar_con_arwing(arwing)


    # Detectar fin de la oleada.
    if orquestador.oleada_actual < len(orquestador.oleadas):

        config_actual = orquestador.oleadas[orquestador.oleada_actual]

        if orquestador.enemigos_generados == config_actual["enemigos"] and len(grupo_enemigos) == 0:
            print(f"--- OLEADA {orquestador.oleada_actual + 1} COMPLETADA — PASANDO A SIGUIENTE ---")
            orquestador.oleada_actual += 1
            
            # Resetear contadores para la nueva oleada
            orquestador.enemigos_generados = 0
            orquestador.ultimo_meteorito = pygame.time.get_ticks()

    # Reiniciar el juego despues de obtener victoria
    
    if (orquestador.oleada_actual >= len(orquestador.oleadas) and len(grupo_enemigos) == 0):
            sistema_logros.activar("juego_completado")

            # ⚠️ Mostrar logro antes de cambiar de escena
            fondo_juego.dibujar_en(ventana)
            todos_los_sprites.draw(ventana)
            sistema_logros.dibujar(ventana, pygame.font.Font(None, 26), ANCHO)
            pygame.display.flip()

            pygame.time.delay(1200)  # tiempo para que el jugador vea el logro

            resultado = pantalla_victoria()

            if resultado == "reiniciar":

                todos_los_sprites.empty()
                grupo_balas_arwing.empty()
                grupo_balas_enemigo.empty()
                grupo_enemigos.empty()
                meteoritos.empty()
                grupo_powerups.empty()

                meteoritos_destruidos = 0

                arwing = Arwing(sistema_logros)
                todos_los_sprites.add(arwing)

                orquestador = OrquestadorHostiles(grupo_enemigos)

                continue 
               

    
    # Carga de sprites en la pantalla de juego
    fondo_juego.actualizar(segundos_por_frame)
    fondo_juego.dibujar_en(ventana)

    todos_los_sprites.draw(ventana)
    grupo_balas_arwing.draw(ventana)
    grupo_balas_enemigo.draw(ventana)

    # barra de vida
    dibujar_barra_vida(ventana, ANCHO - 70, ALTO - 30, arwing.salud, 100)

    # fuente de texto
    fuente = pygame.font.Font(None, 26)

    # mostrar meteoritos en pantalla
    texto_mete = fuente.render(f"Meteoritos: {cantidad_meteoritos}", True, (255, 255, 255))
    ventana.blit(texto_mete, (10, 10))

    # mostrar enemigos en pantalla
    texto_enem = fuente.render(f"Enemigos: {cantidad_enemigos}", True, (255, 255, 255))
    ventana.blit(texto_enem, (10, 40))

    # dibujar logros en pantalla
    sistema_logros.dibujar(ventana, fuente, ANCHO)
    

    pygame.display.flip()

pygame.quit()
