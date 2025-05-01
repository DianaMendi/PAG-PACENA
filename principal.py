import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests


datos_map = pd.read_json("map.json")



def main ():
    
   # url = "https://docs.google.com/spreadsheets/d/1USL95W4CYBvGOIpvBLlcO-3djRTRjJer2DbkCl48vpQ"
    st.title ("APLICACIÓN PACEÑA")
    st.write("## Crear nuevo cliente potencial")
    conn = st.connection("gsheets", type=GSheetsConnection)

    #if st.button("Make API CALL"):

     #   response = requests.get(url)

      #  if response.status_code == 200:
       #     existing_data = response


    existing_data = conn.read(worksheet="CRM",usecols=list(range(11)),ttl=15)
    existing_data = existing_data.dropna(how="all")

    st.dataframe(existing_data)

    SEXO_i = [

        "Femenino",
        "Masculino",
        "Sin definir",
    ]

    TIPO_i = [
        "Empanadas",
        "Bocaditos",
        "Tortas",
        "Pays",
        "Pizzas",
    ]

    OCASION_i = [

        "Casual / Evento",
        "Negocio",
    ]

    CAMPAÑA_i = [

        "Bocaditos normales",
        "Bocaditos especiales",
    ]

    ESTADO_i = [
        "Lead",
        "Seguimiento",
        "Cliente",
        "Cliente perdido",
    ]

    MEDIO_ADQUI_i = [

        "Publicidad Facebook",
        "Orgánico Facebook",
        "Instagram",
        "Tiktok",
        "Preventa",
        "Recomendación cliente",
        "Recomendación del personal",

    ]

    #FORMULARIO

    with st.form(key="CRM_form"):
        idI = st.text_input(label = "ID")
        Nombre = st.text_input(label = "Nombre")
        Sexo = st.selectbox("Sexo", options = SEXO_i, index = None)
        Departamento = st.selectbox("Departamento", options = datos_map.keys(), index=0)
        Provincia = st.selectbox("Provincia", options = list(datos_map[Departamento].keys()), index = 0)
        Distrito = st.selectbox("Distrito", options = list(datos_map[Departamento][Provincia].keys()), index = None)
        Telefono = st.text_input("Teléfono*", max_chars=11)
        Tipo = st.multiselect("Tipo producto*", options = TIPO_i)
        Ocasion = st.selectbox("Ocasión compra*", options = OCASION_i, index = None)
        Medio_Adqui = st.selectbox("Medio de Adquisición*", options = MEDIO_ADQUI_i, index = None)
        Campaña = st.selectbox("Campaña Facebook", options = CAMPAÑA_i, index = None)
        Fecha_Lead = st.date_input(label = "Fecha Lead*")
        Fecha_UC = st.date_input(label = "Fecha Ultimo Contacto")
        Estado = st.selectbox("Estado Cliente*", options = ESTADO_i, index = None)


        st.markdown("**Campo requerido*")

        submit_button = st.form_submit_button(label = "Añadir Cliente potencial")
        existing_data["TelefonoI"] = existing_data["TelefonoI"].astype(str) #PARA CONVERTIR EL EXISTING DATA TELEFONO, PARA CAMBIAR ESA PARTE DEL DATAFRAME SU TIPO
        
        if submit_button:
            if not Tipo or not  Ocasion or not Fecha_Lead or not Medio_Adqui or not Estado or not Telefono:
                st.warning("Falta llenar los campos obligatorios")
                st.stop()
            elif existing_data["TelefonoI"].str.contains(Telefono).any():
                st.warning("El cliente ya existe")
                st.stop()

            else:

                cliente_potencial_new = pd.DataFrame (
                    [
                        {
                            "ID": idI,
                            "Nombre": Nombre,
                            "Sexo": Sexo,
                            "Departamento": Departamento,
                            "Provincia": Provincia,
                            "Distrito": Distrito,
                            "TelefonoI": Telefono,
                            "Tipo": ", " .join(Tipo),
                            "Ocasión": Ocasion,
                            "MedioAdquisicion": Medio_Adqui,
                            "Campaña": Campaña,
                            "FechaLead": Fecha_Lead.strftime("%Y-%m-%d"),
                            "FechaUltimoContacto": Fecha_UC.strftime("%Y-%m-%d"),
                            "Estado": Estado,
                        }
                    ]
                )

                update_df = pd.concat([existing_data, cliente_potencial_new], ignore_index=True)

                conn.update(worksheet="CRM",data=update_df)

                st.success("Cliente potencial añadido")


    #def click_function():
        # Código a ejecutar cuando se hace clic
     #   st.write("Botón clickeado!")

    #st.button("Haz clic", on_click=click_function)'''


# Crear el botón

#if 'clicked' not in st.session_state:
 #   st.session_state.clicked = False

#def click_button():
#    st.session_state.clicked = True

#st.button('Click me', on_click=click_button)

#if st.session_state.clicked:
#    # The message and nested widget will remain on the page
#    st.write('Button clicked!')
#    st.slider('Select a value')




if __name__ == '__main__':
    main()  


