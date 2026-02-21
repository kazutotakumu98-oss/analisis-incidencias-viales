import streamlit as st
import pandas as pd
import plotly.express as px
##//Ejecutar con py -m streamlit run app.py//##
st.set_page_config(page_title="Sistema de Incidencias Viales", layout="wide")


@st.cache_data
def cargar_datos():
    df1 = pd.read_excel("Observatorio Nacional de Seguridad Víal (1).xlsx")
    df2 = pd.read_excel("Observatorio Nacional de Seguridad Víal (2).xlsx")
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = cargar_datos()


st.sidebar.header("Filtros")

anio = st.sidebar.selectbox("Año", ["Todos"] + sorted(df["Año"].dropna().unique().tolist()))
departamento = st.sidebar.selectbox("Departamento", ["Todos"] + sorted(df["Departamento"].dropna().unique().tolist()))

df_filtrado = df.copy()

if anio != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Año"] == anio]

if departamento != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Departamento"] == departamento]


total = len(df_filtrado)

# Simulación de severidad 
df_filtrado["Severidad"] = df_filtrado["Naturaleza"]

promedio_mensual = round(total / 12, 1)



tab1, tab2, tab3 = st.tabs(["📊 Panorama General", "🗺 Análisis Geográfico", "⚠ Factores de Riesgo"])


with tab1:

    st.title("Sistema de Análisis de Incidencias Viales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Incidencias", total)

    col4.metric("Promedio Mensual", promedio_mensual)

    st.divider()

    colA, colB = st.columns(2)

    # Incidencias por Naturaleza
    conteo_tipo = df_filtrado["Naturaleza"].value_counts().reset_index()
    conteo_tipo.columns = ["Naturaleza", "Cantidad"]

    fig_tipo = px.bar(
        conteo_tipo,
        x="Naturaleza",
        y="Cantidad",
        color="Naturaleza",
        title="Incidencias por Tipo",
    )

    colA.plotly_chart(fig_tipo, use_container_width=True)

    # Incidencias por Severidad
    conteo_severidad = df_filtrado["Severidad"].value_counts().reset_index()
    conteo_severidad.columns = ["Severidad", "Cantidad"]

    fig_pie = px.pie(
        conteo_severidad,
        names="Severidad",
        values="Cantidad",
        title="Incidencias por Severidad",
    )

    colB.plotly_chart(fig_pie,  width="stretch")

    st.divider()

    # Evolución temporal
    conteo_mes = df_filtrado.groupby("Mes").size().reset_index(name="Incidencias")
    conteo_mes = conteo_mes.sort_values("Mes")

    fig_line = px.line(
        conteo_mes,
        x="Mes",
        y="Incidencias",
        markers=True,
        title="Evolución Mensual de Incidencias",
    )

    st.plotly_chart(fig_line,  width="stretch")



with tab2:

    st.subheader("Incidencias por Departamento")

    conteo_depto = df_filtrado["Departamento"].value_counts().reset_index()
    conteo_depto.columns = ["Departamento", "Cantidad"]

    fig_geo = px.bar(
        conteo_depto,
        x="Departamento",
        y="Cantidad",
        color="Departamento", color_discrete_sequence=px.colors.qualitative.Set3,
        title="Ranking de Departamentos"
    )

    st.plotly_chart(fig_geo,  width="stretch")

    st.subheader("Top Distritos")

    conteo_distrito = df_filtrado["Distrito"].value_counts().head(10).reset_index()
    conteo_distrito.columns = ["Distrito", "Cantidad"]

    fig_distrito = px.bar(
        conteo_distrito,
        x="Distrito",
        y="Cantidad",
        color="Distrito", color_discrete_sequence=px.colors.qualitative.Set2,
        title="Top 10 Distritos con más Incidencias"
    )

    st.plotly_chart(fig_distrito,  width="stretch")


# =====================================================
# TAB 3 - FACTORES DE RIESGO
# =====================================================

with tab3:

    st.subheader("Principales Causas de Accidentes")

    conteo_causa = df_filtrado["Causa"].value_counts().head(10).reset_index()
    conteo_causa.columns = ["Causa", "Cantidad"]

    fig_causa = px.bar(
        conteo_causa,
        x="Causa",
        y="Cantidad",
        color="Causa", color_discrete_sequence=px.colors.qualitative.Set1,
        title="Top 10 Causas",
    )

    st.plotly_chart(fig_causa,  width="stretch")

    st.subheader("Distribución por Sexo")

    conteo_sexo = df_filtrado["Sexo"].value_counts().reset_index()
    conteo_sexo.columns = ["Sexo", "Cantidad"]

    fig_sexo = px.pie(
        conteo_sexo,
        names="Sexo",
        values="Cantidad",
        title="Distribución por Sexo",
    )

    st.plotly_chart(fig_sexo,  width="stretch")

