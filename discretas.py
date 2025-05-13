import tkinter as tk
from tkinter import ttk
from sympy import symbols, simplify_logic, Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import BooleanFunction
import itertools
import re

# Declarar los símbolos
A, B, C, D = symbols('A B C D')
historial_pasos = {}

def simplificar():
    entrada_original = entrada_expr.get()
    forma = forma_simplificacion.get()
    try:
        paso_1 = entrada_original
        entrada = entrada_original.replace("¬", "~").replace("^", "&").replace("v", "|")
        paso_2 = entrada

        while "NAND(" in entrada or "NOR(" in entrada:
            entrada = reemplazar_operador_personalizado(entrada, "NAND", "&")
            entrada = reemplazar_operador_personalizado(entrada, "NOR", "|")
        paso_3 = entrada

        expr = parse_expr(entrada, evaluate=False)
        paso_4 = str(expr)

        simplificada = simplify_logic(expr, form=forma)
        paso_5 = str(simplificada)

        salida.set(f"Simplificado ({forma.upper()}):\n{simplificada}")

        historial_pasos.clear()
        historial_pasos.update({
            "Original": paso_1,
            "Reemplazo de símbolos (¬,^,v)": paso_2,
            "Traducción NAND/NOR": paso_3,
            "Expresión parseada": paso_4,
            "Simplificado": paso_5
        })
    except Exception as e:
        salida.set(f"Error: {str(e)}")
        historial_pasos.clear()

def reemplazar_operador_personalizado(texto, operador, op_simbolo):
    patron = rf'{operador}\(([^,]+),([^,\)]+)\)'
    return re.sub(patron, lambda m: f'~({m.group(1).strip()} {op_simbolo} {m.group(2).strip()})', texto)

def limpiar():
    entrada_expr.delete(0, tk.END)
    salida.set("")
    historial_pasos.clear()

def insertar_simbolo(simbolo):
    if simbolo == '↑':
        entrada_expr.insert(tk.INSERT, 'NAND(A,B)')
    elif simbolo == '↓':
        entrada_expr.insert(tk.INSERT, 'NOR(A,B)')
    else:
        entrada_expr.insert(tk.INSERT, simbolo)

