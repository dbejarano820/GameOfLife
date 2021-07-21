from tkinter import *
from tkinter import messagebox
import logica


class Pantalla:

    def __init__(self, largo, tamañoCasilla):
        self.largo = largo
        self.tamañoCasilla = tamañoCasilla

        self.root = Tk()
        self.tablero = logica.Tablero(self.largo, self.tamañoCasilla)
        self.admin = logica.Administracion(self)
        self.canvas = Canvas(self.root, height=self.largo, width=self.largo)
        self.canvas.pack()
        
        self.siguiente = Button(self.root, text="Siguiente", command=self.admin.siguiente_turno)
        self.siguiente.pack(side=RIGHT, padx=15, pady=15)
        self.aniquilar = Button(self.root, text="Aniquilar", command=self.admin.aniquilar)
        self.aniquilar.pack(side=RIGHT, padx=15, pady=15)
        self.enfermar = Button(self.root, text="Enfermar", command=self.admin.enfermar)
        self.enfermar.pack(side=RIGHT, padx=15, pady=15)

        self.turnos = Label(self.root, text= "Turno: " + str(self.tablero.turno))
        self.turnos.config(font=("Courier", 44))
        self.turnos.pack()
        self.itemsColores = self.actualizar_colores()
        self.itemsGeneros = self.actualizar_generos()

        self.root.mainloop()
    

    #Funcion para el flujo del juego
    def refrescar(self):
        self.tablero.comportamiento()
        self.actualizar_colores(canvas_done=True, canvas_items=self.itemsColores)
        self.actualizar_generos(canvas_done=True, canvas_items=self.itemsGeneros)
        self.turnos.configure(text="Turno: " + str(self.tablero.turno))

    #Refrescar solamente graficos
    def refrescar_sin_aumento_turno(self):
        self.actualizar_colores(canvas_done=True, canvas_items=self.itemsColores)
        self.actualizar_generos(canvas_done=True, canvas_items=self.itemsGeneros)


    #Actualizar colores de casillas
    def actualizar_colores(self, canvas_done=False, canvas_items={}):
        casillas_items = self.tablero.casillas
        if not canvas_done:
            for coordenadas, casilla in casillas_items.items():
                (x2, y2) = casilla.completar_cuadrado()   
                (x1, y1) = coordenadas
                canvas_items[coordenadas] = self.canvas.create_rectangle(x1, y1, x2, y2,fill = casilla.obtener_color())
            return canvas_items
        
        else:
            if canvas_items:
                for coordenadas, item in canvas_items.items():
                    self.canvas.itemconfig(item, fill=casillas_items[coordenadas].obtener_color())

    #Actualizar signos de generos de entes
    def actualizar_generos(self, canvas_done=False, canvas_items={}):
        casillas_items = self.tablero.casillas
        if not canvas_done:

            for coordenadas, casilla in casillas_items.items():
                (x1, y1) = coordenadas
                x1 = x1 + 12.5
                y1 = y1 + 12.5
                canvas_items[coordenadas] = self.canvas.create_text(x1, y1, text= casilla.obtener_signo(), fill="black")
            return canvas_items
        
        else:
            if canvas_items:
                for coordenadas, item in canvas_items.items():
                    self.canvas.itemconfig(item, text=casillas_items[coordenadas].obtener_signo())

    def terminar_juego(self):
        messagebox.showinfo("showinfo", "El juego de la vida ha terminado")