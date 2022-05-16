import os
import glob

import numpy as pd
import pandas as pd

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/../data', '*.csv')
FILENAMES = glob.glob(PATH)
print(PATH)
tmp_legacy = []
tmp = []


def save_csv(dataframe: pd.DataFrame, filename: str) -> None:
    PATH_FILENAME = os.path.dirname(os.path.abspath(__file__)) + f'/../{filename}'
    print(f'Saving {PATH_FILENAME}...')
    dataframe.to_csv(PATH_FILENAME, index=False)

def append_df(dataframe: pd.DataFrame, filename: str) -> None:
    dataframe['uso_armas'] = ''
    tmp.append(dataframe)

def load_datasets(filenames: str) -> pd.DataFrame:
    for file in filenames:
        print(f'Loading dataset {file}...')
        df = pd.read_csv(file, index_col=None, sep=',', header=0)
        append_df(df, file)
    return pd.concat(tmp, axis=0, ignore_index=True)

def show_data(df: pd.DataFrame) -> None:
    print('2016 to 2021')
    print(df.iloc[1:10])
    #save_csv(df, 'legacy_2016_2021.csv')


if __name__ == '__main__':
    df = load_datasets(FILENAMES)
    print(df.dtypes)
    print(f'Total rows: {len(df)}')
    print(df.groupby(by=['dia']).size().reset_index(name='delitos'))
    show_data(df)