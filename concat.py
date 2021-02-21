import pandas as pd
import os
from tqdm import tqdm

root = './payloads'
csvs = []

for dirpath, dirnames, filenames in os.walk(root):
    for file in filenames:
        if '.csv' in file:
            csvs.append(os.path.abspath(os.path.join(dirpath, file)))

columns =  ['hi'
            , 'icon'
            , 'low'
            , 'overall'
            , 'provider'
            , 'sort_city'
            , 'sort_state'
            , 'sort_zip'
            , 'text'
           ]

df_from_each_file = [pd.read_csv(file, names=columns) for file in tqdm(csvs)]
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df.to_csv('payload_concat.csv', index=True)
