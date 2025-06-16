import requests

def seguirCliente():
    flag_open = st.checkbox("Enviar mensaje", value=False)
# dentro del tab1:
    if flag_open:
        try:
            url = "https://bf40-2001-1388-53a0-25b6-1851-9e4e-f8b1-f8a3.ngrok-free.app/enviar"
            response = requests.post(url, json={
                "numeros": numeros_antiguos,
                "mensaje": text_msg,
                "wait_time": wait_time
            })

            if response.status_code == 200:
                st.success("Mensajes enviados desde tu PC")
            else:
                st.error(f"Error: {response.text}")

        except Exception as e:
            st.error(f"No se pudo conectar al servidor local: {e}")
