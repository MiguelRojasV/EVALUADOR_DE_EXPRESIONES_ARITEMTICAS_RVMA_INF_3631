import sys
from enum import Enum

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

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errores = []
        self.indice_actual = 0

    def token_actual(self):
        """Devuelve el token actual, si hay más tokens."""
        if self.indice_actual < len(self.tokens):
            return self.tokens[self.indice_actual]
        return None

    def avanzar(self):
        """Avanza al siguiente token."""
        if self.indice_actual < len(self.tokens):
            self.indice_actual += 1

    def consumir(self, tipo_esperado):
        """Consume el token actual si coincide con el tipo esperado, si no, lanza un error sintáctico."""
        token = self.token_actual()
        if token and token[1] == tipo_esperado:
            self.avanzar()
        else:
            if token:
                self.errores.append(f"Error sintáctico: se esperaba {tipo_esperado.name} pero se encontró '{token[0]}' en línea {token[2]}")
            else:
                self.errores.append(f"Error sintáctico: se esperaba {tipo_esperado.name} pero no se encontró ningún token.")

    def analizar(self):
        """Inicia el análisis sintáctico de los tokens."""
        while self.token_actual():
            token = self.token_actual()
            if token[0] == "var":
                self.analizar_declaracion()
            elif token[0] == "mostrar":
                self.analizar_mostrar()
            elif token[0] == "si":
                self.analizar_condicional()
            elif token[0] == "fin":
                self.avanzar()
            else:
                self.errores.append(f"Error sintáctico: token inesperado '{token[0]}' en la línea {token[2]}")
                self.avanzar()

    def analizar_declaracion(self):
        """Analiza una declaración de variable."""
        self.consumir(TipoToken.PALABRA_RESERVADA)  # 'var'
        self.consumir(TipoToken.IDENTIFICADOR)     # identificador
        self.consumir(TipoToken.ASIGNACION)        # '='
        self.analizar_expresion()                   # Expresión
        self.consumir(TipoToken.PUNTO_Y_COMA)      # ';'

    def analizar_mostrar(self):
        """Analiza una instrucción 'mostrar'."""
        self.consumir(TipoToken.PALABRA_RESERVADA)  # 'mostrar'
        self.consumir(TipoToken.IDENTIFICADOR)      # identificador
        self.consumir(TipoToken.PUNTO_Y_COMA)       # ';'

    def analizar_condicional(self):
        """Analiza una estructura condicional 'si'."""
        self.consumir(TipoToken.PALABRA_RESERVADA)  # 'si'
        self.consumir(TipoToken.PARENTESIS)         # '('
        self.analizar_expresion()                    # Expresión
        self.consumir(TipoToken.COMPARADOR)         # Comparador
        self.analizar_expresion()                    # Expresión
        self.consumir(TipoToken.PARENTESIS)         # ')'
        self.consumir(TipoToken.PALABRA_RESERVADA)  # 'entonces'
        self.analizar_bloque()                      # Analiza el bloque de instrucciones
        self.consumir(TipoToken.PALABRA_RESERVADA)  # 'fin'

    def analizar_bloque(self):
        """Analiza un bloque de instrucciones dentro de 'si' u otros bloques."""
        while self.token_actual() and self.token_actual()[0] != "fin":
            token = self.token_actual()
            if token[0] == "var":
                self.analizar_declaracion()
            elif token[0] == "mostrar":
                self.analizar_mostrar()
            elif token[0] == "si":
                self.analizar_condicional()
            else:
                self.errores.append(f"Error sintáctico: token inesperado '{token[0]}' en la línea {token[2]}")
                self.avanzar()

    def analizar_expresion(self):
        """Analiza una expresión aritmética o llamada a función."""
        token = self.token_actual()
        if token and token[1] in {TipoToken.IDENTIFICADOR, TipoToken.ENTERO, TipoToken.REAL}:
            self.avanzar()  # Avanzamos al siguiente token
            while self.token_actual() and self.token_actual()[1] == TipoToken.OPERADOR:
                self.avanzar()  # Avanzamos por los operadores
                self.analizar_expresion()  # Expresión recursiva
        elif token and token[1] == TipoToken.PARENTESIS:
            self.consumir(TipoToken.PARENTESIS)  # '('
            self.analizar_expresion()            # Expresión dentro de paréntesis
            self.consumir(TipoToken.PARENTESIS)  # ')'
        elif token and token[1] == TipoToken.PALABRA_RESERVADA:
            if token[0] in {"sen", "cos", "raiz", "logd", "logn"}:  # Funciones matemáticas
                self.avanzar()  # Nombre de la función
                self.consumir(TipoToken.PARENTESIS)  # '('
                self.analizar_expresion()  # Argumento de la función
                self.consumir(TipoToken.PARENTESIS)  # ')'
            elif token[0] in {"sum", "res", "pro", "div", "pot", "mod"}:  # Operadores matemáticos
                self.avanzar()  # Operador
                self.analizar_expresion()  # Expresión siguiente
            else:
                self.errores.append(f"Error sintáctico: función u operador desconocido '{token[0]}' en línea {token[2]}")
        else:
            self.errores.append(f"Error sintáctico: expresión inválida en línea {token[2]}")

if __name__ == '__main__':
    try:
        with open('resultados.txt', 'r', encoding='utf-8') as archivo_tokens:
            tokens = []
            for linea in archivo_tokens:
                if linea.startswith("Tokens:"):
                    continue
                partes = linea.split()
                if len(partes) >= 3:
                    token_valor = partes[0]
                    token_tipo = partes[1]
                    token_linea = int(partes[-1].replace("Linea:", ""))
                    tokens.append((token_valor, TipoToken[token_tipo.upper()], token_linea))

        analizador = AnalizadorSintactico(tokens)
        analizador.analizar()

        with open('errores_sintaxis.txt', 'w', encoding='utf-8') as archivo_errores:
            if analizador.errores:
                archivo_errores.write("Errores sintácticos:\n")
                for error in analizador.errores:
                    archivo_errores.write(f"{error}\n")
            else:
                archivo_errores.write("No se encontraron errores sintácticos.\n")

        print("Análisis sintáctico completado. Resultados guardados en 'errores_sintaxis.txt'.")
    except FileNotFoundError:
        print("El archivo 'resultados.txt' no fue encontrado. Ejecute el analizador léxico primero.")
