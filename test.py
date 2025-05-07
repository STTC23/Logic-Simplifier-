# Entrada de múltiples expresiones en una sola línea
enter = input("Escribe expresiones booleanas separadas por espacios:\n(usa A, B, C, not, and, or, 1, 0):\n")

# Divide la entrada en una lista de expresiones, enter: AandB not(AorB), result: "AandB", "Not(AorB)"
expresiones = enter.split()

# Procesa cada expresión individualmente
for i, expresion in enumerate(expresiones):
    simplificada = ""

    print(f"\nExpresión #{i+1}: {expresion}") #Le decimos al usuario cuál es la expresión que estamos analizando. 

    # Reglas básicas
    if expresion in ["Aand1", "1andA", "Band1", "1andB", "Cand1", "1andC"]: #Imaginemos que in es ==, pero evalúa un array o una lista
        simplificada = expresion[0]  # 0 porque tomará el primer caractér de la expresión debido a la regla, Aand1 = A 
    elif expresion in ["Aand0", "0andA", "Band0", "0andB", "Cand0", "0andC"]:
        simplificada = "0"
    elif expresion in ["Aor0", "0orA", "Bor0", "0orB", "Cor0", "0orC"]:
        simplificada = expresion[0]
    elif expresion in ["Aor1", "1orA", "Bor1", "1orB", "Cor1", "1orC"]:
        simplificada = "1"
    elif expresion in ["AandA", "BandB", "CandC"]:
        simplificada = expresion[0]
    elif expresion in ["AorA", "BorB", "CorC"]:
        simplificada = expresion[0]
    elif expresion in ["AandnotA", "notAandA", "BandnotB", "notBandB", "CandnotC", "notCandC"]:
        simplificada = "0"
    elif expresion in ["AornotA", "notAorA", "BornotB", "notBorB", "CornotC", "notCorC"]:
        simplificada = "1"
    elif expresion in ["not(notA)", "notnotA", "not(notB)", "notnotB", "not(notC)", "notnotC"]:
        simplificada = expresion[-2]  #Toma el penúltimo caracter de la expresión, 

    
       # Leyes de De Morgan
    elif expresion.startswith("not(") and expresion.endswith(")"):
        interior = expresion[4:-1]  # Quita not(...) y extrae interior, en este caso, las variables y su operador lógico, not(AandB)

        if "and" in interior:
            partes = interior.split("and") #interior = "A and B" // partes = ["A ", " B"]
            if len(partes) == 2:
                simplificada = f"not{partes[0]} or not{partes[1]}"
            else:
                simplificada = "De Morgan parcial (más de 2 variables)"
        elif "or" in interior:
            partes = interior.split("or")
            if len(partes) == 2:
                simplificada = f"not{partes[0]} and not{partes[1]}"
            else:
                simplificada = "De Morgan parcial (más de 2 variables)"
        else:
            simplificada = "No aplica De Morgan (falta 'and' o 'or')"

    else:
        simplificada = "No se puede simplificar (o formato no reconocido)."

    # Se muestra el resultado de la expresión simplificada
    print("→ Simplificación:", simplificada)
