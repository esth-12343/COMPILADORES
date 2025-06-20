import os # manipular rutas de archivos
from tokens_NEW_C import tokens_list

from graphviz import Digraph
import pandas as pd #para la manupulacion del csv
import math

# Ruta al ejecutable lol de Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Graphviz\bin'



print("\nINICIANDO\n")
print("_____________________________________________\n")

#creare una clase que pueda representar un solo simbolo y la clase arbol para gestionar los simbolos como quiera sin tener problemas con el la fuente del arbol
class simbolo:
    def __init__(martina, tipo_data, nom_sym, function, valor=None):
        # Inicialización de los atributos de la clase
        martina.tipo_data = tipo_data
        martina.nom_sym = nom_sym
        martina.function = function
        martina.valor = valor

class Arbol:
    def __init__(martina, simbolo_lexer, lexema, line, column, scotty, id, tipo_data=None, valor=None):
        # Inicialización de los atributos de la clase
        global count
        martina.id = id
        martina.lexema = lexema
        martina.simbolo_lexer = simbolo_lexer
        martina.scotty = scotty
        martina.line = line
        martina.column = column
        martina.children = []
        martina.padre = None
        martina.simbolos = []
        martina.tipo_data = tipo_data
        martina.valor = valor
# Método para agregar un símbolo al árbol
    def agregar_simbolo(martina, tipo_data, nom_sym, function, valor=None):
        simbolo_lexer = simbolo(tipo_data, nom_sym, function, valor=valor)
        martina.simbolos.append(simbolo_lexer)
        martina.tipo_data = tipo_data
        martina.valor = valor
#para representar objetos que contienen informacion sobre los tokens
#abstraccion de tokens
class tokens:
    def __init__(martina, type, lexeme, line):
        # Inicialización de los atributos de la clase
        martina.type = type
        martina.lexeme = lexeme
        martina.line = line

#lectura del csv desde la primera fila con el col=0
tabla_sintactica = pd.read_csv("TOKENS.csv", index_col=0)
count = 1


#la pila la creo y esu para un procesador de datos que ayuda al árbol, si algo no coincide se consulta a la tabla
class Pila:
    def __init__(martina, hachico, scotty):
        # Inicialización de los atributos de la clase
        global count
        martina.id = count
        martina.simboloLex = hachico
        martina.scotty = scotty
        count += 1


#para organizar y administrar los simbolos, puede almacenar nuevos simbolos
class gogosimbolo:
    def __init__(martina):
        # Inicialización de los atributos de la clase
        martina.simbolos = []

    # Método para insertar un símbolo en la lista de símbolos
    def insert(martina, simbolo_lexer):
        martina.simbolos.append(simbolo_lexer)

    # Método para buscar un símbolo por su nombre
    def lookup(martina, nom_sym):
        for simbolo_lexer in martina.simbolos:
            if simbolo_lexer.nom_sym == nom_sym:
                return simbolo_lexer
        return None

    
# Lista que almacena todos los tokens
Token = tokens_list
# Inicialización de la pila con los nodos de PROGRAMA y $
node_PROGRAMA = Pila("PROGRAMA", False)
node_dolar = Pila("$", True)
stack = [node_PROGRAMA, node_dolar]
nodo_actual = 1
i = 1
nodoPadre = Arbol("PROGRAMA", None, None, None, False, node_PROGRAMA.id)

simbolos = []
#funcion recursiva para buscar un nodo en especifico devuelve un nodo si lo encuentro o de lo contrario none
def buscar(node, id):
    if node.id == id:
        return node
    for c in node.children:
        found_node = buscar(c, id)
        if found_node is not None:
            return found_node
    return None
# Función para generar y representar el árbol sintáctico
def arbolSintactico(raiz):
    lol = Digraph()
#para generar los nodos del arbol sintactico
#constructor de etiquetas que se usaran para cada nodo del arbol
    def generar_nodos(node):
        label = f"{node.simbolo_lexer}"
        if node.line is not None:
            label += f"\nline: {node.line}"
        if node.column is not None:
            label += f"\ncol: {node.column}"
        if node.valor is not None:
            label += f"\nvalor: {node.valor}"

        lol.node(str(node.id), label, style="filled", fillcolor='white')

        if node.padre:
            lol.edge(str(node.padre.id), str(node.id))

        for child in node.children:
            generar_nodos(child)

    generar_nodos(raiz)
    return lol
