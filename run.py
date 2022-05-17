from click import option
from src.application import FILENAMES
from src.application import load_datasets

import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Delitos en la ciudad de la furia",
                    page_icon=":bar_chart:",
                    layout='wide')
df = None
df = load_datasets(FILENAMES)

# ---- SIDEBAR ----
st.sidebar.header("Criterios de búsqueda:")
anio = st.sidebar.multiselect(
    "Seleccione el año:",
    options=df['anio'].unique(),
    default=df['anio'].unique()
)

mes = st.sidebar.multiselect(
    "Seleccione el mes:",
    options=df['mes'].unique(),
    default=df['mes'].unique()
)

barrio = st.sidebar.multiselect(
    "Seleccione el barrio:",
    options=df['barrio'].unique(),
    default=df['barrio'].unique()
)


delito = st.sidebar.multiselect(
    "Seleccione un delito:",
    options=df['tipo_delito'].unique(),
    default=df['tipo_delito'].unique()
)

df_selection = df.query(
    "anio == @anio & mes == @mes & barrio == @barrio & tipo_delito == @delito"
)

# ---- MAINPAGE ----
st.title(":cop: Delitos @CABA")
st.markdown('##')

# TOP KPIs
total_crimes = int(len(df_selection.index))
crimes_at_weekends = int(len(df_selection[(df_selection['dia'] == 'sábado') | (df_selection['dia'] == 'domingo')]))

left_column, center_column, right_column = st.columns(3)
with left_column:
    st.subheader('Cantidad total de delitos:')
    st.subheader(f"{round(total_crimes/1000,2)}k")
with center_column:
    st.subheader('Delitos durante la semana:')
    st.subheader(f"{round(((total_crimes - crimes_at_weekends)/total_crimes)*100,2)}%")
with right_column:
    st.subheader('Delitos en fines de semana:')
    st.subheader(f"{round((crimes_at_weekends/total_crimes)*100,2)}%")

st.markdown('---')

st.dataframe(df_selection)

st.markdown('---')

st.title('Distribución')
crimes_per_day = df_selection.groupby(by=['dia']).size().sort_values().reset_index(name='delitos')
crimes_per_hour = df_selection.groupby(by=['franja_horaria']).size().sort_values().reset_index(name='hora')
crimes_per_year = df_selection.groupby(by=['anio']).size().sort_values().reset_index(name='delitos')
crimes_per_type = df_selection.groupby(by=['tipo_delito']).size().sort_values().reset_index(name='tipo')
crimes_per_neighborhood = df_selection.groupby(by=['barrio']).size().sort_values().reset_index(name='delitos')


fig_crimes_day = px.bar(
    crimes_per_day,
    x='delitos',
    y=crimes_per_day['dia'],
    orientation='h',
    title='Distribución de crimenes por día',
    color_discrete_sequence=["#0083B8"] * len(crimes_per_day),
    template='plotly_white'
)

fig_crimes_hour = px.bar(
    crimes_per_hour,
    x='hora',
    y=crimes_per_hour['franja_horaria'],
    orientation='h',
    title='Distribución de crimenes por hora',
    color_discrete_sequence=["#0083B8"] * len(crimes_per_hour),
    template='plotly_white',
)

fig_crimes_year = px.bar(
    crimes_per_year,
    x='delitos',
    y=crimes_per_year['anio'],
    orientation='h',
    title='Distribución de crimenes por Año',
    color_discrete_sequence=["#0083B8"] * len(crimes_per_year),
    template='plotly_white',
)

fig_crimes_type = px.bar(
    crimes_per_type,
    x='tipo',
    y=crimes_per_type['tipo_delito'],
    orientation='h',
    title='Distribución de crimenes por Tipo',
    color_discrete_sequence=["#0083B8"] * len(crimes_per_type),
    template='plotly_white',
)

fig_crimes_neighborhood = px.bar(
    crimes_per_neighborhood,
    x='delitos',
    y=crimes_per_neighborhood['barrio'],
    orientation='h',
    title='Distribución de crimenes por Barrio',
    color_discrete_sequence=["#0083B8"] * len(crimes_per_neighborhood),
    template='plotly_white',
)

st.plotly_chart(fig_crimes_day)
st.plotly_chart(fig_crimes_hour)
st.plotly_chart(fig_crimes_year)
st.plotly_chart(fig_crimes_type)
st.plotly_chart(fig_crimes_neighborhood)


# HIDE FOOTER
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)