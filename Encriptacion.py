"""Encriptacion y desencriptacion RSA con algoritmos propios."""


def esprimo(numero):
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def potenciamodular(base, exponente, modulo):
    resultado = 1
    base = base % modulo
    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente = exponente // 2
    return resultado


def inversomodular(numero, modulo):
    """Calcula el inverso con el algoritmo extendido de Euclides."""
    if type(numero) is not int or type(modulo) is not int or modulo <= 1:
        raise ValueError("El inverso requiere enteros y un modulo mayor que 1.")

    resto_anterior, resto = modulo, numero % modulo
    coeficiente_anterior, coeficiente = 0, 1
    while resto != 0:
        cociente = resto_anterior // resto
        resto_anterior, resto = resto, resto_anterior - cociente * resto
        coeficiente_anterior, coeficiente = (
            coeficiente,
            coeficiente_anterior - cociente * coeficiente,
        )

    if resto_anterior != 1:
        raise ValueError("El numero no tiene inverso modular.")
    return coeficiente_anterior % modulo


def validarparametros(p, q, e):
    """Comparte las mismas condiciones RSA entre ambas operaciones."""
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
    return n, phi


def encriptar(mensaje, p, q, e):
    if not isinstance(mensaje, str) or mensaje == "":
        raise ValueError("Escribe un mensaje que no este vacio.")
    n, phi = validarparametros(p, q, e)

    for caracter in mensaje:
        if not 32 <= ord(caracter) <= 126:
            raise ValueError(
                "Solo se permiten caracteres ASCII del 32 al 126 "
                "(sin tildes, enie, tabulaciones ni saltos de linea)."
            )

    longitud = len(mensaje)
    relleno = longitud % 2 == 1
    texto = mensaje + " " if relleno else mensaje
    codigos_ascii = []
    bloques_originales = []
    bloques_cifrados = []

    for i in range(0, len(texto), 2):
        caracter1 = texto[i]
        caracter2 = texto[i + 1]
        codigo1 = f"{ord(caracter1):03d}"
        codigo2 = f"{ord(caracter2):03d}"
        bloque = codigo1 + codigo2
        cifrado = potenciamodular(int(bloque), e, n)

        codigos_ascii.append((caracter1, codigo1))
        codigos_ascii.append((caracter2, codigo2))
        bloques_originales.append(bloque)
        bloques_cifrados.append(f"{cifrado:06d}")

    return {
        "mensaje": mensaje,
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


def desencriptar(cifrado, longitud, p, q, e):
    """Recupera el mensaje usando C, L y los parametros RSA originales."""
    n, phi = validarparametros(p, q, e)
    if not isinstance(cifrado, str) or cifrado == "":
        raise ValueError("Escribe un cifrado que no este vacio.")

    # Se aceptan solo digitos ASCII y un espacio entre bloques, como al cifrar.
    bloques_cifrados = cifrado.split(" ")
    for posicion, bloque in enumerate(bloques_cifrados, start=1):
        if len(bloque) != 6 or any(digito < "0" or digito > "9" for digito in bloque):
            raise ValueError(
                f"El bloque cifrado {posicion} debe tener seis digitos del 0 al 9. "
                "Separa los bloques con un solo espacio."
            )
        if int(bloque) >= n:
            raise ValueError(f"El bloque cifrado {posicion} debe ser menor que n.")

    if type(longitud) is not int:
        raise ValueError("La longitud L debe ser un numero entero.")
    cantidad = len(bloques_cifrados)
    if longitud not in (2 * cantidad, 2 * cantidad - 1):
        raise ValueError(
            f"Para {cantidad} bloques, L debe ser {2 * cantidad} "
            f"o {2 * cantidad - 1}."
        )

    d = inversomodular(e, phi)
    bloques_originales = []
    codigos_ascii = []
    caracteres = []
    for posicion, bloque in enumerate(bloques_cifrados, start=1):
        numero = potenciamodular(int(bloque), d, n)
        original = f"{numero:06d}"
        codigo1, codigo2 = original[:3], original[3:]
        if not (32 <= int(codigo1) <= 126 and 32 <= int(codigo2) <= 126):
            raise ValueError(
                f"El bloque {posicion} no produce dos codigos ASCII "
                "entre 032 y 126. Revisa el cifrado y los parametros RSA."
            )
        bloques_originales.append(original)
        for codigo in (codigo1, codigo2):
            caracter = chr(int(codigo))
            caracteres.append(caracter)
            codigos_ascii.append((caracter, codigo))

    texto = "".join(caracteres)
    relleno = longitud % 2 == 1
    if relleno and texto[-1] != " ":
        raise ValueError(
            "L es impar, pero el ultimo caracter recuperado no es un espacio de relleno."
        )

    # Retirar exactamente un caracter, sin perder espacios del mensaje original.
    mensaje = texto[:-1] if relleno else texto
    return {
        "mensaje": mensaje,
        "cifrado": cifrado,
        "L": longitud,
        "n": n,
        "phi": phi,
        "d": d,
        "llavepublica": (e, n),
        "llaveprivada": (d, n),
        "relleno": relleno,
        "textorelleno": texto,
        "ascii": codigos_ascii,
        "bloquesoriginales": bloques_originales,
        "bloquescifrados": bloques_cifrados,
    }


def convertirentero(texto, nombre):
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"{nombre} debe ser un numero entero.") from None


