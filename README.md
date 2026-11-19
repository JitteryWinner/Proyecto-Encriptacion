# Proyecto de encriptación y desencriptación RSA

Proyecto para MM2015 Matemática Discreta 1.

Autores:

- David Berganza #25573
- José Alejandro Rustrian #25512

## Requisitos y ejecución

Python 3.10 o posterior. Comprobado con Python 3.12.14 y 3.14.3.
Solo se utiliza la biblioteca estándar: no hay paquetes que instalar con pip
ni se necesita un archivo de dependencias.

Desde la carpeta del proyecto, iniciar la interfaz gráfica en Windows:

```console
py -3 main.py
```

El lanzador `py -3` selecciona la instalación de Python 3. En otros sistemas,
o si `python` ya corresponde a esa instalación, usar `python main.py`.

La interfaz usa Tkinter, incluido en la instalación oficial de Python para
Windows. Si la instalación no lo incluye, habilitar el componente Tcl/Tk al
modificar la instalación de Python. En Linux puede requerirse el paquete
`python3-tk` de la distribución.

También se puede usar el menú por consola:

```console
py -3 Encriptacion.py
```

## Uso de la interfaz

1. Ingresar los primos distintos `p` y `q` y el exponente público `e`.
   **Cargar ejemplo** completa los parámetros y el mensaje del caso de referencia.
2. En **Encriptar**, escribir el mensaje y presionar **Encriptar**. Los campos
   de resultado muestran el cifrado `C` y la longitud original `L`.
3. Guardar `C` y `L` junto con los parámetros usados. La aplicación los copia
   también a los campos de entrada de la pestaña **Desencriptar**.
4. Para desencriptar, ingresar o revisar `C` y `L`, conservar los mismos
   `p`, `q` y `e`, y presionar **Desencriptar**.
5. El campo **Mensaje recuperado M** muestra el texto original. El panel
   **Detalle del proceso** muestra `n`, `phi`, la llave pública, `L`, el
   relleno, cada conversión ASCII y los bloques antes y después de la operación.
   En desencriptación muestra también `d` y la llave privada `(d, n)`.

El detalle escribe los mensajes entre comillas para que se distingan los
espacios iniciales y finales. Las comillas no forman parte del mensaje.
Los errores se muestran en un cuadro de diálogo y en el estado de la ventana;
se pueden corregir los datos y volver a ejecutar.

En consola, elegir **1** para encriptar, **2** para desencriptar o **3** para
salir. El programa solicita las entradas y muestra el mismo detalle del proceso.

## Representación, relleno y validaciones

- Se admiten caracteres ASCII imprimibles del 32 al 126, incluidos espacios,
  mayúsculas, minúsculas, números y signos. No se admiten mensajes vacíos,
  tildes, ñ, tabulaciones ni saltos de línea.
- Cada carácter se representa con tres dígitos y cada pareja forma un bloque
  de seis dígitos.
- Si la longitud original `L` es impar, se agrega exactamente un espacio
  al final antes de cifrar. Al desencriptar se verifica ese espacio y se
  elimina solo el último carácter. Si `L` es par, no se elimina nada.
  Todos los espacios originales se conservan, incluidos los del final.
- `p`, `q` y `e` deben ser enteros; `p` y `q` deben ser primos distintos.
  Se exige `126126 < p*q < 1000000`, `e > 1` y `MCD(e, phi) = 1`.
  Se aceptan exponentes públicos mayores que `phi` si cumplen esas condiciones.
- Cada bloque cifrado debe contener exactamente seis dígitos del 0 al 9 y
  ser menor que `n`. Usar un solo espacio entre bloques, sin espacios
  adicionales al inicio o al final del cifrado.
- Para `k > 0` bloques, `L` debe ser un entero igual a `2*k` o `2*k-1`.
  Se comprueban ambos códigos ASCII de cada bloque recuperado y el espacio
  de relleno cuando corresponde.

## Ejemplo completo

```text
Mensaje original: "RSA"
p = 367, q = 373, e = 17
n = 136891
phi = 136152
Llave pública: (17, 136891)
L = 3
Texto con relleno: "RSA "
ASCII: R=082, S=083, A=065, espacio=032
Bloques originales: 082083 065032
C = 026054 123875

Entradas para desencriptar:
C = 026054 123875
L = 3
p = 367, q = 373, e = 17

d = 8009
Llave privada: (8009, 136891)
Bloques recuperados: 082083 065032
Mensaje recuperado: "RSA"
```

Para demostrar una validación, cambiar `L` a `2`: el cifrado tiene dos
bloques y solo admite `L = 3` o `L = 4`. Para comprobar los espacios,
repetir las operaciones con `" A  "` (sin ingresar las comillas).

## Código y algoritmos

En `Encriptacion.py`:

- `esprimo`: comprobación por división hasta la raíz cuadrada.
- `mcd`: algoritmo de Euclides.
- `inversomodular`: algoritmo extendido de Euclides; obtiene el representante
  `1 <= d < phi` que satisface `e*d % phi == 1`.
- `potenciamodular`: cuadrados sucesivos con reducción modular durante el cálculo.
- `validarparametros`: validaciones RSA compartidas.
- `encriptar` y `desencriptar`: conversión ASCII, bloques, relleno y resultados.
- `resumirproceso`: detalle compartido por ambas interfaces.

`main.py` contiene la ventana y sus controles.
No se usa `math.gcd`, `pow` modular ni bibliotecas de criptografía.

## Comprobaciones

Para revisar el funcionamiento desde la interfaz:

1. Usar **Cargar ejemplo** y encriptar. Debe resultar
   `C = 026054 123875`, `L = 3`, `n = 136891` y `phi = 136152`.
2. Desencriptar con esos datos. Debe aparecer `d = 8009` y recuperarse
   exactamente `RSA`.
3. Repetir con `AB`, ` A ` y ` A  ` (sin las comillas) para comprobar
   longitudes pares e impares y la conservación de espacios.
4. Probar un mensaje con tildes, un bloque de cinco dígitos o `L = 2`
   para el cifrado del ejemplo. El programa debe informar el error.
