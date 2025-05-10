import tkinter as tk
from sympy import symbols, simplify_logic
from sympy.parsing.sympy_parser import parse_expr


# Declarar símbolos lógicos
A, B, C, D = symbols('A B C D')

def simplificar():
    entrada = entrada_expr.get()
    try:
        # Reemplazar ¬ por ~ para negación lógica
        entrada = entrada.replace("¬", "~")
        expr = parse_expr(entrada, evaluate=False)
        simplificada = simplify_logic(expr, form='dnf')
        salida.set(f"Simplificado: {str(simplificada)}")
    except Exception as e:
        salida.set(f"Error: {str(e)}")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Simplificador de Expresiones Lógicas")

tk.Label(ventana, text="Puedes usar la siguiente simbología (usa (&, |,~) o (^, v, ¬) ):").pack()
entrada_expr = tk.Entry(ventana, width=40)
entrada_expr.pack()
tk.Button(ventana, text="Simplificar", command=simplificar).pack(pady=5)
salida = tk.StringVar()
tk.Label(ventana, textvariable=salida).pack(pady=10)

ventana.mainloop()
