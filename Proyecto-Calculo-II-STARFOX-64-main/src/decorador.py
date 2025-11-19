def registrar_evento(nombre_evento):
    """Decorador que incrementa un contador de eventos dentro del Arwing."""
    def decorador(func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "estadisticas"):
                self.estadisticas = {}

            if nombre_evento not in self.estadisticas:
                self.estadisticas[nombre_evento] = 0

            self.estadisticas[nombre_evento] += 1
            return func(self, *args, **kwargs)
        return wrapper
    return decorador
