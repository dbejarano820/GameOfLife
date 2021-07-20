from tkinter import *
import logica

class Pantalla:

    def __init__(self, largo, tamañoCasilla):
        self.largo = largo
        self.tamañoCasilla = tamañoCasilla

        self.root = Tk()
        self.tablero = logica.Tablero(self.largo, self.tamañoCasilla)
        self.admin = logica.Administracion(self.root)
        self.canvas = Canvas(self.root, height=self.largo, width=self.largo)
        self.canvas.pack()
        
        self.siguiente = Button(self.root, text="Siguiente", command=self.admin.siguienteTurno)
        self.siguiente.pack(side=RIGHT, padx=15, pady=15)
        self.aniquilar = Button(self.root, text="Aniquilar", command=self.admin.aniquilar)
        self.aniquilar.pack(side=RIGHT, padx=15, pady=15)
        self.enfermar = Button(self.root, text="Enfermar", command=self.admin.enfermar)
        self.enfermar.pack(side=RIGHT, padx=15, pady=15)

        self.turnos = Label(self.root, text= "Turno: 1")
        self.turnos.config(font=("Courier", 44))
        self.turnos.pack()
        self.items = self.actualizar()
        self.root.after(5, self.actualizar)
        self.root.mainloop()
    
    def refrescar(self):
        self.tablero.comportamiento()
        self.actualizar(canvas_done=True, canvas_items=self.items)
        self.root.after(5, self.refrescar)

    def actualizar(self, canvas_done=False, canvas_items={}):

        casillas_items = self.tablero.casillas

        if not canvas_done:

            for coordenadas, casilla in casillas_items.items():
                (x2, y2) = casilla.completar_cuadrado()
                (x1, y1) = coordenadas

                canvas_items[coordenadas] = self.canvas.create_rectangle(x1, y1, x2, y2,fill = casilla.obtener_color())
                #obtener genero otra lista de items
            return canvas_items
        
        else:

            if canvas_items:
                for coordenadas, item in canvas_items.items():
                    self.canvas.itemconfig(item, fill=casillas_items[coordenadas].obtener_color())