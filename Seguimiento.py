import streamlit as st
from streamlit_gsheets import GSheetsConnection
##from streamlit_option_menu import option_menu
import webbrowser as webbrowser
import time, webbrowser, pyautogui
from datetime import datetime
import pywhatkit
import pandas as pd

def seguirCliente():

    conn = st.connection("gsheets", type=GSheetsConnection)

    existing_data = conn.read(worksheet="SEGUIMIENTO",usecols=list(range(7)),ttl=7)
    mensaje_data = conn.read(worksheet="MENSAJES",usecols=list(range(3)),ttl=3)

    clientes_antiguos = conn.read(worksheet="MENSAJE_DIARIO",usecols=list(range(6)),ttl=6)

    existing_data = existing_data.dropna(how="all")

    #CON EL DICT PARA CONVERTIR DICCIONARIO EL ZIP PARA GRUPAR TIPO KEYS Y VALUES

    Mensajes_Casual = dict(zip(list(mensaje_data["Mensaje"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else "")),list(mensaje_data["Casual"])))
    Mensajes_Negocio = dict(zip(list(mensaje_data["Mensaje"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else "")),list(mensaje_data["Negocio"])))


    #PAR LOS CLIENTES ANTIGUOS, OBTENER SUS NUMEROS

    numeros_antiguos = list(clientes_antiguos["Telefono"].astype(str).str.strip())

    ##st.markdown(Mensajes_Negocio)

    Telefonos = list(existing_data["TelefonoI"].dropna(how="all").apply(lambda x: str(int(float(x))) if pd.notnull(x) else ""))

    

    ##st.markdown(Telefonos)

    
    wait_time = 30
    col1, col2 = st.columns(2)

    ##to_phne = col1.text_input('DATA TELEFONOS', help = "INngresar con el código del país",placeholder="+51945699321")

    st.dataframe(clientes_antiguos.head(5))


    ##repeat_msg_count = col2.number_input("¿Cuántas veces se enviarán el mensaje?", min_value = 1)

    text_msg = st.text_area("Ingresa el Mensaje",value = "Estimado cliente buenas tardes ...",placeholder="Ingresa el mensaje")

    tab1,tab2, tab3 = st.tabs(["Enviar ahora", "Programar envío","ENVIAR SEGUIMIENTO"])

    with tab1:
        flag_open = st.checkbox("Enviar mensaje",value =False)

        if flag_open == True:
            text_msg_all = ""
            for i in range(len(numeros_antiguos)):
                text_msg_all = text_msg_all + text_msg+'\n'

                pywhatkit.sendwhatmsg_instantly (phone_no = f"+51{numeros_antiguos[i]}",
                message = text_msg_all,
                wait_time = wait_time)

                time.sleep(5)
                pyautogui.hotkey('ctrl','w')
                pyautogui.press('enter')
                
                pyautogui.hotkey('ctrl','r')
                text_msg_all = ""

            flag_open = False


    with tab2:
        col11,col12 = st.columns(2)

        time_send = col11.time_input("Hora que se enviará el mensaje")
        time_hour = int(str(time_send).split(":")[0])
        time_min = int(str(time_send).split(":")[1])

        flag_open = col11.checkbox("Programar mensaje",value=False)

        if flag_open == True:
            text_msg_all = ""

            current_time = datetime.now().time()
            left_time = datetime.strptime(f"{time_hour}:{time_min}", "%H:%M").time()

            current_datetime = datetime.combine(datetime.today(), current_time)
            left_datetime = datetime.combine(datetime.today(), left_time)
            st.success(f"Se enviará el mensaje en {int((left_datetime-current_datetime).total_seconds())} segundos")

            for i in range (len(numeros_antiguos)):
                text_msg_all = text_msg_all + text_msg+'\n'
                
                pywhatkit.sendwhatmsg(phone_no = f"+51{numeros_antiguos[i]}",
                message = text_msg_all,
                time_hour=time_hour,
                time_min=time_min,
                wait_time = wait_time,
                )
            


                time.sleep(5)
                pyautogui.hotkey('ctrl','w')
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl','r')
                text_msg_all = ""

            flag_open = False


    with tab3:
        flag_open = st.checkbox("Enviar seguimiento",value =False)

        Tipo_Ocasion = list(existing_data["Ocasión"].dropna(how="all"))
        NumDiasClientes = list(existing_data["Días"].dropna(how="all"))

        if flag_open == True:
            
            for i in range(len(Telefonos)):

                match int(NumDiasClientes[i]):
                    case 1:
                        mensaje = Mensajes_Casual["1"] if Tipo_Ocasion[i] == "Casual / Evento" else Mensajes_Negocio["1"]
                    case 2:
                        mensaje = Mensajes_Casual["2"] if Tipo_Ocasion[i] == "Casual / Evento" else Mensajes_Negocio["2"]
                    case 3:
                        mensaje = Mensajes_Casual["3"] if Tipo_Ocasion[i] == "Casual / Evento" else Mensajes_Negocio["3"]
                    case 4:
                        mensaje = Mensajes_Casual["4"] if Tipo_Ocasion[i] == "Casual / Evento" else Mensajes_Negocio["4"]
                    case 5:
                        mensaje = Mensajes_Casual["5"] if Tipo_Ocasion[i] == "Casual / Evento" else Mensajes_Negocio["5"]

               

                pywhatkit.sendwhatmsg_instantly (phone_no = f"+51{Telefonos[i]}",
                message = mensaje,
                wait_time = wait_time)

                time.sleep(5)
                pyautogui.hotkey('ctrl','w')
                pyautogui.press('enter')
                flag_open = False
                pyautogui.hotkey('ctrl','r')

        
        
        