import streamlit as st
import requests


def seguirCliente() {
    numero = st.text_input("Número")
    mensaje = st.text_area("Mensaje")
    hora = st.number_input("Hora", 0, 23)
    minuto = st.number_input("Minuto", 0, 59)

    if st.button("Enviar"):
        data = {
            "numero": numero,
            "mensaje": mensaje,
            "hora": hora,
            "minuto": minuto
        }
        r = requests.post("https://1234abcd.ngrok.io/enviar", json=data)
        if r.status_code == 200:
            st.success("Mensaje enviado desde tu PC")
        else:
            st.error("Error al enviar")
}