import pygame
import os #Encargado de traducir entradas universales/rutas absolutas sin importar sistema operativo.
from constantes import ANCHO, ALTO

class fondo:
    def __init__(self, ruta_imagen, velocidad=120):
        try:
            self.imagen = pygame.image.load(ruta_imagen).convert()
            self.imagen = pygame.transform.scale(self.imagen, (ANCHO, ALTO))
        except Exception as e:
            print(f"ERROR al cargar el fondo, se utilizará uno por defecto.")
            # Fondo en caso de falla
            self.imagen = pygame.Surface((ANCHO, ALTO))
            self.imagen.fill((0, 0, 0))

        self.velocidad = velocidad
        # Dos copias del mismo fondo para scroll continuo
        self.fondo_1 = 0
        self.fondo_2 = -ALTO

    def actualizar(self, segundos_por_frame):
        movimiento_vertical = self.velocidad * segundos_por_frame
        self.fondo_1 += movimiento_vertical
        self.fondo_2 += movimiento_vertical
        if self.fondo_1 >= ALTO:
            self.fondo_1 = self.fondo_2 - ALTO
        if self.fondo_2 >= ALTO:
            self.fondo_2 = self.fondo_1 - ALTO


    """Función encargada de superponer ambos fondos a utilizar en
       la ventana principal del juego. blit se encarga de realizarlo.
    """
    def dibujar_en(self, pantalla):
        pantalla.blit(self.imagen, (0, int(self.fondo_1)))
        pantalla.blit(self.imagen, (0, int(self.fondo_2)))
