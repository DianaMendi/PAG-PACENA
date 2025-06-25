
#CONFIGURACIÓN INICIAL

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from streamlit_option_menu import option_menu
from datetime import datetime #PARA IMPORTA DEL DÍA FECHA

import Seguimiento #IMPORTANDO EL SEGUIMIENTO.PY PARA USAR SUS FUNCIONES
import DashboardCRM #IMPORTANDO LA HOJA DE SAHBOARD CRM PARA USAR SUS FUNCIONES
import Dashboard_General
import os


datos_map = pd.read_json("map.json")



def main ():

    with st.sidebar:

        col1, col2, col3 = st.columns([1, 2, 1])
    
        with col2:

            st.image('pages/img/logoh.jpg',width=200)

        selected = option_menu(
            menu_title = "Menú Principal",
            options = ["Cliente potencial","Seguimiento","Dashboard CRM","Dashboard General"],
        )

        col4, col5, col6 = st.columns([1, 2, 1])

        with col5:

            st.markdown("<marquee> **By Diana Mendizabal** </marquee>", unsafe_allow_html=True)

    if selected == "Seguimiento":
        Seguimiento.seguirCliente()
    elif selected == "Cliente potencial":
        PrincipalP()
    elif selected == "Dashboard CRM":
        DashboardCRM.Dashboard()
    elif selected == "Dashboard General":
        Dashboard_General.Dashboard_General()


#ESTE CODIGO SERÁ DE LA PÁGINA PRINCIPAL QUE ES DE AÑADIR CLIENTE POTENCIAL

