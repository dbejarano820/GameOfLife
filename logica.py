import random


class Casilla:

    def __init__(self, coordenadas, tamaño, colorVivo, colorMuerto, colorEnfermo, signoHombre, signoMujer):
        self.coordenadas = coordenadas
        self.tamaño = tamaño
        self.hayEnte = False
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer
        self.contadorTurnos = 0
        self.contadorTurnosPareja = 0

    def generar_ente(self, genero, salud, estado, ):
        self.genero = genero   # verdadero es mujer
        self.salud = salud     # verdadero es saludable
        self.estado = estado   # verdadero es vivo
        self.hayEnte = True
        self.tienePareja = False

    def completar_cuadrado(self):
        return (self.coordenadas[0]+self.tamaño, self.coordenadas[1]+self.tamaño)

    def aumentar_turno(self):
        self.contadorTurnos = self.contadorTurnos + 1
        if self.tienePareja:
            self.contadorTurnosPareja = self.contadorTurnosPareja + 1
        else:
            self.contadorTurnosPareja = 0

    def vecinos(self): 
        (x, y) = self.coordenadas
        return list(filter(self.inbounds, [
            (x-self.tamaño, y+self.tamaño), (x, y+self.tamaño), (x+self.tamaño, y+self.tamaño),
            (x-self.tamaño, y),                                      (x+self.tamaño, y),
            (x-self.tamaño, y-self.tamaño), (x, y-self.tamaño), (x+self.tamaño, y-self.tamaño),
        ]))

    def obtener_color(self):
        print(self.hayEnte)
        if(self.hayEnte):
            if not self.estado:
                return self.colorMuerto
            elif not self.salud:
                return self.colorEnfermo
            else:
                return self.colorVivo
        else:
            return 'grey'
    
    def obtener_signo(self):
        if(self.hayEnte):
            if self.genero:
                return self.signoHombre
            else:
                return self.signoMujer
        else:
            return ""
    

class Tablero:

    def __init__(self, largo, tamañoCasillas, colorVivo='lime green', colorMuerto='indian red', colorEnfermo='light yellow', signoHombre="H", signoMujer="M"):
        self.largo = largo
        self.tamañoCasillas = tamañoCasillas
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer
        self.turno = 1
        self.turnosSinNacimiento = 0
        self.casillas = self.iniciar_tablero()
        self.primera_generacion()


    def iniciar_tablero(self):
        casillas = {}
        #  (Rows) Loop through the 'length' in steps of 'size' (so as to get the right top left corner each time)
        for y in range(0, self.largo, self.tamañoCasillas):
            #  (Cells) Loop through the 'length' in steps of 'size' (so as to get the right top left corner each time)
            for x in range(0, self.largo, self.tamañoCasillas):
                casilla = Casilla((x, y),
                                    self.tamañoCasillas,
                                    colorVivo=self.colorVivo,
                                    colorMuerto=self.colorMuerto,
                                    colorEnfermo=self.colorEnfermo,
                                    signoHombre=self.signoHombre,
                                    signoMujer=self.signoMujer)
                casillas[(x, y)] = casilla
        return casillas 


    def primera_generacion(self):
        contador = 200
        random_casillas = list(self.casillas.items())
        random.shuffle(random_casillas)
        for coordenadas, casilla in random_casillas:
            if contador < 1:
                break
            genero = random.choice([True, False])
            salud = random.choice([True, False])
            estado = random.choice([True, False])
            casilla.generar_ente(genero, salud, estado)
            contador = contador - 1

    def generar_ente_aleatorio(self):
        pass

    def comportamiento(self):
        for coordenada, casillaActual in self.casillas.items():
            vecinosVivos = 0
            vecinosMuertos = 0
            vecinosEnfermos = 0
            vecinosSanos = 0
            tienePareja = False
            vecinos = casillaActual.vecinos()

            for vecino in vecinos:

                if self.casillas[vecino].hayEnte:
                    enteVecino = self.casillas[vecino]
                    tienePareja = enteVecino.genero != casillaActual.genero
                    if not enteVecino.estado:
                        vecinosMuertos = vecinosMuertos + 1
                        continue
                    elif not enteVecino.salud:
                        vecinosEnfermos = vecinosEnfermos + 1
                    elif enteVecino.salud:
                        vecinosSanos = vecinosSanos + 1
                    else:
                        vecinosVivos = vecinosVivos + 1

                    #Esta vivo
                    muerte = False
                    if casillaActual.estado:
                        if vecinosVivos >= 3:
                            casillaActual.estado = True
                        if vecinosMuertos >= 4:
                            casillaActual.estado = False
                            muerte = True
                        if tienePareja and casillaActual.contadorTurnosPareja > 3:
                            self.generar_ente_aleatorio()
                        if vecinosEnfermos >= 4:
                            casillaActual.salud = False
                        if vecinosSanos >= 6:
                            casillaActual.salud = True
                
                    if muerte:
                        casillaActual.contadorTurnos = 0
                        casillaActual.contadorTurnosPareja = 0
                    else:
                        casillaActual.aumentar_turno()
                


class Administracion:

    def __init__(self, root, tablero):
        self.root = root
        self.tablero = tablero
        pass


    def siguienteTurno(self):
        pass

    def aniquilar(self):
        self.root.destroy()

    def enfermar(self):
        pass