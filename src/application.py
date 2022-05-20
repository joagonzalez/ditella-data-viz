from operator import index
import os
import glob
from statistics import mode
from matplotlib.pyplot import xlabel
import numpy as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ANIOS = ['2016', '2017', '2018', '2019', '2020', '2021']
DELITOS = ['Robo', 'Hurto', 'Lesiones', 'Homicidio']
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
FRANJAS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
BARRIOS = ['Palermo', '']
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/../data', '*.csv')
FILENAMES = glob.glob(PATH)

def save_csv(dataframe: pd.DataFrame, filename: str) -> None:
    PATH_FILENAME = os.path.dirname(os.path.abspath(__file__)) + f'/../{filename}'
    print(f'Saving {PATH_FILENAME}...')
    dataframe.to_csv(PATH_FILENAME, index=False)

def load_datasets(filenames: str) -> pd.DataFrame:
    tmp = []
    for file in filenames:
        print(f'Loading dataset {file}...')
        df = pd.read_csv(file, index_col=None, sep=',', header=0)
        df['uso_armas'] = ''
        tmp.append(df)
    dataset = pd.concat(tmp, axis=0, ignore_index=True)
    return clear_datasets(dataset)

def clear_datasets(df: pd.DataFrame) -> pd.DataFrame:
    df.id = df.id.astype('string')
    df.franja_horaria = df.franja_horaria.astype('string')
    df.lat = df.lat.astype('string')
    df.comuna = df.comuna.astype('string')
    df.long = df.long.astype('string')

    del df['cantidad_registrada']
    del df['cantidad']
    del df['uso_armas']
    
    return df

def show_data(df: pd.DataFrame) -> None:
    print('2016 to 2021')
    print(df.iloc[1:10])

def normalize(cant: int, df: pd.DataFrame) -> float:
    return (cant / len(df.index))*100

def rose_df(df: pd.DataFrame) -> pd.DataFrame:
    df_plot = pd.DataFrame()
    df_plot_dia = pd.DataFrame()
    for anio in ANIOS:
        # FILTRO DATASET POR TIPO DELITO
        df_anio = df[(df['anio'] == int(anio))]
        for delito in DELITOS:
            df_filtrado = df[(df['anio'] == int(anio)) & df['tipo_delito'].str.contains(delito, na=False)]
            print(f'filtramos delito {delito} por año {anio}')
            #print(df_filtrado)
            tmp = pd.DataFrame([{'anio': anio, 'tipo_delito': delito, 'cantidad': normalize(len(df_filtrado.index), df_anio)}])
            df_plot = pd.concat([df_plot.reset_index(drop=True), tmp])
        # print(df_plot)


        # FILTRO DATASET POR DIA
        for dia in DIAS:
            df_filtrado_dia = df[(df['anio'] == int(anio)) & df['dia'].str.contains(dia, na=False)]
            print(f'filtramos dia {dia} por año {anio}')
            #print(df_filtrado_dia)
            tmp_dia = pd.DataFrame([{'anio': anio, 'dia': dia, 'cantidad': normalize(len(df_filtrado_dia.index), df_anio)}])
            df_plot_dia = pd.concat([df_plot_dia.reset_index(drop=True), tmp_dia])
        #print(df_plot_dia)

    return df_plot, df_plot_dia

def bar_plot_df(df: pd.DataFrame) -> pd.DataFrame:
    df_plot = pd.DataFrame()
    tmp = {}
    tmp_franjas = []
    for franja in FRANJAS:
        for anio in ANIOS:
            print(f'filtramos franja {franja} por año {anio}')
            df_anio = df[(df['anio'] == int(anio))]
            df_filtrado = df[(df['anio'] == int(anio)) & (df['franja_horaria'] == franja)]
            tmp_franjas.append({'anio': anio, 'franja': franja, 'delitos': normalize(len(df_filtrado.index), df_anio)})
            #print(tmp_franjas)
    print('---------------------------------------------\n\n')
    print(tmp_franjas)
    
    df_plot = pd.DataFrame(tmp_franjas)
    print(df_plot)
    return df_plot

def bar_hor_df(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df.index)
    print(f'el dataset tiene {total} registros')
    
    crimes_per_neighborhood = df.groupby(by=['barrio'], as_index=False).size().sort_values('size')
    crimes_per_neighborhood['tasa'] = crimes_per_neighborhood['size'].mul(1/total)

    print(crimes_per_neighborhood)
    return crimes_per_neighborhood[20:]

def bar_plot(df: pd.DataFrame) -> None:
    fig = px.bar(
        df, 
        x="franja", 
        y="delitos", 
        facet_col='anio', 
        facet_col_wrap=3,
        text_auto='.2s',
        labels={'anio': 'Año', 'franja': 'Franja horaria [0-23]hs', 'delitos': 'Tasa de delitos [%]'},
        title='Distribución horaria de delitos entre los años 2016-2021 @CABA'
    )
    
    #fig.update_layout(
    #    font=dict(
    #        family="Courier New, monospace",
    #        #size=28,
    #    )
    #)
    
    return fig

def rose_plot(df:pd.DataFrame, graph: str) -> px.bar_polar:
    title_delito = 'Distribución temporal de tipos de delito entre los años 2016-2021 @CABA'
    title_dia = 'Distribución temporal de delitos por día de la semana entre los años 2016-2021 @CABA'
    fig = px.bar_polar(
        df, r="cantidad", 
        theta="anio",
        title= title_delito if graph == "delito" else title_dia,
        color="tipo_delito" if graph == "delito" else "dia", #template="plotly_dark",
        color_discrete_sequence= px.colors.sequential.Oryel_r,
        labels={'cantidad':'Tasa de delitos comentidos [%]',
                'tipo_delito': 'Tipo de delito',
                'dia': 'Dia de la semana del delito'
                }
    )

    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=22,
        )
    )
    
    return fig

