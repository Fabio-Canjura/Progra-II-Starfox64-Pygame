
#Decorador que incrementa un contador de eventos dentro del Arwing.
def registrar_evento(nombre_evento):
    def decorador(funcion_original):
        def funcion_decorada(self, grupo_balas):
            # Ejecutar la función
            se_disparo = funcion_original(self, grupo_balas)
            # Solo contar si REALMENTE disparó
            if se_disparo:
                self.estadisticas[nombre_evento] = self.estadisticas.get(nombre_evento, 0) + 1
            return se_disparo
        return funcion_decorada
    return decorador


