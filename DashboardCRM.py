import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def Dashboard():
    st.markdown("FILTRE AQUÍ")

    conn = st.connection("gsheets", type=GSheetsConnection)

    existing_data = conn.read(worksheet="SEGUIMIENTO",usecols=list(range(7)),ttl=7)
    mensaje_data = conn.read(worksheet="MENSAJES",usecols=list(range(3)),ttl=3)

    clientes_antiguos = conn.read(worksheet="MENSAJE_DIARIO",usecols=list(range(6)),ttl=6)

    existing_data = conn.read(worksheet="CRM",usecols=list(range(15)),ttl=15)

    obtencion = existing_data["MedioAdquisicion"].dropna(how="all")
    campaña = existing_data["Campaña"].dropna(how="all")
    distrito = existing_data["Distrito"].dropna(how="all")
    estado = existing_data["Estado"].dropna(how="all")
    mes = existing_data["FechaLead"].dropna(how="all")
    sexo = existing_data["Sexo"].dropna(how="all")
    ocasion = existing_data["Ocasión"].dropna(how="all")

    existing_data["FechaLead"] = pd.to_datetime(existing_data["FechaLead"], errors="coerce")

    # Crear una nueva columna temporal con el nombre del mes
    existing_data["MesNombre"] = existing_data["FechaLead"].dt.strftime('%B')



    col1, col2, col3, col4 , col5 = st.columns(5)


    # Crear columnas para poner los filtros en fila
    with col1:
        filtro_campaña = st.multiselect(
            "Campaña:",
            options=existing_data["Campaña"].dropna().unique()
        )

    with col2:
        filtro_obtencion = st.multiselect(
            "Medio de Obtención:",
            options=existing_data["MedioAdquisicion"].dropna().unique()
        )

    with col3:
        filtro_estado = st.multiselect(
            "Estado:",
            options=existing_data["Estado"].dropna().unique()
        )

    with col4:
        filtro_mes = st.multiselect(
            "Mes:",
            options=existing_data["MesNombre"].dropna().unique()
        )

    with col5:
        filtro_ocasion = st.multiselect(
            "Ocasion:",
            options=existing_data["Ocasión"].dropna().unique()
        )



    # Aplicar filtros
    df_filtrado = existing_data.copy()

    if filtro_campaña:
        df_filtrado = df_filtrado[df_filtrado["Campaña"].isin(filtro_campaña)]

    if filtro_obtencion:
        df_filtrado = df_filtrado[df_filtrado["MedioAdquisicion"].isin(filtro_obtencion)]

    if filtro_estado:
        df_filtrado = df_filtrado[df_filtrado["Estado"].isin(filtro_estado)]

    if filtro_mes:
        df_filtrado = df_filtrado[df_filtrado["MesNombre"].isin(filtro_mes)]

    if filtro_ocasion:
        df_filtrado = df_filtrado[df_filtrado["Ocasión"].isin(filtro_ocasion)]

    # -------------------------------
    # 📊 Gráfico 1: Leads y Clientes por Mes
    # -------------------------------
    st.markdown("## 📅 Leads y Clientes Nuevos por Mes")

    df_mes_estado = df_filtrado.groupby(["MesNombre", "Estado"]).size().unstack(fill_value=0)

    #orden_meses = [
       # "enero", "febrero", "marzo", "abril", "mayo", "junio",
        #"julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    #]
    #df_mes_estado = df_mes_estado.reindex(orden_meses)

    st.bar_chart(df_mes_estado)
    st.write("Total 120 clientes nuevos mes de Julio")

    # -------------------------------
    # 📊 Gráfico 2: Medio de Adquisición por número de leads
    # -------------------------------
    st.markdown("## 🧭 Medio de Adquisición de los clientes")

    df_obtencion = df_filtrado["MedioAdquisicion"].value_counts().sort_values(ascending=True)

    st.bar_chart(df_obtencion)

    st.write("La publicidad de facebook trajo 82 clientes nuevos entre negocio y bocaditos, Asimismo la página misma de Facebook unos 23 clientes")


    st.markdown("## 🧭 Clientes por ocasión")

    df_ocasion = df_filtrado["Ocasión"].value_counts().sort_values(ascending=True)

    st.bar_chart(df_ocasion)

    st.write("De los nuevos clientes de Julio 100 son casual / evento y 20 de Negocio")


    ##MES POR ESTADO


    ##MES POR OBTENCION
    ##MES POR CAMPAÑA
