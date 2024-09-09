import tkinter as tk
import controladores.controlador as controlador
from vistas.vista import crear_vista_calculadora

if __name__ == "__main__":
    raiz = tk.Tk()
    crear_vista_calculadora(raiz, controlador)
    raiz.mainloop()
