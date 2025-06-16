import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

def seguirCliente():
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Leer datos
    existing_data = conn.read(worksheet="SEGUIMIENTO", usecols=list(range(7)), ttl=7)
    mensaje_data = conn.read(worksheet="MENSAJES", usecols=list(range(3)), ttl=3)
    clientes_antiguos = conn.read(worksheet="MENSAJE_DIARIO", usecols=list(range(6)), ttl=6)

    existing_data = existing_data.dropna(how="all")

    # Diccionarios de mensajes
    Mensajes_Casual = dict(zip(
        mensaje_data["Mensaje"].dropna().apply(lambda x: str(int(float(x)))), 
        mensaje_data["Casual"]
    ))
    Mensajes_Negocio = dict(zip(
        mensaje_data["Mensaje"].dropna().apply(lambda x: str(int(float(x)))), 
        mensaje_data["Negocio"]
    ))

    # Teléfonos
    numeros_antiguos = list(clientes_antiguos["Telefono"].astype(str).str.strip())
    Telefonos = list(existing_data["TelefonoI"].dropna().apply(lambda x: str(int(float(x)))))

    # INTERFAZ
    st.subheader("Seguimiento de Clientes")
    st.dataframe(clientes_antiguos.head(5))

    wait_time = 30
    text_msg = st.text_area("Mensaje a enviar", value="Estimado cliente, buenas tardes...")

    tab1, tab2 = st.tabs(["Enviar ahora", "Seguimiento Clientes"])

    with tab1:
        flag_open = st.checkbox("Enviar mensaje", value=False)

        if flag_open:
            try:
                url = "https://d414-2001-1388-53a0-25b6-1851-9e4e-f8b1-f8a3.ngrok-free.app/enviar"  # <- REEMPLAZA con tu URL ngrok activa
                response = requests.post(url, json={
                    "numeros": numeros_antiguos,
                    "mensaje": text_msg,
                    "wait_time": wait_time
                })

                if response.status_code == 200:
                    st.success("✅ Mensajes enviados desde tu PC.")
                else:
                    st.error(f"❌ Error del servidor: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"❌ No se pudo conectar al servidor local: {e}")

    with tab2:
        existing_data = conn.read(worksheet="SEGUIMIENTO", usecols=list(range(7)), ttl=7)
        mensaje_data = conn.read(worksheet="MENSAJES", usecols=list(range(3)), ttl=3)

        existing_data = existing_data.dropna(how="all")

        Mensajes_Casual = dict(zip(
            mensaje_data["Mensaje"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else ""),
            mensaje_data["Casual"]
        ))
        Mensajes_Negocio = dict(zip(
            mensaje_data["Mensaje"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else ""),
            mensaje_data["Negocio"]
        ))

        Telefonos = list(existing_data["TelefonoI"].dropna().apply(lambda x: str(int(float(x))) if pd.notnull(x) else ""))
        Tipo_Ocasion = list(existing_data["Ocasión"].dropna())
        NumDiasClientes = list(existing_data["Días"].dropna())

        wait_time = 30

        with st.expander("📤 Enviar seguimiento por días y ocasión"):
            text_msg = st.text_area("Mensaje base", "Hola, te recordamos nuestras ofertas esta semana")
            flag_open = st.checkbox("✅ Enviar Seguimiento", value=False)

            if flag_open:
                for i in range(len(Telefonos)):
                    try:
                        dias = int(NumDiasClientes[i])
                        tipo = Tipo_Ocasion[i]

                        if tipo == "Casual / Evento":
                            mensaje = Mensajes_Casual.get(str(dias), text_msg)
                        else:
                            mensaje = Mensajes_Negocio.get(str(dias), text_msg)

                        response = requests.post("https://d414-2001-1388-53a0-25b6-1851-9e4e-f8b1-f8a3.ngrok-free.app/enviar", json={
                            "numeros": [Telefonos[i]],
                            "mensaje": mensaje,
                            "wait_time": wait_time
                        })

                        if response.status_code == 200:
                            st.success(f"Mensaje enviado a {Telefonos[i]}")
                        else:
                            st.error(f"❌ Error {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error con {Telefonos[i]}: {e}")