#para poder imprimir la tabla ll1
def imprimirTablaLL1(tabla_ll1):
    print("\nIMPRESION DEL ARCHIVO CSV:\n")
    print("_____________________________________________\n")
    print(tabla_ll1)
    
    print("\nTABLA LL1 :\n")
    print("_____________________________________________\n")
    for non_terminal, row in tabla_ll1.iterrows():
        print(non_terminal, end=' | ')
        for scotty, jiafeiuccion in row.items():
            #indice de la columna seguido de su valor
            print(f'{scotty}: {jiafeiuccion}', end=' | ')
        print()

# Variable para controlar si se produce un error
error = False

# Variable que parece no utilizarse más adelante en el código
simone = 0

# Lista para almacenar los tokens procesados
t = []

# Iterar sobre cada token en la lista Token
for token_actual in Token:
    # Agregar el token actual a la lista t
    t.append(token_actual)

# Ciclo while que se ejecuta indefinidamente hasta que se cumple una condición y se rompe con 'break'
while True:
    # Comprobar si el símbolo en la cima de la pila es '$' y el tipo del primer token es '$'
    if stack[0].simboloLex == "$" and Token[0].type == "$":
        # Si se cumple, imprimir un mensaje indicando que todo  bien y salir del bucle while
        print("_____________________________________________\n")
        print("TODO BIEN")
        print("_____________________________________________\n")
        break

    # Si no se cumple la condición anterior, comprobar si el símbolo en la cima de la pila es un no-terminal
    # y coincide con el tipo del primer token
    elif stack[0].scotty and stack[0].simboloLex == Token[0].type:
        # Si coincide, eliminar el símbolo en la cima de la pila y el primer token de la lista de tokens
        stack.pop(0)
        token = Token.pop(0)
        # Asignar el tipo de datos del siguiente token al nodo actual en el árbol sintáctico
        tipo_data = Token[0].type
        # Verificar si el tipo de datos es distinto de None (es decir, si hay un tipo de datos válido)
        if tipo_data is not None:
            # Buscar el nodo padre actual en el árbol sintáctico y asignarle el tipo de datos
            padre = buscar(nodoPadre, nodo_actual)
            #Ayuda a mantener actualizada la informacion del tipo de datos en el árbol
            padre.tipo_data = tipo_data


    elif stack[0].scotty and stack[0].simboloLex != Token[0].type:
        print("NO RECONOCE")
        print("_____________________________________________\n")
        error = True
        break
    else:
        jiafei = tabla_sintactica.loc[stack[0].simboloLex][Token[0].type]

        if jiafei == "e":
            stack.pop(0)
        else:
            if isinstance(jiafei, float) and math.isnan(jiafei):
                print("NO RECONOCE")
                print("_____________________________________________\n")
                error = True
                break
            else:
                jiafei = jiafei.split(" ")
                padre_stack = stack.pop(0)

                padre = buscar(nodoPadre, padre_stack.id)
                #creacion y actualizacion de los nodos del árbol
                for Symlexer in jiafei[::-1]:
                    is_terminal = Symlexer in tabla_sintactica.columns
                    node = Pila(Symlexer, is_terminal)
                    stack.insert(0, node)
                    nodo_actual = node.id
                    
                    nod = Arbol(Symlexer, None, None, None, is_terminal, node.id)
                    #vamos creando nuevos nodos en el nodo padre
                    padre.children.insert(0, nod)
                    nod.padre = padre

                    if nod.scotty:
                        for token_actual in t:
                            if token_actual.type == nod.simbolo_lexer:
                                nod.valor = token_actual.lexeme
                                nod.line = token_actual.line
                                nod.column = token_actual.column
                                t.remove(token_actual)
                                break

# Si no hay errores en el análisis sintáctico
if not error:
    # Imprimir la tabla LL1 de manera legible
    imprimirTablaLL1(tabla_sintactica)
    # Generar el árbol sintáctico
    lol = arbolSintactico(nodoPadre)
    # Renderizar el árbol sintáctico en formato PNG y guardarlo como 'arbolSintactico.png'
    lol.render('arbolSintactico', format='png', view=True)


