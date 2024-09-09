import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import modelos.modelo as modelo
import modelos.modelo_db as modelo_db

tema_claro = {
    "bg_color": "#D9E8F5",
    "fg_color": "#304269",
    "button_bg": "#6C8EB1",
    "button_fg": "#FFFFFF",
    "entry_bg": "#FFFFFF",
    "entry_fg": "#304269",
    "hist_bg": "#FFFFFF",
    "hist_fg": "#304269",
}

tema_oscuro = {
    "bg_color": "#28292A",
    "fg_color": "#FFDF00",
    "button_bg": "#47494E",
    "button_fg": "#FFDF00",
    "entry_bg": "#47494E",
    "entry_fg": "#FFDF00",
    "hist_bg": "#47494E",
    "hist_fg": "#FFDF00",
}


def al_hacer_click_boton(boton, entrada_expresion, historial, canvas, toolbar, DB=modelo_db.db.reference('/historial')):
    texto_actual = entrada_expresion.get()
    cursor_pos = entrada_expresion.index(tk.INSERT)

    if boton == 'C':
        entrada_expresion.delete(0, tk.END)
    elif boton == 'del':
        if cursor_pos > 0:
            entrada_expresion.delete(cursor_pos - 1, cursor_pos)
    elif boton == '=':
        resultado = modelo.evaluar_expresion(texto_actual)
        entrada_expresion.delete(0, tk.END)
        entrada_expresion.insert(0, resultado)
        if resultado != "Error":
            historial.insert(tk.END, f"{texto_actual} = {resultado}")
            try:
                DB.push(f"{texto_actual}={resultado}")
            except Exception as e: pass
    elif boton == 'GRAPH':
        try:
            graficar_expresion(texto_actual, historial, canvas, toolbar, DB)
        except Exception as e:
            print(e)
            mostrar_mensaje("Error al graficar, prueba una expresión de la forma x**2+3")
    elif boton == 'exp':
        entrada_expresion.insert(cursor_pos, '**')
        entrada_expresion.icursor(cursor_pos + 2)
    elif boton in ['sin', 'cos', 'tan']:
        entrada_expresion.insert(cursor_pos, f'{boton}(')
        entrada_expresion.icursor(cursor_pos + len(f'{boton}('))
    elif boton == '→':
        if cursor_pos < len(texto_actual):
            entrada_expresion.icursor(cursor_pos + 1)
    elif boton == '←':
        if cursor_pos > 0:
            entrada_expresion.icursor(cursor_pos - 1)
    else:
        entrada_expresion.insert(cursor_pos, boton)
        entrada_expresion.icursor(cursor_pos + len(boton))

def graficar_expresion(expresion, historial, canvas, toolbar, DB):
    n_expresion = expresion.replace('sin(', 'np.sin(').replace('cos(', 'np.cos(').replace('tan(', 'np.tan(').replace('π', 'np.pi')
    
    x = np.linspace(-10, 10, 4000)
    y = eval(n_expresion, {"x": x, "np": np})
    
    # Eliminar asíntotas
    y = np.where(np.abs(y) > 10**2, np.nan, y)

    canvas.figure.clf()
    ax = canvas.figure.add_subplot(111)
    ax.plot(x, y)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid(True)
    ax.set_title(f"y = {expresion}")
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    canvas.draw()

    historial.insert(tk.END, f"{expresion}")
    try:
        DB.push(expresion)
    except Exception as e: pass

def cargar_historial(event, entrada_expresion, historial):
    seleccion = historial.curselection()
    if seleccion:
        expresion = historial.get(seleccion).split('=')[0]
        entrada_expresion.delete(0, tk.END)
        entrada_expresion.insert(tk.END, expresion)

def cambiar_tema(raiz, tema, entrada_expresion, historial, botones, teclado, cargar_historial, borrar_historial, borrar_nube, subir_historial, btn_tema):
    raiz.configure(bg=tema["bg_color"])
    entrada_expresion.configure(bg=tema["entry_bg"], fg=tema["entry_fg"])
    teclado.configure(bg=tema["bg_color"])
    historial.configure(bg=tema["hist_bg"], fg=tema["hist_fg"])
    cargar_historial.configure(bg=tema["bg_color"], fg=tema["fg_color"])
    borrar_historial.configure(bg=tema["bg_color"], fg=tema["fg_color"])
    borrar_nube.configure(bg=tema["bg_color"], fg=tema["fg_color"])
    subir_historial.configure(bg=tema["bg_color"], fg=tema["fg_color"])
    btn_tema.configure(bg=tema["bg_color"], fg=tema["fg_color"])
    for boton in botones:
        boton.configure(bg=tema["button_bg"], fg=tema["button_fg"])

def mostrar_mensaje(mensaje):
    messagebox.showinfo("", mensaje)

def descargar_historial(historial):
    historial.delete(0, tk.END)
    try:
        historial_firebase = modelo_db.db.reference('/historial').get()
        for key, value in historial_firebase.items():
            historial.insert(tk.END, f"{value}")
    except Exception as e:
        excepcion = str(e)
        if excepcion.count('failed') == 1:
            mostrar_mensaje("No estás conectado a internet, solo funcionará el historial local")
        else:
            mostrar_mensaje("La base de datos está vacía")

def borrar_historial_local(historial):
    historial.delete(0, tk.END)

def borrar_baseDedatos():
    try:
        respuesta = messagebox.askquestion("¿Desea continuar?", "Esta acción va a eliminar los datos de la nube de forma permanente, permanecerán en el historial local hasta que lo borre o cierre el programa")
        if respuesta == "yes":
            modelo_db.db.reference('/historial').delete()
        else:
            pass
    except Exception as e:
        mostrar_mensaje("Debes conectarte a internet primero")

def subir_historial(historial, DB = modelo_db.db.reference('historial')): 
    for i in historial.get(0, tk.END):
        try:
            nube = modelo_db.db.reference('historial').get()
            if i in nube.values(): pass
            else:
                DB.push(i)
        except Exception as e:
            mostrar_mensaje("Debes conectarte a internet primero")
            break
