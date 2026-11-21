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

py -3 main.py

El lanzador py -3 selecciona la instalación de Python 3. En otros sistemas,
o si python ya corresponde a esa instalación, usar python main.py.

La interfaz usa Tkinter, incluido en la instalación oficial de Python para
Windows. Si la instalación no lo incluye, habilitar el componente Tcl/Tk al
modificar la instalación de Python. En Linux puede requerirse el paquete
python3-tk de la distribución.

También se puede usar el menú por consola:

py -3 Encriptacion.py

3. Repetir con `AB`, ` A ` y ` A  ` (sin las comillas) para comprobar
   longitudes pares e impares y la conservación de espacios.
4. Probar un mensaje con tildes, un bloque de cinco dígitos o `L = 2`
   para el cifrado del ejemplo. El programa debe informar el error.
