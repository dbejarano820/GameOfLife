import random
import time


class Casilla:

    def __init__(self, coordenadas, largo, tamaño, colorVivo, colorMuerto, colorEnfermo, signoHombre, signoMujer):
        self.coordenadas = coordenadas
        self.largo = largo
        self.tamaño = tamaño
        self.hayEnte = False
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer
        self.contadorTurnos = 0
        self.contadorTurnosPareja = 0

    def generar_ente(self, genero, salud, estado):
        self.genero = genero   # verdadero es mujer
        self.salud = salud     # verdadero es saludable
        self.estado = estado   # verdadero es vivo
        self.hayEnte = True
        self.tienePareja = False

    def completar_cuadrado(self):
        return (self.coordenadas[0]+self.tamaño, self.coordenadas[1]+self.tamaño)

    def inbounds(self, coord):
        (x, y) = coord
        return (x >= 0 and x <= self.largo-self.tamaño) and (y >= 0 and y <= self.largo-self.tamaño)

    def aumentar_turno(self):
        self.contadorTurnos = self.contadorTurnos + 1
        if self.tienePareja:
            self.contadorTurnosPareja = self.contadorTurnosPareja + 1
        else:
            self.contadorTurnosPareja = 0

    def vecinos(self): 
        (x, y) = self.coordenadas
        return list(filter(self.inbounds,[
            (x-self.tamaño, y+self.tamaño), (x, y+self.tamaño), (x+self.tamaño, y+self.tamaño),
            (x-self.tamaño, y), (x+self.tamaño, y),(x-self.tamaño, y-self.tamaño), (x, y-self.tamaño), 
            (x+self.tamaño, y-self.tamaño)]))

    def obtener_color(self):
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

    def eliminar(self):
        self.hayEnte = False
        self.genero = None
        self.estado = None
        self.salud = None
    

class Tablero:

    def __init__(self, largo, tamañoCasillas, colorVivo='lime green', colorMuerto='indian red', colorEnfermo='light yellow', signoHombre="H", signoMujer="M"):
        self.largo = largo
        self.tamañoCasillas = tamañoCasillas
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer
        self.turno = 0
        self.turnosSinNacimiento = 0
        self.casillas = self.iniciar_tablero()
        self.primera_generacion()


    def iniciar_tablero(self):
        casillas = {}
        for y in range(0, self.largo, self.tamañoCasillas):
            for x in range(0, self.largo, self.tamañoCasillas):
                casilla = Casilla((x, y),
                                    self.largo,
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
                return
            estado = random.choice([True, False])
            salud = random.choice([True, False])
            genero = random.choice([True, False])
            casilla.generar_ente(genero, salud, estado)
            contador = contador - 1

    def generar_ente_aleatorio(self):
        self.turnosSinNacimiento = 0
        print("birth")
        random_casillas = list(self.casillas.items())
        random.shuffle(random_casillas)
        for coordenadas, casilla in random_casillas:
            if casilla.hayEnte:
                continue
            genero = random.choice([True, False])
            salud = random.choice([True, False])
            estado = random.choice([True, False])
            casilla.generar_ente(genero, salud, estado)
            return

    def hay_entes_vivos(self):
        lists = list(self.casillas.items())
        for coordenadas, casilla in lists:
            if casilla.hayEnte == True:
                return True
        return False

    def comportamiento(self):
        nacimiento = False
        for coordenada, casillaActual in self.casillas.items():
            if not casillaActual.hayEnte:
                continue
            vecinosVivos = 0
            vecinosMuertos = 0
            vecinosEnfermos = 0
            vecinosSanos = 0
            tienePareja = False
            muerte = False
            vecinos = casillaActual.vecinos()

            for vecino in vecinos:
                if self.casillas[vecino].hayEnte:
                    enteVecino = self.casillas[vecino]
                    if not tienePareja:
                        tienePareja = enteVecino.genero != casillaActual.genero
                    if not enteVecino.estado:
                        vecinosMuertos = vecinosMuertos + 1
                    if not enteVecino.salud:
                        vecinosEnfermos = vecinosEnfermos + 1
                    if enteVecino.salud:
                        vecinosSanos = vecinosSanos + 1
                    if enteVecino.estado:
                        vecinosVivos = vecinosVivos + 1
            
            casillaActual.tienePareja = tienePareja
            casillaActual.aumentar_turno()

            if not casillaActual.estado and casillaActual.contadorTurnos >= 3:
                casillaActual.eliminar()
                #continue

            elif not casillaActual.salud and casillaActual.contadorTurnos >= 5:
                casillaActual.eliminar()
                #continue
                
            elif casillaActual.contadorTurnos >= 8:
                casillaActual.eliminar()
                
            
            else:
                for vecino in vecinos:
                    if self.casillas[vecino].hayEnte:
                        enteVecino = self.casillas[vecino]
                        if not tienePareja:
                            tienePareja = enteVecino.genero != casillaActual.genero
                        if not enteVecino.estado:
                            vecinosMuertos = vecinosMuertos + 1
                        if not enteVecino.salud:
                            vecinosEnfermos = vecinosEnfermos + 1
                        if enteVecino.salud:
                            vecinosSanos = vecinosSanos + 1
                        if enteVecino.estado:
                            vecinosVivos = vecinosVivos + 1

                #Esta vivo
                casillaActual.tienePareja = tienePareja
                if casillaActual.estado:
                    if vecinosVivos >= 3:
                        casillaActual.estado = True
                    if vecinosMuertos >= 4:
                        casillaActual.estado = False
                        muerte = True
                    if casillaActual.tienePareja and casillaActual.contadorTurnosPareja >= 3:
                        self.generar_ente_aleatorio()
                        casillaActual.contadorTurnosPareja = 0
                        nacimiento = True
                    if vecinosEnfermos >= 4:
                        casillaActual.salud = False
                    if vecinosSanos >= 6:
                        casillaActual.salud = True

                if muerte:
                    casillaActual.contadorTurnos = 0
                    casillaActual.contadorTurnosPareja = 0
                    continue
                
        if not nacimiento:
            self.turnosSinNacimiento = self.turnosSinNacimiento + 1

class Administracion:

    def __init__(self, tool):
        self.root = tool.root
        self.gui = tool
        self.tablero = tool.tablero


    def siguienteTurno(self):

        sigue = self.tablero.hay_entes_vivos()
        print("Ok" + str(sigue))
        print(self.tablero.turnosSinNacimiento)
        if self.tablero.turnosSinNacimiento >= 5 or not sigue:
            self.gui.terminarJuego()
           # time.sleep(2.5)
            self.root.destroy()
            return

        self.tablero.turno = self.tablero.turno + 1
        self.gui.refrescar()

    def aniquilar(self):
        self.root.destroy()

    def enfermar(self):
        pass

