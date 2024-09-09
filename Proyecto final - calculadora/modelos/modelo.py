import math
import numpy as np

def evaluar_expresion(expresion):
    try:
        #evalua si hay expresiones que requieren numpy
        if 'sin(' in expresion:
            n_expresion = expresion.replace('sin(', 'np.sin(')
            
        elif 'cos(' in expresion :
            n_expresion = expresion.replace('cos(', 'np.cos(')
        elif'tan(' in expresion:
            n_expresion = expresion.replace('tan(', 'np.tan(')
        elif 'π' in expresion:
            n_expresion = expresion.replace('π', 'np.pi')
        else: n_expresion = expresion
        resultado = eval(n_expresion, {"np": np})
        return resultado
    except Exception as e:
        return f"Error"
