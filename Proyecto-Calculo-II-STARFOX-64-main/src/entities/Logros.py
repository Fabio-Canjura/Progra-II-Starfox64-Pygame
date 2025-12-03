# esta clase muestra los logros obtenidos durante la partida

import pygame

class SistemaLogros:
    def __init__(self):
        self.logros = set()
        self.mensaje = ""
        self.tiempo_mensaje = 0
        self.duracion_mensaje = 2000  # ms

    def activar(self, nombre):
        if nombre not in self.logros:
            self.logros.add(nombre)
            # Crear un mensaje del logro
            nombre_formateado = nombre.replace("_", " ").title()
            self.mensaje = f"¡Logro desbloqueado: {nombre_formateado}!"
            self.tiempo_mensaje = pygame.time.get_ticks()

    def dibujar(self, pantalla, fuente, ancho):
        # Mostrar mensaje solo por 2 segundos
        if pygame.time.get_ticks() - self.tiempo_mensaje < self.duracion_mensaje:
            texto = fuente.render(self.mensaje, True, (255, 215, 0))  # dorado
            x = ancho // 2 - texto.get_width() // 2
            pantalla.blit(texto, (x, 20))

    def obtener_logros(self):
        return self.logros
