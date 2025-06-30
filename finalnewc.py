from sintacticonewc import nodoPadre
from semanticonewc import symbol_table

print("\nComenzando Analizar el archivo ( ensamblador)\n")
# Definición de una excepción personalizada
class TypeDataError(Exception):
    pass
# Función para agregar instrucciones al código assembly
def generar_assembly(instruccion):
    global codigo_assembly
    codigo_assembly.append(instruccion)

codigo_assembly = []
# Función para agregar instrucciones a la pila de expresiones
def agrear_pila(instruccion):
    global pila_expresion
    pila_expresion.append(instruccion)

pila_expresion = []
# Inicialización del segmento de datos en el código assembly
codigo_assembly.append(".data")


# Iterar sobre la tabla de símbolos y definir variables de tipo entero en el scope específico
for simbolo in symbol_table.symbols:
    if simbolo['is_function'] == False and simbolo['data_type'] == "inty" and simbolo['scope'] == "jiafei_your_queen":
        generar_assembly(f"    var_{simbolo['name']}: .word 0:1")

# Inicialización del segmento de texto en el código assembly
codigo_assembly.append(".text")

# Variables globales para manejar el estado
acum_pila = True

tipo_prev = None

op_actual = []
signo_actual = ""

# Función recursiva para verificar si un nodo tiene un ancestro específico
def el_muy_antiguo(nodo, tata):
    if nodo.simbolo_lexer == tata:
        return True
    
    if nodo.padre is None:
        return False

    return el_muy_antiguo(nodo.padre, tata)

