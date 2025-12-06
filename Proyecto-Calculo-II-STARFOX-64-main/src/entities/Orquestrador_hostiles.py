import pygame
import random
from entities.meteoritos import Meteorito
from entities.Enemigos import Enemigos


class OrquestadorHostiles:

    def __init__(self, grupo_enemigos):
        self.grupo_enemigos = grupo_enemigos
        #Oleadas del nivel, 3 en total.
        self.oleadas = [
            {"enemigos": 3, "max_simultaneos": 2, "intervalo_meteoritos": 1500},
            {"enemigos": 5, "max_simultaneos": 3, "intervalo_meteoritos": 1300},
            {"enemigos": 6, "max_simultaneos": 3, "intervalo_meteoritos": 1000},
        ]

        self.oleada_actual = 0
        self.enemigos_generados = 0
        self.ultimo_meteorito = pygame.time.get_ticks()

        self.generador = self.generador_hostiles()

    def generador_hostiles(self):
        while True:

            if self.oleada_actual >= len(self.oleadas):
                yield None
                continue

            config = self.oleadas[self.oleada_actual]
            tiempo_actual = pygame.time.get_ticks()

            # Generación de meteoritos
            if tiempo_actual - self.ultimo_meteorito >= config["intervalo_meteoritos"]:
                pos_x = random.randint(0, 760)
                meteorito = Meteorito(pos_x, -40, random.randint(2, 5))
                self.ultimo_meteorito = tiempo_actual
                yield meteorito
                continue

            # Generación de enemigos
            if (self.enemigos_generados < config["enemigos"]
                and len(self.grupo_enemigos) < config["max_simultaneos"]):

                pos_x = random.randint(0, 760)
                enemigo = Enemigos(pos_x, -40, random.randint(2, 4))
                self.enemigos_generados += 1
                yield enemigo
                continue

            yield None