def mostrar_pasos():
    if not historial_pasos:
        return

    ventana_pasos = tk.Toplevel()
    ventana_pasos.title("Paso a paso de la simplificación")
    ventana_pasos.geometry("600x300")
    ventana_pasos.configure(bg="#2a2a3b")

    tk.Label(ventana_pasos, text="🧩 PASO A PASO", font=("Segoe UI", 14, "bold"), fg="#00ffcc", bg="#2a2a3b").pack(pady=10)

    for clave, valor in historial_pasos.items():
        tk.Label(ventana_pasos, text=f"{clave}:", fg="white", bg="#2a2a3b", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x", padx=10)
        tk.Label(ventana_pasos, text=valor, fg="#00ffcc", bg="#2a2a3b", anchor="w", font=("Courier New", 10), wraplength=560, justify="left").pack(fill="x", padx=20, pady=2)

def mostrar_tabla_verdad():
    if not historial_pasos or "Expresión parseada" not in historial_pasos:
        return

    expr_str = historial_pasos["Expresión parseada"]

    try:
        expr = parse_expr(expr_str, evaluate=False)
        variables = sorted(expr.free_symbols, key=lambda s: str(s))
        tabla = []

        for valores in itertools.product([False, True], repeat=len(variables)):
            asignacion = dict(zip(variables, valores))
            resultado = expr.subs(asignacion)
            tabla.append([int(val) for val in valores] + [int(bool(resultado))])

        ventana_tabla = tk.Toplevel()
        ventana_tabla.title("Tabla de Verdad")
        ventana_tabla.configure(bg="#2a2a3b")
        ventana_tabla.geometry("700x400")

        encabezado = [str(v) for v in variables] + ["Resultado"]
        for col, titulo in enumerate(encabezado):
            tk.Label(ventana_tabla, text=titulo, bg="#1e1e2f", fg="#00ffcc", width=10, relief=tk.RIDGE).grid(row=0, column=col)

        for fila_idx, fila in enumerate(tabla, start=1):
            for col_idx, valor in enumerate(fila):
                tk.Label(ventana_tabla, text=str(valor), bg="#333", fg="white", width=10, relief=tk.RIDGE).grid(row=fila_idx, column=col_idx)

    except Exception as e:
        print(f"Error al mostrar tabla de verdad: {e}")

# Interfaz principal 1
BG_COLOR = "#1e1e2f"
FG_COLOR = "#f1f1f1"
BUTTON_COLOR = "#0078D7"
HIGHLIGHT = "#00ffcc"

ventana = tk.Tk()
ventana.title("Simplificador Lógico con Flechas, Tabla y Pasos")
ventana.geometry("780x600")
ventana.configure(bg=BG_COLOR)

tk.Label(ventana, text="🧠 Simplificador de Expresiones Lógicas", bg=BG_COLOR, fg=HIGHLIGHT, font=("Segoe UI", 16, "bold")).pack(pady=10)
tk.Label(ventana, text="Usa (&, |, ~) o (^, v, ¬), también NAND↑ y NOR↓", bg=BG_COLOR, fg=FG_COLOR).pack()

entrada_expr = tk.Entry(ventana, width=70, font=("Consolas", 12), bg="#2b2b3d", fg=FG_COLOR, insertbackground="white", relief=tk.FLAT)
entrada_expr.pack(pady=10)

tk.Label(ventana, text="Teclado de símbolos", bg=BG_COLOR, fg=HIGHLIGHT, font=("Segoe UI", 10, "bold")).pack()
teclado_frame = tk.Frame(ventana, bg=BG_COLOR)
teclado_frame.pack()

simbolos = ['A', 'B', 'C', 'D', '(', ')', '¬', '^', 'v', '&', '|', '↑', '↓']
for i, simbolo in enumerate(simbolos):
    btn = tk.Button(teclado_frame, text=simbolo, width=4 if simbolo not in ['↑', '↓'] else 6,
                    font=("Segoe UI", 10, "bold"), command=lambda s=simbolo: insertar_simbolo(s),
                    bg="#333", fg=HIGHLIGHT, relief=tk.RAISED)
    btn.grid(row=i//7, column=i%7, padx=5, pady=5)

forma_simplificacion = tk.StringVar(value="dnf")
forma_frame = tk.Frame(ventana, bg=BG_COLOR)
forma_frame.pack(pady=5)
tk.Label(forma_frame, text="Forma:", bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT)
ttk.Combobox(forma_frame, textvariable=forma_simplificacion, values=["dnf", "cnf"], width=6).pack(side=tk.LEFT, padx=5)

botones_frame = tk.Frame(ventana, bg=BG_COLOR)
botones_frame.pack(pady=10)
tk.Button(botones_frame, text="Simplificar", command=simplificar, bg=BUTTON_COLOR, fg="white", width=12).pack(side=tk.LEFT, padx=10)
tk.Button(botones_frame, text="Ver paso a paso", command=mostrar_pasos, bg="#5cb85c", fg="white", width=14).pack(side=tk.LEFT, padx=10)
tk.Button(botones_frame, text="Ver tabla de verdad", command=mostrar_tabla_verdad, bg="#f0ad4e", fg="white", width=18).pack(side=tk.LEFT, padx=10)
tk.Button(botones_frame, text="Limpiar", command=limpiar, bg="#D9534F", fg="white", width=10).pack(side=tk.LEFT, padx=10)

salida = tk.StringVar()
tk.Label(ventana, textvariable=salida, bg="#2a2a3b", fg=HIGHLIGHT, font=("Courier New", 11), width=85, height=6, wraplength=680, justify="left", relief=tk.RIDGE, bd=2).pack(pady=15)

ventana.mainloop()