# Función recursiva para recorrer el árbol de sintaxis
def recorrer_arbol(nodo):
    global tipo_prev
    global tipo_actual
    global scope_actual
    global tipo_scope_actual


    global acum_pila
    global variable_actual
    global op_actual
    global signo_actual

    if nodo.simbolo_lexer == "FUNCTION":
        tipo_scope_actual = nodo.children[0].children[0].children[0].valor
        scope_actual = nodo.children[2].valor
        if nodo.children[2].valor != "principal":
            generar_assembly(f"    move $fp $sp")
            
            generar_assembly(f"\n    sw $ra 0($sp)")
            generar_assembly(f"    addiu $sp $sp -4")

            generar_assembly(f"\n    lw $a0, 8($sp)")


    elif nodo.simbolo_lexer == "Crear_variables":
        variable_actual = nodo.children[1].valor

    elif nodo.simbolo_lexer == "Asig_varibles":
        variable_actual = nodo.children[0].valor

    # LUEGO DEL IGUAL =

    elif nodo.simbolo_lexer == "E":
        if nodo.children[0].simbolo_lexer == "CADENA":
            nombre_variable = nodo.children[0].valor
            tipo_actual = nombre_variable

    elif nodo.simbolo_lexer == "FH":
        if nodo.children[0].simbolo_lexer == "NUMERO":
            nombre_variable = nodo.children[0].valor
            tipo_actual = nombre_variable
            generar_assembly(f"    li $a0, {nodo.children[0].valor}")

        elif nodo.children[0].simbolo_lexer == "DECIMAL":
            nombre_variable = nodo.children[0].valor
            tipo_actual = nombre_variable

        elif nodo.children[0].simbolo_lexer == "ID":
            nombre_variable = nodo.children[0].valor
            info_variable = symbol_table.lookup(nombre_variable, scope_actual)
            if info_variable and 'name' in info_variable:
                tipo_actual = info_variable['name']
                if info_variable['scope'] == "principal":
                    generar_assembly(f"\n    la $t0, var_{info_variable['name']}")
                    generar_assembly(f"    lw $a0, 0($t0)")
            else:
                info_variable = symbol_table.lookup(nombre_variable, "global")
                if info_variable and 'data_type' in info_variable:
                    tipo_actual = info_variable['data_type']

    elif nodo.simbolo_lexer in ["SUMA", "RESTA", "MULTIPLICAR", "DIVIDIR"]:
        tipo_prev = tipo_actual

        op_actual = [] 

        if nodo.simbolo_lexer == "SUMA":
            op_actual.append(f"    add $a0 $t1 $a0 # SUMAR")
        if nodo.simbolo_lexer == "RESTA":
            op_actual.append(f"    sub $a0 $t1 $a0 # RESTAR")
        if nodo.simbolo_lexer == "MULTIPLICAR":
            op_actual.append(f"    mult $t1 $a0 # MULTIPLICAR")
            op_actual.append(f"    mflo $a0")
        if nodo.simbolo_lexer == "DIVIDIR":
            op_actual.append(f"    div $t1, $a0 # DIVIDIR")
            op_actual.append(f"    mflo $a0")

    if nodo.simbolo_lexer == "E'":
        if nodo.children:
            if acum_pila: 
                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n")
                acum_pila = False
            else: 
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n ")

                acum_pila = False
        else:
            if nodo.padre.simbolo_lexer != "E":
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                acum_pila = True

    if nodo.simbolo_lexer == "T'":
        if nodo.children:
            if acum_pila: 
                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n")
                acum_pila = False
            else: 
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n ")

                acum_pila = False
        else:
            if nodo.padre.simbolo_lexer != "T":
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP 2")
                acum_pila = True
        
    if nodo.simbolo_lexer == "E'":
        if not nodo.children:
            tipo_prev = tipo_scope_actual
            generar_assembly(f"")

            if not el_muy_antiguo(nodo, "RTN"):
                generar_assembly(f"    la  $t1, var_{variable_actual}")
                generar_assembly(f"    sw  $a0, 0($t1)\n")

    elif nodo.simbolo_lexer == "ID":
        if nodo.padre.simbolo_lexer == "TX":
            generar_assembly(f"\n    # Imprimir {nodo.valor}:")
            generar_assembly(f"    lw $a0, var_{nodo.valor}")
            generar_assembly(f"    li $v0, 1")
            generar_assembly(f"    syscall")

    # Llamado de funciones

    if nodo.simbolo_lexer == "FN":
        if nodo.children and nodo.padre.children[0].simbolo_lexer == "ID":
            generar_assembly(f"\n    # invocacion a una funcion")
            generar_assembly(f"    sw $fp 0($sp)")
            generar_assembly(f"    addiu $sp $sp-4")

    if nodo.simbolo_lexer == "F'":
        if el_muy_antiguo(nodo, "FN"):
            generar_assembly(f"\n    # generamos codigo para cada parametro")
            generar_assembly(f"    li $a0, {nodo.children[0].valor}")

            generar_assembly(f"\n    # metemos el parametro a la pila")
            generar_assembly(f"    sw $a0 0($sp)")
            generar_assembly(f"    addiu $sp $sp-4")

    if nodo.simbolo_lexer == "PARENTESIS_CERRADO":
        if nodo.padre.simbolo_lexer == "FN":
            if nodo.padre.padre.children[0].simbolo_lexer == "ID":
                generar_assembly(f"\n    jal {nodo.padre.padre.children[0].valor} # invocamos a la funcion\n")

    # Condicionales


    if nodo.simbolo_lexer == "F":
        if nodo.children:
            signo_actual = nodo.children[0].simbolo_lexer

    if nodo.simbolo_lexer == "F'":
        if nodo.children[0].simbolo_lexer == "ID" and nodo.padre.simbolo_lexer == "H":

            generar_assembly(f"\n    # e_1")
            generar_assembly(f"    la $t0, var_{nodo.children[0].valor}")
            generar_assembly(f"    lw $a0, 0($t0)")

            generar_assembly(f"\n    # push")
            generar_assembly(f"    sw $a0, 0($sp)")
            generar_assembly(f"    add $sp, $sp, -4")
            
        if nodo.children[0].simbolo_lexer == "NUMERO" and nodo.padre.simbolo_lexer == "H":

            generar_assembly(f"\n    # e_2")
            generar_assembly(f"    li $a0, {nodo.children[0].valor}")

            generar_assembly(f"\n    # comparacion")
            generar_assembly(f"    lw $t1, 4($sp)")
            generar_assembly(f"    add $sp, $sp, 4")

            if signo_actual == "MENOR":
                generar_assembly(f"    blt $a0, $t1, label_false\n")
            if signo_actual == "MAYOR":
                generar_assembly(f"    bgt $a0, $t1, label_false\n")
            if signo_actual == "MENOR_IGUAL":
                generar_assembly(f"    ble $a0, $t1, label_false\n")
            if signo_actual == "MAYOR_IGUAL":
                generar_assembly(f"    bge $a0, $t1, label_false\n")
            if signo_actual == "IGUAL_IGUAL":
                generar_assembly(f"    bne $a0, $t1, label_false\n")
            if signo_actual == "DIFERENTE":
                generar_assembly(f"    beq $a0, $t1, label_false\n")

            generar_assembly(f"label_true:")

    if nodo.simbolo_lexer == "ELS":
        if not nodo.children:
            generar_assembly(f"label_false:")
            generar_assembly(f"\nlabel_end:")
        else:
            generar_assembly(f"label_false:")

    if nodo.simbolo_lexer == "LLAVE_CERRADO":
        if nodo.padre.children[0].simbolo_lexer == "IF":
            generar_assembly(f"    b label_end\n")
        elif nodo.padre.children[0].simbolo_lexer == "ELSE":
            generar_assembly(f"label_end:\n")
        elif nodo.padre.simbolo_lexer == "FUNCTION":
            if nodo.padre.children[2].valor == "principal":
                generar_assembly(f"\n    # Finalizar el main:")
                generar_assembly(f"    li $v0, 10")
                generar_assembly(f"    syscall ")
            else:
                generar_assembly(f"\n    lw $ra 4($sp)")
                generar_assembly(f"    addiu $sp $sp 12 # 12 = 4*num_param + 8 ")
                generar_assembly(f"    lw $fp 0($sp)")
                generar_assembly(f"    jr $ra")

    if nodo.simbolo_lexer != "PROGRAMA":
            for child in nodo.children:
                recorrer_arbol(child)

try:
    def recorrer_arbol_al_reves(nodo):
        if nodo is not None:

            for child in reversed(nodo.children):
                recorrer_arbol_al_reves(child)

        if nodo.simbolo_lexer == "FUNCTION":
            generar_assembly(f"{nodo.children[2].valor}:")
            recorrer_arbol(nodo) # Desde donde se va a recorrer

    recorrer_arbol_al_reves(nodoPadre)
# Guardar el código assembly en un archivo
    with open('ensamblador_final.asm', 'w') as f:
        for linea in codigo_assembly:
            f.write(linea + '\n')
            print(linea)
# Mensaje de éxito
    print(f"\nfinalizacion exitosa")

except TypeDataError as e:
    print(f"\nError: {e}")