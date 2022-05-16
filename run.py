from click import option
from src.application import FILENAMES
from src.application import load_datasets

import streamlit as st
import plotly.express as px

df = load_datasets(FILENAMES)

st.set_page_config(page_title="Delitos en la ciudad de la furia",
                    page_icon=":bar_chart:",
                    layout='wide')

df.id = df.id.astype('string')
df.franja_horaria = df.franja_horaria.astype('string')
df.lat = df.lat.astype('string')
df.long = df.long.astype('string')

del df['cantidad_registrada']
del df['cantidad']
del df['uso_armas']

# ---- SIDEBAR ----
st.sidebar.header("Criterios de búsqueda:")
anio = st.sidebar.multiselect(
    "Seleccione el año:",
    options=df['anio'].unique(),
    default=df['anio'][0]
)

mes = st.sidebar.multiselect(
    "Seleccione el mes:",
    options=df['mes'].unique(),
    default=df['mes'][0]
)

barrio = st.sidebar.multiselect(
    "Seleccione el barrio:",
    options=df['barrio'].unique(),
    default=df['barrio'][0]
)

comuna = st.sidebar.multiselect(
    "Seleccione la comuna:",
    options=df['comuna'].unique(),
    default=df['comuna'][0]
)

delito = st.sidebar.multiselect(
    "Seleccione un delito:",
    options=df['tipo_delito'].unique(),
    default=df['tipo_delito'][0]
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
    st.subheader(f"{total_crimes}")
with center_column:
    st.subheader('Delitos durante la semana:')
    st.subheader(f"{total_crimes - crimes_at_weekends}")
with right_column:
    st.subheader('Delitos en fines de semana:')
    st.subheader(f"{crimes_at_weekends}")

st.markdown('---')

st.dataframe(df_selection)

st.markdown('---')

st.title('Histografia')
crimes_per_day = df_selection.groupby(by=['dia']).size().reset_index(name='delitos')

fig_crimes_day = px.bar(
    crimes_per_day,
    x='delitos',
    y=crimes_per_day['dia'],
    orientation='h',
    title='Distribución de crimenes por día',
    color_discrete_sequence=["#0083B8"] * len(crimes_per_day),
    template='plotly_white'
)

st.plotly_chart(fig_crimes_day)

# HIDE FOOTER

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)