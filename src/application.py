from operator import index
import os
import glob
import numpy as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ANIOS = ['2016', '2017', '2018', '2019', '2020', '2021']
DELITOS = ['Robo', 'Hurto', 'Lesiones', 'Homicidio']
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
FRANJAS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
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

def maps(df: pd.DataFrame):

    df['text'] = df['tipo_delito']
    limits = [(0,2),(3,10),(11,20),(21,50),(50,3000),(3100,5100),(5101,7100),(7101,10100),(20100,22101)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locations=['Argentina'],
            locationmode = 'country names',
            lon = df_sub['long'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = 5,
                color = colors[i%5],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = 'crimes'))

    fig.update_layout(
            title_text = '2016-2021 AR city crimes<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'south america',
                landcolor = 'rgb(217, 217, 217)',
            )
        )
    fig.show()

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

def bar_plot(df: pd.DataFrame) -> None:
    fig = px.bar(df, x="franja", y="delitos", facet_col='anio', facet_col_wrap=3,
                 text_auto='.2s',
                title='Evolución de delitos pre y post pandemia')
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    fig.show()

def rose_plot(df:pd.DataFrame, graph: str) -> None:
    fig = px.bar_polar(df, r="cantidad", theta="anio",
                   title='Evolución de patrones delictivos en CABA [2016-2021]',
                   color="tipo_delito" if graph == "delito" else "dia", #template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Oryel_r)

    fig.update_layout(
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        #polar = dict(# setting parameters for the second plot would be polar2=dict(...)
        #sector = [120,240],)
        )

    fig.show()

if __name__ == '__main__':
    df = load_datasets(FILENAMES)
    # save_csv(df, 'legacy_2016_2021.csv')
    print(df.dtypes)
    print(f'Total rows: {len(df)}')
    print(df.groupby(by=['dia']).size().reset_index(name='delitos'))
    show_data(df)
    df_rose_delito, df_rose_dia = rose_df(df)
    rose_plot(df_rose_delito, 'delito')
    rose_plot(df_rose_dia, 'dia')
    ts_df = bar_plot_df(df)
    bar_plot(ts_df)
    