import random

class Casilla:

    def __init__(self, coordenadas, largo, tamaño, colorVivo, colorMuerto, colorEnfermo, signoHombre, signoMujer):
        self.coordenadas = coordenadas #coordenada de la esquina superior izquierda  
        self.largo = largo   #largo del tablero (en este caso es 625)
        self.tamaño = tamaño #tamaño de cada casilla (en este caso es 25)    625/25 = 25
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

    #Funcion para obtener las coordenadas de la esquina derecha inferior
    def completar_cuadrado(self):
        return (self.coordenadas[0]+self.tamaño, self.coordenadas[1]+self.tamaño)

    #Funcion para validar si una coordenada está dentro del tablero
    def adentro(self, coord):
        (x, y) = coord
        return (x >= 0 and x <= self.largo-self.tamaño) and (y >= 0 and y <= self.largo-self.tamaño)

    #Funcion que aumento los turnos que un ente lleva existiendo
    def aumentar_turno(self):
        self.contadorTurnos = self.contadorTurnos + 1
        if self.tienePareja:
            self.contadorTurnosPareja = self.contadorTurnosPareja + 1
        else:
            self.contadorTurnosPareja = 0

    #Funcion para obtener una lista de las casillas validas alrededor de una casilla original
    def vecinos(self): 
        (x, y) = self.coordenadas
        return list(filter(self.adentro,[
            (x-self.tamaño, y+self.tamaño), (x, y+self.tamaño), (x+self.tamaño, y+self.tamaño),
            (x-self.tamaño, y), (x+self.tamaño, y),(x-self.tamaño, y-self.tamaño), (x, y-self.tamaño), 
            (x+self.tamaño, y-self.tamaño)]))

    #Funcion para obtener el color de una casilla dependiendo del contexto
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
    
    #Funcion para obtener el signo del genero de un ente 
    def obtener_signo(self):
        if(self.hayEnte):
            if self.genero:
                return self.signoHombre
            else:
                return self.signoMujer
        else:
            return ""

    #Funcion para eliminar por completo a un ente
    def eliminar(self):
        self.hayEnte = False
        self.genero = None
        self.estado = None
        self.salud = None

    #Funcion cuando muerte un ente
    def morir(self):
        self.estado = False
        self.contadorTurnos = 0
        self.contadorTurnosPareja = 0

    #Funcion para enferma a un ente
    def enfermar(self):
        self.salud = False

    def sanar(self):
        self.salud = True
    
#El tablero utiliza un diccionario como estructura para contener a las casillas. La llave es la cooredenada y el valor la casilla como tal.
#self.casillas es la estructura
class Tablero:

    #en este constructor puede cambiar los colores y signos que se utilizan
    def __init__(self, largo, tamañoCasillas, colorVivo='lime green', colorMuerto='indian red', colorEnfermo='light yellow', signoHombre="H", signoMujer="M"):
        self.largo = largo  #625 en este caso
        self.tamañoCasillas = tamañoCasillas #25 en este caso .... 625/25= 25 casillas 
        self.colorVivo = colorVivo
        self.colorMuerto = colorMuerto
        self.colorEnfermo = colorEnfermo
        self.signoHombre = signoHombre
        self.signoMujer = signoMujer
        self.turno = 0
        self.turnosSinNacimiento = 0
        self.casillas = self.iniciar_tablero()   #Estructura que contiene todas las casillas
        self.primera_generacion()   #Genera aleatoriamente 200 entes

    #Funcion que inicializa la estructura de datos con las casillas
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

    #Funcion que genera 200 entes aleatorios, se hace un shuffle al orden de la estructura de datos
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

    #Se utiliza el mismo metodo de shuffle para la aleatoridad
    def generar_ente_aleatorio(self):
        self.turnosSinNacimiento = 0
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

    #Funcion para validar se hay entes 
    def hay_entes_vivos(self):
        lists = list(self.casillas.items())
        for coordenadas, casilla in lists:
            if casilla.hayEnte == True:
                return True
        return False

    def enfermar_ente_aleatorio(self):
        random_casillas = list(self.casillas.items())
        random.shuffle(random_casillas)
        for coordenadas, casilla in random_casillas:
            if not casilla.hayEnte or not casilla.estado or not casilla.salud:
                continue
            casilla.enfermar()
            return       

    #Funcion principal para llevar a cabo el comportamiento de los entes cada turno
    def comportamiento(self):
        nacimiento = False
        for coordenada, casillaActual in self.casillas.items():
            if not casillaActual.hayEnte:    #si la casilla no tiene ente, continua
                continue

            vecinosVivos = 0     #variables por utilizar
            vecinosMuertos = 0
            vecinosEnfermos = 0
            vecinosSanos = 0
            tienePareja = False
            muerte = False
            vecinos = casillaActual.vecinos()

            for vecino in vecinos:                  #Se recorren todos los vecinos de un ente para sacar la info necesaria de las reglas
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

            if not casillaActual.estado and casillaActual.contadorTurnos >= 3:       #Administracion si debe morir or ser borrado
                casillaActual.eliminar()

            elif not casillaActual.salud and casillaActual.contadorTurnos >= 5:
                casillaActual.morir()
                
            elif casillaActual.contadorTurnos >= 8:
                casillaActual.morir()  
            
            else:                                       #Se validan las reglas especificadas en el pdf
                if casillaActual.estado:
                    if vecinosVivos >= 3:
                        casillaActual.estado = True
                    elif vecinosMuertos >= 4:
                        casillaActual.morir()
                    if casillaActual.tienePareja and casillaActual.contadorTurnosPareja >= 3:
                        self.generar_ente_aleatorio()
                        casillaActual.contadorTurnosPareja = 0
                        nacimiento = True
                    if vecinosEnfermos >= 4:
                        casillaActual.enfermar()
                    elif vecinosSanos >= 6:
                        casillaActual.sanar()
                
        if not nacimiento:
            self.turnosSinNacimiento = self.turnosSinNacimiento + 1    #Llevar cuenta de turnos sin nacimientos... 5 y se termina el juego


#Clase que se utiliza para controlar el flujo del juego
class Administracion:

    def __init__(self, tool):
        self.root = tool.root
        self.gui = tool
        self.tablero = tool.tablero


    def siguiente_turno(self):
        sigue = self.tablero.hay_entes_vivos()
        if self.tablero.turnosSinNacimiento >= 5 or not sigue:   #Si se cumplen 5 turnos sin nacimientos o no hay entes vivos.. se termina el juego
            self.gui.terminar_juego()
            self.root.destroy()
            return

        self.tablero.turno = self.tablero.turno + 1
        self.gui.refrescar()

    def aniquilar(self):
        self.gui.terminar_juego()
        self.root.destroy()

    def enfermar(self):
        self.tablero.enfermar_ente_aleatorio()
        self.gui.refrescar_sin_aumento_turno()

