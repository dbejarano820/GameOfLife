import random


class Casilla:

    def __init__(self, coordenadas, tamaño, hayEnte, colorVivo, colorMuerto, colorEnfermo, signoHombre, signoMujer):
        self.coordenadas = coordenadas
        self.tamaño = tamaño
        self.hayEnte = hayEnte
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer

    def generar_ente(self, genero, salud, estado, ):
        self.genero = genero 
        self.salud = salud
        self.estado = estado

    def completar_cuadrado(self):
        return (self.coordenadas[0]+self.tamaño, self.coordenadas[1]+self.tamaño)

    # def pintar_valido(self, coordenadas):
    #     (x,y) = coordenadas
    #     return (x>=0 and x<=self.tamaño) and (y>=0 and y<=self.tamaño-tamaño)

    def hay_ente(self):
        return self.hayEnte

    def vecinos(self): 
        (x, y) = self.coordenadas
        return list(filter(self.inbounds, [
            (x-self.tamaño, y+self.tamaño), (x, y+self.tamaño), (x+self.tamaño, y+self.tamaño),
            (x-self.tamaño, y),                                      (x+self.tamaño, y),
            (x-self.tamaño, y-self.tamaño), (x, y-self.tamaño), (x+self.tamaño, y-self.tamaño),
        ]))

    def obtener_color(self):
        if(self.hay_ente):
            if not self.estado:
                return self.colorMuerto
            elif not self.salud:
                return self.colorEnfermo
            else:
                return self.colorVivo
        else:
            return 'grey'
    
    def obtener_signo(self):
        if(self.hay_ente):
            if self.genero:
                return self.signoHombre
            else:
                return self.signoMujer
        else:
            return ""
    

class Tablero:

    def __init__(self, coordenadas, largo, tamañoCasillas, colorVivo='lime green', colorMuerto='indian red', colorEnfermo='light yellow', signoHombre="H", signoMujer="M"):
        self.coordenadas = coordenadas
        self.largo = largo
        self.tamañoCasillas = tamañoCasillas
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer

        self.casillas