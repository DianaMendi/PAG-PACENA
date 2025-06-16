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
                url = "https://defd-2001-1388-53a0-25b6-1851-9e4e-f8b1-f8a3.ngrok-free.app/enviar"  # <- REEMPLAZA con tu URL ngrok activa
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
        st.subheader("📊 Seguimiento de Clientes")

        seguimiento_data = conn.read(worksheet="SEGUIMIENTO", ttl=5).dropna(how="all")
        
        # Mostrar la tabla de seguimiento
        st.dataframe(seguimiento_data, use_container_width=True)

        # Filtro por estado o nombre
        st.write(seguimiento_data.columns.tolist())

        estados = seguimiento_data["Estado"].unique().tolist()
        estado_seleccionado = st.selectbox("Filtrar por estado:", ["Todos"] + estados)

        if estado_seleccionado != "Todos":
            seguimiento_data = seguimiento_data[seguimiento_data["Estado"] == estado_seleccionado]

        nombre_buscar = st.text_input("🔍 Buscar por nombre:")
        if nombre_buscar:
            seguimiento_data = seguimiento_data[seguimiento_data["Nombre"].str.contains(nombre_buscar, case=False)]

        st.write("Resultados filtrados:")
        st.dataframe(seguimiento_data, use_container_width=True)

        st.markdown("---")
        st.subheader("✏️ Actualizar seguimiento")

        cliente_id = st.text_input("ID del cliente a actualizar")
        nuevo_estado = st.selectbox("Nuevo estado", ["Pendiente", "Respondido", "Cliente perdido"])

        if st.button("Actualizar estado"):
            if cliente_id in seguimiento_data["ID"].astype(str).values:
                fila = seguimiento_data[seguimiento_data["ID"].astype(str) == cliente_id].index[0]
                seguimiento_data.at[fila, "Estado"] = nuevo_estado
                seguimiento_data.at[fila, "Último contacto"] = pd.Timestamp.now().strftime('%Y-%m-%d')

                # Escribir de vuelta a Google Sheets
                conn.update(worksheet="SEGUIMIENTO", data=seguimiento_data)
                st.success("✅ Estado actualizado correctamente.")
            else:
                st.error("⚠️ ID no encontrado.")

