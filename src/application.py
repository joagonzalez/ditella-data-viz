import os
import glob

import numpy as pd
import pandas as pd

import plotly.graph_objects as go

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/../data', '*.csv')
FILENAMES = glob.glob(PATH)
print(PATH)


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
    #save_csv(df, 'legacy_2016_2021.csv')

def maps(df: pd.DataFrame):

    df['text'] = df['tipo_delito']
    limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(df.index)):
        fig.add_trace(go.Scattergeo(
            locations=['Argentina'],
            locationmode = 'country names',
            lon = df['long'],
            lat = df['lat'],
            text = df['text'],
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

if __name__ == '__main__':
    df = load_datasets(FILENAMES)
    print(df.dtypes)
    print(f'Total rows: {len(df)}')
    print(df.groupby(by=['dia']).size().reset_index(name='delitos'))
    show_data(df)
    maps(df)