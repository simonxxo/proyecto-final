import tkinter as tk
from controladores.controlador import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def crear_vista_calculadora(raiz, controlador):
    raiz.title("Calculadora Científica y Gráfica")
    raiz.configure(bg=tema_claro["bg_color"])
    raiz.resizable(0,0)

    entrada_expresion = tk.Entry(raiz, font=("Arial", 16), bd=5, insertwidth=4, width=30, borderwidth=4,
                                 bg=tema_claro["entry_bg"], fg=tema_claro["entry_fg"],)
    entrada_expresion.grid(row=0, column=0, columnspan=4, pady=5)
    entrada_expresion.focus_set()

    historial = tk.Listbox(raiz, font=("Arial", 12), width=30, height=30, bg=tema_claro["hist_bg"], fg=tema_claro["hist_fg"])
    historial.grid(row=1, column=4, rowspan=7, padx=10, pady=10)
    historial.bind('<Double-1>', lambda event: controlador.cargar_historial(event, entrada_expresion, historial))

    teclado = tk.Frame(raiz, bg=tema_claro["bg_color"])
    teclado.grid(row=1, column=0, rowspan=8, columnspan=4, padx=10, pady=10)

    # Crear figura para las gráficas
    fig, ax = plt.subplots(figsize=(5, 5))

    # Crear Canvas usando FigureCanvasTkAgg
    canvas_graficas = FigureCanvasTkAgg(fig, master=raiz)
    canvas_graficas.draw()
    canvas_graficas.get_tk_widget().grid(row=1, column=5, rowspan=8, pady=2, columnspan= 5, padx= 20)

    # Crear Frame para la barra de herramientas
    toolbar_frame = tk.Frame(raiz)
    toolbar_frame.grid(row=8, column=5, padx=10, pady=10)
    toolbar = NavigationToolbar2Tk(canvas_graficas, toolbar_frame)
    toolbar.update()

    botones = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3), ('C', 0, 4), ('→', 0, 5),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3), ('del', 1, 4),('←', 1, 5),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3), ('GRAPH', 2, 4),(')', 2, 5),
        ('.', 3, 0), ('0', 3, 1), ('x', 3, 2), ('+', 3, 3), ('exp', 3, 4),('(',3, 5),
        ('sin', 4, 0), ('cos', 4, 1), ('tan', 4, 2), ('π', 4, 3), ('=', 4, 4)
    ]

    botones_gui = []
    for boton, row, column in botones:
        btn = tk.Button(teclado, text=boton, padx=15, pady=15, bg=tema_claro["button_bg"], fg=tema_claro["button_fg"], font=("Arial", 14),
                        width=4, height=2, command=lambda btn=boton: controlador.al_hacer_click_boton(btn, entrada_expresion, historial, canvas_graficas, toolbar))
        btn.grid(row=row, column=column, padx=1, pady=1)
        botones_gui.append(btn)

    for i in range(5):
        teclado.grid_rowconfigure(i, weight=1)
    for j in range(6):
        teclado.grid_columnconfigure(j, weight=1)
        

    boton_tema = tk.Button(teclado, text="Cambiar Tema", padx=15, pady=10, bg=tema_claro["button_bg"], fg=tema_claro["button_fg"], 
                           command=lambda: cambiar_tema(raiz, tema_oscuro, entrada_expresion, historial, botones_gui, teclado, btn_descargar_historial, btn_borrar_historial, btn_borrar_nube, btn_subir_historial, boton_tema) 
                           if raiz["bg"] == tema_claro["bg_color"] else cambiar_tema(raiz, tema_claro, entrada_expresion, historial, botones_gui, teclado, btn_descargar_historial, btn_borrar_historial, btn_borrar_nube, btn_subir_historial, boton_tema))
    boton_tema.grid(row=5, column=0, columnspan=5, pady=10, sticky="ew")

    btn_descargar_historial = tk.Button(teclado, text="Cargar Historial", padx=15, pady=10, bg=tema_claro["button_bg"], fg=tema_claro["button_fg"], command=lambda: descargar_historial(historial))
    btn_descargar_historial.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    btn_borrar_historial = tk.Button(teclado, text="Borrar Historial Local", padx=15, pady=10, bg=tema_claro["button_bg"], fg=tema_claro["button_fg"], command=lambda: borrar_historial_local(historial))
    btn_borrar_historial.grid(row=6, column=2, columnspan=3, padx=5, pady=5, sticky="ew")

    btn_borrar_nube = tk.Button(teclado, text="Borrar Historial en Nube", padx=15, pady=10, bg=tema_claro["button_bg"], fg=tema_claro["button_fg"], command=lambda: borrar_baseDedatos())
    btn_borrar_nube.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    btn_subir_historial = tk.Button(teclado, text="Subir Historial a Nube", padx=15, pady=10, bg=tema_claro["button_bg"], fg=tema_claro["button_fg"], command=lambda: subir_historial(historial))
    btn_subir_historial.grid(row=7, column=2, columnspan=3, padx=5, pady=5, sticky="ew")

    descargar_historial(historial)
