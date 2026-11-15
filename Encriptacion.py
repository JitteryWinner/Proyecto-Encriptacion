#Logica del progrma
# Verifica si un numero es primo
def esprimo(numero):
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True

# Se Calcula el MCD de dos números
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Se Calcula la potencia modular de un numero
def potenciamodular(base, exponente, modulo):
    resultado = 1
    base = base % modulo
    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente = exponente // 2
    return resultado


def encriptar(mensaje, p, q, e):
    # Revisar los datos antes de hacer calculos.
    if not isinstance(mensaje, str) or mensaje == "":
        raise ValueError("Escribe un mensaje que no este vacio.")
    if type(p) is not int or type(q) is not int or type(e) is not int:
        raise ValueError("p, q y e deben ser numeros enteros.")
    if not esprimo(p) or not esprimo(q) or p == q:
        raise ValueError("p y q deben ser numeros primos diferentes.")

    n = p * q
    phi = (p - 1) * (q - 1)
    if not 126126 < n < 1000000:
        raise ValueError("n = p * q debe ser mayor que 126126 y menor que 1000000.")
    if e <= 1 or mcd(e, phi) != 1:
        raise ValueError("e debe ser mayor que 1 y su MCD con phi debe ser 1.")

    for caracter in mensaje:
        if not 32 <= ord(caracter) <= 126:
            raise ValueError("Solo se permiten caracteres ASCII del 32 al 126 (No se pueden tildes ni la ñ).")

    # Longitud antes de agregar relleno

    longitud = len(mensaje)  
    relleno = longitud % 2 == 1
    texto = mensaje
    if relleno:
        texto += " "

# 
    codigos_ascii = []
    bloques_originales = []
    bloques_cifrados = []

    for i in range(0, len(texto), 2):
        caracter1 = texto[i]
        caracter2 = texto[i + 1]
        codigo1 = f"{ord(caracter1):03d}"
        codigo2 = f"{ord(caracter2):03d}"
        bloque = codigo1 + codigo2
        numero = int(bloque)
        cifrado = potenciamodular(numero, e, n)

        codigos_ascii.append((caracter1, codigo1))
        codigos_ascii.append((caracter2, codigo2))
        bloques_originales.append(bloque)
        bloques_cifrados.append(f"{cifrado:06d}")

# Se devuelven los datos de la encriptacion
    return {
        "cifrado": " ".join(bloques_cifrados),
        "L": longitud,
        "n": n,
        "phi": phi,
        "llavepublica": (e, n),
        "relleno": relleno,
        "textorelleno": texto,
        "ascii": codigos_ascii,
        "bloquesoriginales": bloques_originales,
        "bloquescifrados": bloques_cifrados,
    }

# Mensajes principales del programa

if __name__ == "__main__":
    try:
        print("Bienvenido al programa de encriptacion y desencriptacion RSA")
        print("Porfavor ingrese los datos que se le solicitan a continuacion")
        mensaje = input("Mensaje: ")
        p = int(input("Primo p: "))
        q = int(input("Primo q: "))
        e = int(input("Exponente e: "))
        datos = encriptar(mensaje, p, q, e)

        print("\nResultados de la encriptacion:")
        print("n:", datos["n"])
        print("phi:", datos["phi"])
        print("Llave publica:", datos["llavepublica"])
        print("Longitud:", datos["L"])
        print("Se agrego relleno:", "Si" if datos["relleno"] else "No")
        print("ASCII:", datos["ascii"])
        print("Bloques originales:", datos["bloquesoriginales"])
        print("Bloques cifrados:", datos["bloquescifrados"])
        print("Mensaje cifrado C:", datos["cifrado"])
    except ValueError as error:
        print("Error:", error)