def PrincipalP ():
    # url = "https://docs.google.com/spreadsheets/d/1USL95W4CYBvGOIpvBLlcO-3djRTRjJer2DbkCl48vpQ"
    st.title ("AGREGAR O EDITAR CLIENTES")
    conn = st.connection("gsheets", type=GSheetsConnection)


    #if st.button("Make API CALL"):

     #   response = requests.get(url)

      #  if response.status_code == 200:
       #     existing_data = response


    existing_data = conn.read(worksheet="CRM",usecols=list(range(20)),ttl=20)
    #AMPLIAREMOS EL NUM DE COLUMNAS PARA QUE TMB RECONOZACA LAS FECHAS, ESTADO


    existing_data = existing_data.dropna(how="all")


    ##PAR QUE SE MUESTRE LOS 5 PRIMEROS
    st.dataframe(existing_data.head(5))



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


    PRECIO_i = [

        "2",
        "2,40",
        "2,45",
        "2,5",
        "2,8",
        "3",
        "4",

    ]


    existing_data["TelefonoI"] = existing_data["TelefonoI"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else "")

    
    existing_data["ID"] = existing_data["ID"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else "")


    #PARA AÑADIR COLOR AL BOTON DE SELECCIONAR TELEFONO

    st.markdown(

        """
        <style>
            div[data-baseweb = "select"]{
                background-color:#f7b260 ! important;
                border-radius: 5px;
                padding: 3px;
            
            }

        </style>

        <div id="telefono-box">

        """,

        unsafe_allow_html = True

    )

    with st.container():
    # Usamos columnas para controlar el ancho
        col1, col2, col3 = st.columns([1, 3, 1])  # Centramos

        with col2:
            st.markdown("""
            <div style='background-color:#ff4d4d; padding: 5px; border-radius: 10px; text-align: center'>
                <label style='color:white; font-weight:bold; font-size:18px; '>EDITAR LEAD POR TELÉFONO</label>
            """, unsafe_allow_html=True)

            # Luego el selectbox normal (no estará *dentro* del div, pero estará justo debajo)

            cliente_ids = st.selectbox("", options = existing_data["TelefonoI"].tolist(), index = None, key="telefono_select")
    
            st.markdown("</div>", unsafe_allow_html=True)

    #cliente_data = None

    #st.write("## Crear nuevo cliente potencial")




    st.markdown("""
        <div style='background-color:#f7b260; padding: 5px; border-radius: 10px; text-align: center'>
        <label style='color:black; font-weight:bold; font-size:18px; '>AGREGAR NUEVO CLIENTE</label>
        """, unsafe_allow_html=True)

    


    if cliente_ids: # and "form_initialized" not in st.session_state:
        cliente_data = existing_data[existing_data["TelefonoI"] == cliente_ids].iloc[0]




           # idI.value = cliente_data["ID"]
           # "Nombre": Nombre,
        
        st.session_state.idI = cliente_data["ID"]
            #st.session_state.form_initialized = True  ESTO NO PORQUE SOLO FUNCIONARA LA PRIMERA VEZ CUANDO SELECCIONEMOS EL TELEFONO LUEGO YA NO 

        st.session_state.Nombre = cliente_data["Nombre"]
        st.session_state.Sexo = cliente_data["Sexo"]
        st.session_state.Departamento = cliente_data["Departamento"] if pd.notna(cliente_data["Departamento"]) and cliente_data["Departamento"] != "" else ""
        st.session_state.Provincia = cliente_data["Provincia"] if pd.notna(cliente_data["Provincia"]) and cliente_data["Departamento"] != "" else ""
        st.session_state.Distrito = cliente_data["Distrito"] if pd.notna(cliente_data["Distrito"]) and cliente_data["Departamento"] != "" else ""
        st.session_state.Telefono = cliente_data["TelefonoI"]
        st.session_state.Tipo = cliente_data["Tipo"].split(", ")
        st.session_state.Ocasion = cliente_data["Ocasión"]
        st.session_state.Medio_Adqui = cliente_data["MedioAdquisicion"]
        st.session_state.Campaña = cliente_data["Campaña"]
        st.session_state.Fecha_Lead = pd.to_datetime(cliente_data["FechaLead"])
        st.session_state.Fecha_UC = pd.to_datetime(cliente_data["FechaUltimoContacto"])
        st.session_state.Estado = cliente_data["Estado"]
        st.session_state.Comentario = cliente_data["Comentario"] if pd.notna(cliente_data["Comentario"]) else ""
        st.session_state.Direccion = cliente_data["DIRECCION"]
        st.session_state.Referencia = cliente_data["REFERENCIA"]
        st.session_state.H_entrega = cliente_data["HORA_ENTREGA"]
        st.session_state.Delivery = cliente_data["DELIVERY"]
        st.session_state.Precio = cliente_data["Precio"]
    
    fecha_str = datetime.now().date() ##PARA TENER LA FECHA ACTUAL EN CASO NO SE COLOQUE EN EL INPUT DE FECHA LEAD
    
    #FORMULARIO

    with st.form(key="CRM_form"):


        #PARA EDITAR UN CLIENTE ACTUAL

        idI = st.text_input(label = "ID", value=st.session_state.get("idI", ""))
        Nombre = st.text_input(label = "Nombre", value=st.session_state.get("Nombre", ""))
        Sexo = st.selectbox("Sexo", options = SEXO_i, index=SEXO_i.index(st.session_state["Sexo"]) if "Sexo" in st.session_state and st.session_state["Sexo"] in SEXO_i else None)
        Departamento = st.selectbox("Departamento", options = datos_map.keys(), index=list(datos_map.keys()).index(st.session_state["Departamento"]) if "Departamento" in st.session_state else 0)
        Provincia = st.selectbox("Provincia", options = list(datos_map[Departamento].keys()), index=list(datos_map[Departamento].keys()).index(st.session_state["Provincia"]) if "Provincia" in st.session_state else 0)
        Distrito = st.selectbox("Distrito", options = list(datos_map[Departamento][Provincia]), index=list(datos_map[Departamento][Provincia].keys()).index(st.session_state["Distrito"]) if "Distrito" in st.session_state and pd.notna(cliente_data["Distrito"]) and cliente_data["Departamento"] != "" else 0)
        Telefono = st.text_input("Teléfono*", value=st.session_state.get("Telefono", ""), max_chars=11)
        Tipo = st.multiselect("Tipo producto*", options = TIPO_i, default=st.session_state.get("Tipo", []))
        Ocasion = st.selectbox("Ocasión compra*", options = OCASION_i, index=OCASION_i.index(st.session_state["Ocasion"]) if "Ocasion" in st.session_state and st.session_state["Ocasion"] in OCASION_i else None)
        Medio_Adqui = st.selectbox("Medio de Adquisición*", options = MEDIO_ADQUI_i, index=MEDIO_ADQUI_i.index(st.session_state["Medio_Adqui"]) if "Medio_Adqui" in st.session_state and st.session_state["Medio_Adqui"] in MEDIO_ADQUI_i else None)
        Campaña = st.selectbox("Campaña Facebook", options = CAMPAÑA_i, index=CAMPAÑA_i.index(st.session_state["Campaña"]) if "Campaña" in st.session_state and st.session_state["Campaña"] in CAMPAÑA_i else None)
        Fecha_Lead = st.date_input(label = "Fecha Lead*", value=st.session_state.get("Fecha_Lead", None))
        Fecha_UC = st.date_input(label = "Fecha Ultimo Contacto", value=st.session_state.get("Fecha_UC", None))
        Estado = st.selectbox("Estado Cliente*", options = ESTADO_i, index=ESTADO_i.index(st.session_state["Estado"]) if "Estado" in st.session_state and st.session_state["Estado"] in ESTADO_i else None)
        Comentario = st.text_area(label = "Comentario", value=st.session_state.get("Comentario", ""))


            
        with st.expander("📦 Datos adicionales"):
            Direccion = st.text_input(label = "DIRECCION", value=st.session_state.get("DIRECCION", ""))
            Referencia = st.text_input(label = "REFERENCIA",value=st.session_state.get("REFERENCIA", ""))
            H_entrega = st.text_input(label = "HORA_ENTREGA",value=st.session_state.get("HORA_ENTREGA", ""))
            Delivery = st.text_input(label = "DELIVERY",value=st.session_state.get("DELIVERY", ""))
            Precio = st.text_input(label = "Precio",value=st.session_state.get("Precio", ""))

        st.markdown("**Campo requerido*")

        submit_button = st.form_submit_button(label = "Añadir Cliente potencial")
        existing_data["TelefonoI"] = existing_data["TelefonoI"].astype(str) #PARA CONVERTIR EL EXISTING DATA TELEFONO, PARA CAMBIAR ESA PARTE DEL DATAFRAME SU TIPO
        #j
        
        if submit_button:
            if not Tipo or not  Ocasion  or not Medio_Adqui or not Estado or not Telefono:
                st.warning("Falta llenar los campos obligatorios")
                st.stop()
            elif existing_data["TelefonoI"].str.contains(Telefono).any():
               ## st.warning("El cliente ya existe")
               ## st.stop()
                
                if existing_data["TelefonoI"].str.contains(Telefono).any():
                    st.session_state.cliente_existente = True
                    st.session_state.datos_temporales = {
                        "ID": idI,
                        "Nombre": Nombre,
                        "Sexo": Sexo,
                        "Departamento": Departamento,
                        "Provincia": Provincia,
                        "Distrito": Distrito,
                        "TelefonoI": Telefono,
                        "Tipo": ", ".join(Tipo),
                        "Ocasión": Ocasion,
                        "MedioAdquisicion": Medio_Adqui,
                        "Campaña": Campaña,
                        "FechaLead": fecha_str.strftime("%Y-%m-%d") if Fecha_Lead is None else Fecha_Lead.strftime("%Y-%m-%d"),
                        "FechaUltimoContacto": fecha_str.strftime("%Y-%m-%d") if Fecha_Lead is None else Fecha_Lead.strftime("%Y-%m-%d") if Fecha_UC is None  else Fecha_UC.strftime("%Y-%m-%d"),
                            # O un valor por defecto como "" )
                        ##ESO ES PARA QUE SI NO HAYA FECHA ULTIMO CONTACTO SE AGREGUE LA FECHALEAD PARA QUE NO HAYA ERROR
                        "Estado": Estado,
                        "Comentario": Comentario,
                        "DIRECCION": Direccion,
                        "REFERENCIA": Referencia,
                        "HORA_ENTREGA": H_entrega,
                        "DELIVERY": Delivery,
                        "Precio": Precio,

                    }
            else:

                cliente_potencial_new = pd.DataFrame (
                    [
                        {
                            "ID": int(float(existing_data["ID"].max()))+1,
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
                            "FechaLead": fecha_str.strftime("%Y-%m-%d") if Fecha_Lead is None else Fecha_Lead.strftime("%Y-%m-%d"),
                            "FechaUltimoContacto": fecha_str.strftime("%Y-%m-%d") if Fecha_Lead is None else Fecha_Lead.strftime("%Y-%m-%d") if Fecha_UC is None  else Fecha_UC.strftime("%Y-%m-%d"),
                            "Estado": Estado,
                            "DIRECCION": Direccion,
                            "REFERENCIA": Referencia,
                            "HORA_ENTREGA": H_entrega,
                            "DELIVERY": Delivery,
                            "Precio": Precio,
                        }
                    ]
                )

                update_df = pd.concat([existing_data, cliente_potencial_new], ignore_index=True)

                conn.update(worksheet="CRM",data=update_df)

                st.success("Cliente potencial añadido")



    if st.session_state.get("cliente_existente", False):

        st.session_state.mostrar_popup = True

        if st.session_state.mostrar_popup:
            
            st.markdown("EL CONTACTO YA EXISTE ¿Quieres cambiarlo?");
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Sí, reemplazar"):
                    st.success("Cliente reemplazado.")
                    index = existing_data[existing_data["TelefonoI"] == st.session_state.datos_temporales["TelefonoI"]].index[0]
                    for key, value in st.session_state.datos_temporales.items():
                        existing_data.at[index, key] = value

                    # Guardar cambios en la hoja de cálculo
                    conn.update(worksheet="CRM", data=existing_data)

                    # Limpiar estados
                    st.session_state.mostrar_popup = False
                    st.session_state.cliente_existente = False
                    st.session_state.datos_temporales = {}
            with col2:
                if st.button("❌ Cancelar"):
                    st.session_state.mostrar_popup = False


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