def bar_hor_plot(df: pd.DataFrame) -> px.bar:
    fig = px.bar(
        df,
        x='tasa',
        y=df['barrio'],
        labels={'tasa':'Tasa de delitos comentidos 2016-2021 [%]',
                'barrio': 'Barrios de la Ciudad de Buenos Aires'
                },
        orientation='h',
        hover_data=['tasa'], 
        color='tasa',
        color_continuous_scale=px.colors.sequential.YlOrRd,
        color_discrete_sequence= px.colors.sequential.Jet,
        #color_discrete_sequence=["#0083B8"] * len(df),
        title=f'Tasa de delitos espacial acumulada entre los años 2016-2021 @CABA',
        template='plotly_white',
    ) 

    #fig.update_layout(
    #    font=dict(
    #        family="Courier New, monospace",
            #size=28,
    #    )
    #)

    fig.update_traces(
        textfont_size=12, 
        textangle=0, 
        textposition="outside", 
        cliponaxis=False
    )
    
    return fig

def neighborhood_distribution(df: pd.DataFrame) -> pd.DataFrame:
    df_barrio = df.groupby(by=['barrio', 'anio'], as_index=False).size()#size().sort_values().reset_index(name='delitos')
    
    df_barrio = df_barrio[
        df_barrio['barrio'].str.contains('Boca', na=False) |
        df_barrio['barrio'].str.contains('Pompeya', na=False) |
        df_barrio['barrio'].str.contains('Recoleta', na=False) |
        df_barrio['barrio'].str.contains('Retiro', na=False) |
        df_barrio['barrio'].str.contains('Caballito', na=False) |
        df_barrio['barrio'].str.contains('Flores', na=False) |
        df_barrio['barrio'].str.contains('stitución', na=False) |
        df_barrio['barrio'].str.contains('Palermo', na=False)
    ]

    df_anios = df.groupby(by=['anio'], as_index=False).size()
    print(df_barrio[df_barrio['barrio'].str.contains('Boca', na=False)])
    print(df_anios['anio'][0])
    print(df_barrio)

    fig = px.area(df_barrio, 
        x='anio', 
        y='size', 
        facet_col='barrio',
        facet_col_wrap=3,
        title=f'Evolución en la ocurrencia de delitos en barrios principales durante los años 2016-2021 @CABA',
        labels={'anio': 'Años', 'size': 'Cantidad de delitos'}
    )

    fig2 = px.bar(df_barrio, 
        x='anio', 
        y='size', 
        color='barrio',
        barmode='group',
        title=f'Evolución en la ocurrencia de delitos en barrios principales durante los años 2016-2021 @CABA',
        labels={'anio': 'Años', 'size': 'Cantidad de delitos', 'barrio': 'Barrios CABA'},
        text_auto=True,
    )


    #fig.update_layout(
        #title="Plot Title",
        #xaxis_title="X Axis Title",
        #yaxis_title="Y Axis Title",
        #legend_title="Legend Title",
    #    font=dict(
    #        family="Courier New, monospace",
            #size=18,
            #color="RebeccaPurple"
    #    )
    #)

    fig2.update_traces(
        textfont_size=30, 
        #textangle=0, 
        #extposition="outside", 
        cliponaxis=False
    )

    #fig2.update_layout(
        #title="Plot Title",
        #xaxis_title="X Axis Title",
        #yaxis_title="Y Axis Title",
        #legend_title="Legend Title",
        #autosize=False,
        #width=2048,
        #height=1536,
        #font=dict(
            #family="Courier New, monospace",
            #size=28,
            #color="RebeccaPurple"
        #)
    #)
    
    return fig, fig2
   

if __name__ == '__main__':
    # PARA REPRODUCIR IMAGENES DE INFORGRAFIA DESCOMENTAR .update_layout donde se especifica font y size
    df = load_datasets(FILENAMES)
    # save_csv(df, 'legacy_2016_2021.csv')
    print(df.dtypes)
    print(f'Total rows: {len(df)}')
    print(df.groupby(by=['dia']).size().reset_index(name='delitos'))
    show_data(df)
    
    df_rose_delito, df_rose_dia = rose_df(df)
    df_bar = bar_plot_df(df)
    df_hor_bar = bar_hor_df(df)
    
    print(df_hor_bar)
    
    fig_rose_delito = rose_plot(df_rose_delito, 'delito')
    fig_rose_dia = rose_plot(df_rose_dia, 'dia')
    fig_bar = bar_plot(df_bar)
    fig_hor_bar = bar_hor_plot(df_hor_bar)
    fig_n, fig2_n = neighborhood_distribution(df)
    
    fig_rose_delito.show()
    fig_rose_dia.show()
    fig_bar.show()
    fig_hor_bar.show()
    fig_n.show()
    fig2_n.show()
else:
    df = load_datasets(FILENAMES)
    df_rose_delito, df_rose_dia = rose_df(df)
    df_bar = bar_plot_df(df)
    df_hor_bar = bar_hor_df(df)
    fig_rose_delito = rose_plot(df_rose_delito, 'delito')
    fig_rose_dia = rose_plot(df_rose_dia, 'dia')
    fig_bar = bar_plot(df_bar)
    fig_hor_bar = bar_hor_plot(df_hor_bar)
    fig_n, fig2_n = neighborhood_distribution(df)