def resumirproceso(datos):
    """Presenta los mismos detalles en consola y en la interfaz grafica."""
    desencriptando = "d" in datos
    operacion = "desencriptacion" if desencriptando else "encriptacion"
    lineas = [
        f"Resultados de la {operacion}",
        f"n: {datos['n']}",
        f"phi: {datos['phi']}",
        f"Llave publica (e, n): {datos['llavepublica']}",
    ]
    if desencriptando:
        lineas.extend([
            f"Exponente privado d: {datos['d']}",
            f"Llave privada (d, n): {datos['llaveprivada']}",
        ])
    lineas.extend([
        f"Longitud L: {datos['L']}",
        "Relleno: " + ("Si, un espacio final." if datos["relleno"] else "No."),
        f"Texto procesado (incluye relleno): {datos['textorelleno']!r}",
        f"Mensaje cifrado C: {datos['cifrado']}",
        f"Mensaje {'recuperado' if desencriptando else 'original'} M: {datos['mensaje']!r}",
        "",
        "Conversion de caracteres a ASCII (incluye relleno):",
    ])
    lineas.extend(f"{caracter!r} -> {codigo}" for caracter, codigo in datos["ascii"])
    antes, despues = datos["bloquesoriginales"], datos["bloquescifrados"]
    if desencriptando:
        antes, despues = despues, antes
    lineas.extend(["", "Bloques (cifrado -> recuperado):" if desencriptando
                   else "Bloques (original -> cifrado):"])
    lineas.extend(
        f"{posicion}: {origen} -> {destino}"
        for posicion, (origen, destino) in enumerate(zip(antes, despues), start=1)
    )
    return "\n".join(lineas)


def main():
    print("Bienvenido al programa de encriptacion y desencriptacion RSA")
    while True:
        print("\n1. Encriptar\n2. Desencriptar\n3. Salir")
        try:
            opcion = input("Operacion: ").strip()
            if opcion == "3":
                return
            if opcion not in ("1", "2"):
                print("Error: elige 1, 2 o 3.")
                continue

            if opcion == "1":
                mensaje = input("Mensaje: ")
            else:
                cifrado = input("Mensaje cifrado C: ")
                longitud = convertirentero(input("Longitud original L: "), "L")
            p = convertirentero(input("Primo p: "), "p")
            q = convertirentero(input("Primo q: "), "q")
            e = convertirentero(input("Exponente e: "), "e")
            if opcion == "1":
                datos = encriptar(mensaje, p, q, e)
            else:
                datos = desencriptar(cifrado, longitud, p, q, e)
            print("\n" + resumirproceso(datos))
        except ValueError as error:
            print("Error:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            return


if __name__ == "__main__":
    main()
