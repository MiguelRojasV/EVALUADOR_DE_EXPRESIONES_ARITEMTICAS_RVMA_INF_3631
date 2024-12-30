import re
import sys
from enum import Enum

# Diccionario de palabras reservadas
PALABRAS_RESERVADAS = {
    "var": "PALABRA_RESERVADA",
    "mostrar": "PALABRA_RESERVADA",
    "si": "PALABRA_RESERVADA",
    "entonces": "PALABRA_RESERVADA",
    "fin": "PALABRA_RESERVADA",
    "sen": "PALABRA_RESERVADA",
    "cos": "PALABRA_RESERVADA",
    "raiz": "PALABRA_RESERVADA",
    "logd": "PALABRA_RESERVADA",
    "logn": "PALABRA_RESERVADA",
}

# Diccionario de operadores matemáticos
OPERADORES_MATEMATICOS = {
    "sum": "OPERADOR",  # Suma
    "res": "OPERADOR",  # Resta
    "pro": "OPERADOR",  # Producto
    "div": "OPERADOR",  # División
    "pot": "OPERADOR",  # Potencia
    "mod": "OPERADOR",  # Módulo
}

# Patrones para los tokens
PATRONES_TOKEN = {
    'comparador': r"(>=|<=|==|!=|>|<)",   # Operadores de comparación
    'asignacion': r"(=|\+=|\-=|\*=|/=|%=)", # Operadores de asignación
    'operador': r"[\+\-\*/\^%]",            # Operadores matemáticos básicos
    'parentesis': r"[()]",                 # Paréntesis
    'coma': r",",                          # Comas
    'punto_y_coma': r";",                  # Punto y coma
    'entero': r"\b\d+\b",                  # Números enteros
    'real': r"\b\d+\.\d+\b",               # Números reales
    'identificador': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",  # Identificadores
}

# Enumeración para tipos de token
class TipoToken(Enum):
    PALABRA_RESERVADA = 1
    COMPARADOR = 2
    ASIGNACION = 3
    OPERADOR = 4
    PARENTESIS = 5
    COMA = 6
    PUNTO_Y_COMA = 7
    ENTERO = 8
    REAL = 9
    IDENTIFICADOR = 10

# Analizador léxico
class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.errores = []

    def analizar(self):
        lineas = self.codigo.split('\n')
        for numero_linea, linea in enumerate(lineas, start=1):
            columna = 1
            while linea:
                linea = linea.lstrip()  # Eliminar espacios al inicio
                columna_inicial = columna + (len(linea) - len(linea.lstrip()))

                if not linea:  # Si la línea está vacía, terminar el análisis
                    break

                match = None
                for token_nombre, patron in PATRONES_TOKEN.items():
                    regex = re.compile(patron)
                    match = regex.match(linea)

                    if match:
                        valor = match.group(0)
                        # Si el valor es una palabra reservada o un operador matemático
                        if token_nombre == 'identificador' and valor in PALABRAS_RESERVADAS:
                            self.tokens.append((valor, PALABRAS_RESERVADAS[valor], numero_linea, columna_inicial))
                        elif valor in OPERADORES_MATEMATICOS:
                            self.tokens.append((valor, OPERADORES_MATEMATICOS[valor], numero_linea, columna_inicial))
                        else:
                            self.tokens.append((valor, TipoToken[token_nombre.upper()].name, numero_linea, columna_inicial))
                        linea = linea[len(valor):].lstrip()  # Continuar con el análisis
                        columna = columna_inicial + len(valor)
                        break

                if not match:  # Si no se encontró un token válido
                    self.errores.append((linea[0], numero_linea, columna_inicial))
                    linea = linea[1:].lstrip()
                    columna += 1

        return self.tokens, self.errores

if __name__ == '__main__':
    if len(sys.argv) > 1:
        archivo_nombre = sys.argv[1]
        try:
            with open(archivo_nombre, 'r') as archivo:
                codigo = archivo.read()

            analizador = AnalizadorLexico(codigo)
            tokens, errores = analizador.analizar()

            # Guardar tokens en un archivo
            with open('resultados.txt', 'w', encoding='utf-8') as archivo_resultados:
                archivo_resultados.write("Tokens:\n")
                for token in tokens:
                    archivo_resultados.write(f"{token[0]:<20} {token[1]:<20} Linea: {token[2]} Columna: {token[3]}\n")

            # Guardar errores léxicos en un archivo
            with open('errores_lexicos.txt', 'w', encoding='utf-8') as archivo_errores:
                if errores:
                    archivo_errores.write("Errores léxicos:\n")
                    for error in errores:
                        archivo_errores.write(f"Caracter inesperado '{error[0]}' en linea {error[1]}, columna {error[2]}\n")
                else:
                    archivo_errores.write("No se encontraron errores léxicos.\n")

            print("Análisis léxico completado. Archivos 'resultados.txt' y 'errores_lexicos.txt' generados.")

        except FileNotFoundError:
            print(f"El archivo {archivo_nombre} no fue encontrado.")
    else:
        print("Debe proporcionar el nombre de un archivo como argumento.")
