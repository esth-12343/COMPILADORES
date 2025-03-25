import ply.lex as lex

# Lista de nombres de tokens
tokens = (
    # Strings primero para darles prioridad
    'DT_STRING',
    # Variables, constantes y tipos de datos
    'VAR_KEYWORD', 'VAR', 'CONST', 'DT_INT', 'DT_FLOAT', 'DT_CHAR', 'DT_BOOL',
    
    # Estructuras de control
    'IF', 'ELSE', 'SWITCH', 'FOR', 'WHILE', 'DO_WHILE',
    
    # Control de flujo
    'RETURN', 'BREAK', 'CONTINUE',
    
    # Operadores de flujo
    'COUT', 'CIN', 'O_IN', 'ENDLINE',
    
    # Operadores aritméticos
    'O_SUMA', 'O_REST', 'O_MULT', 'O_DIV', 'O_MOD',
    
    # Operadores relacionales
    'O_IGUALDAD', 'O_DIFERENTE', 'O_MAYOR', 'O_MENOR', 'O_MAYORIGUAL',
    
    # Símbolos especiales
    'SYM_PAR_IZQ', 'SYM_PAR_DER', 'SYM_LLAVE_IZQ', 'SYM_LLAVE_DER',
    
    # Varios
    'FUNCTION', 'E_INS', 'COM_SIMPLE', 'COM_MULTI'
)

# Expresiones regulares para tokens simples
t_O_SUMA = r'\+'
t_O_REST = r'-'
t_O_MULT = r'\*'
t_O_DIV = r'/'
t_O_MOD = r'%'
t_O_IGUALDAD = r'=='
t_O_DIFERENTE = r'!='
t_O_MAYOR = r'>'
t_O_MENOR = r'<'
t_O_MAYORIGUAL = r'>='
t_SYM_PAR_IZQ = r'\('
t_SYM_PAR_DER = r'\)'
t_SYM_LLAVE_IZQ = r'\{'
t_SYM_LLAVE_DER = r'\}'
t_O_IN = r'<<|>>'
t_ENDLINE = r';|ENDLINE'

def t_VAR_KEYWORD(t):
    r'VAR(?![a-zA-Z0-9-])'
    return t

# Tokens más complejos
def t_VAR(t):
    r'V-[a-zA-Z]+-[0-9]+'
    return t

def t_CONST(t):
    r'CT-[a-zA-Z]+-[0-9]+'
    return t

def t_DT_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_DT_INT(t):
    r'(DT-INT|[0-9]+)'
    if t.value.isdigit():
        t.value = int(t.value)
    return t

def t_DT_BOOL(t):
    r'true|false|TRUE|FALSE|0|1'
    return t

def t_DT_STRING(t):
    r'"([^"]|\n)*"'
    t.value = t.value  # Mantener las comillas
    return t

def t_IF(t):
    r'IF'
    return t

def t_RETURN(t):
    r'RETURN'
    return t

def t_COUT(t):
    r'COUT'
    return t

def t_CIN(t):
    r'CIN'
    return t

def t_FUNCTION(t):
    r'F-[a-zA-Z]+-[0-9]+'
    return t

def t_COM_SIMPLE(t):
    r'//.*'
    pass

def t_COM_MULTI(t):
    r'/\*(.|\n)*?\*/'
    pass

# Caracteres ignorados
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

def analyze_file(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            lexer.input(data)
            print(f"\nAnalizando archivo: {filename}")
            print("-" * 30)
            for tok in lexer:
                print(f"Token: {tok.type}, Valor: {tok.value}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
    except Exception as e:
        print(f"Error al leer el archivo: {str(e)}")

# Test
if __name__ == "__main__":
    filename = input("Ingrese el nombre del archivo a analizar: ")
    analyze_file(filename)
