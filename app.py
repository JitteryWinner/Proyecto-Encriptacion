
import streamlit as st

from Encriptacion import (
    convertirentero,
    encriptar,
    desencriptar,
    resumirproceso
)

st.set_page_config(
    page_title="Proyecto de criptografía RSA",
    page_icon="",
    layout="centered"
)

# Estado de la aplicación
valores = {
    "p": "",
    "q": "",
    "e": "",
    "mensaje": "",
    "cifrado": "",
    "longitud": "",
    "resultado_cifrado": None,
    "resultado_descifrado": None,
    "error_cifrado": "",
    "error_descifrado": ""
}

for clave, valor in valores.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


def cargar_ejemplo():
    st.session_state.update(valores)
    st.session_state.p = "367"
    st.session_state.q = "373"
    st.session_state.e = "17"
    st.session_state.mensaje = "RSA"


def obtener_parametros():
    p = convertirentero(st.session_state.p, "p")
    q = convertirentero(st.session_state.q, "q")
    e = convertirentero(st.session_state.e, "e")
    return p, q, e


def ejecutar_encriptacion():
    st.session_state.error_cifrado = ""
    st.session_state.resultado_cifrado = None
    st.session_state.resultado_descifrado = None
    st.session_state.error_descifrado = ""

    try:
        p, q, e = obtener_parametros()

        datos = encriptar(
            st.session_state.mensaje,
            p, q, e
        )

        st.session_state.resultado_cifrado = datos
        st.session_state.cifrado = datos["cifrado"]
        st.session_state.longitud = str(datos["L"])

    except ValueError as error:
        st.session_state.error_cifrado = str(error)


def ejecutar_desencriptacion():
    st.session_state.error_descifrado = ""
    st.session_state.resultado_descifrado = None

    try:
        p, q, e = obtener_parametros()

        longitud = convertirentero(
            st.session_state.longitud, "L"
        )

        datos = desencriptar(
            st.session_state.cifrado,
            longitud,
            p, q, e
        )

        st.session_state.resultado_descifrado = datos

    except ValueError as error:
        st.session_state.error_descifrado = str(error)


# Encabezado
st.title("Encriptación y desencriptación RSA")

st.write(
    "Sistema de encriptación y desencriptación "
    "de mensajes mediante el algoritmo RSA."
)

st.divider()

# Parámetros compartidos
st.subheader("Parámetros RSA")

col1, col2, col3 = st.columns(3)

with col1:
    st.text_input("Número primo p", key="p")

with col2:
    st.text_input("Número primo q", key="q")

with col3:
    st.text_input("Exponente e", key="e")

col1, col2 = st.columns(2)

with col1:
    st.button(
        "Cargar ejemplo",
        on_click=cargar_ejemplo,
        use_container_width=True
    )

with col2:
    st.button(
        "Limpiar campos",
        on_click=lambda: st.session_state.update(valores),
        use_container_width=True
    )

with st.expander("Requisitos de los parámetros"):
    st.markdown("""
    - p y q deben ser números primos diferentes.
    - n = p × q debe ser mayor que 126126
      y menor que 1000000.
    - e debe ser mayor que 1.
    - El MCD entre e y φ(n) debe ser igual a 1.
    - El mensaje debe contener caracteres ASCII
      imprimibles del 32 al 126.
    """)

st.divider()

tab1, tab2 = st.tabs([
    "Encriptar",
    "Desencriptar"
])

# Sección de encriptación
with tab1:
    st.subheader("Encriptar mensaje")

    st.text_input(
        "Mensaje original M",
        key="mensaje",
        placeholder="Escribe tu mensaje..."
    )

    st.caption(
        "Utiliza caracteres ASCII imprimibles, "
        "sin tildes ni ñ. Se conservan los espacios."
    )

    st.button(
        "Encriptar mensaje",
        type="primary",
        on_click=ejecutar_encriptacion,
        use_container_width=True
    )

    if st.session_state.error_cifrado:
        st.error(st.session_state.error_cifrado)

    datos = st.session_state.resultado_cifrado

    if datos is not None:
        st.success("Mensaje encriptado correctamente.")

        st.write("**Mensaje cifrado C**")
        st.code(datos["cifrado"], language=None)

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Longitud original L", datos["L"])

        with c2:
            st.metric("Módulo n", datos["n"])

        st.write("**Llave pública (e, n):**")
        st.code(str(datos["llavepublica"]), language=None)

        st.info(
            "El cifrado C y la longitud L se han "
            "copiado a la pestaña Desencriptar."
        )

        with st.expander(
            "Ver procedimiento matemático",
            expanded=True
        ):
            st.code(
                resumirproceso(datos),
                language=None
            )

        st.download_button(
            "Descargar resultados",
            data=resumirproceso(datos),
            file_name="encriptacion_rsa.txt",
            mime="text/plain"
        )


# Sección de desencriptación
with tab2:
    st.subheader("Desencriptar mensaje")

    st.text_input(
        "Mensaje cifrado C",
        key="cifrado",
        placeholder="Bloques separados por un espacio"
    )

    st.text_input(
        "Longitud original L",
        key="longitud"
    )

    st.button(
        "Desencriptar mensaje",
        type="primary",
        on_click=ejecutar_desencriptacion,
        use_container_width=True
    )

    if st.session_state.error_descifrado:
        st.error(st.session_state.error_descifrado)

    datos = st.session_state.resultado_descifrado

    if datos is not None:
        st.success("Mensaje recuperado correctamente.")

        st.write("**Mensaje recuperado M**")
        st.code(repr(datos["mensaje"]), language=None)

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Exponente privado d", datos["d"])

        with c2:
            st.metric("Módulo n", datos["n"])

        st.write("**Llave privada (d, n):**")
        st.code(str(datos["llaveprivada"]), language=None)

        with st.expander(
            "Ver procedimiento matemático",
            expanded=True
        ):
            st.code(
                resumirproceso(datos),
                language=None
            )

        st.download_button(
            "Descargar resultados",
            data=resumirproceso(datos),
            file_name="desencriptacion_rsa.txt",
            mime="text/plain"
        )

# Pie de página
st.divider()

st.markdown("""

**Integrantes:**
- David Berganza — 25573
- José Alejandro Rustrian — 25512
""")

