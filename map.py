import pandas as pd
from urllib.request import urlopen
import numpy as np
import plotly.express as px
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv('data_with_fips.csv')

grouped_df = df[['overall', 'STCOUNTYFP']].groupby(['STCOUNTYFP']).mean().reset_index()
grouped_df = grouped_df[~grouped_df['STCOUNTYFP'].isnull()]
grouped_df['fips'] = grouped_df.apply(lambda row: str(int(row['STCOUNTYFP'])).rjust(5,'0'), axis=1)

min_accuracy = grouped_df['overall'].min()
max_accuracy = grouped_df['overall'].max()

fig = px.choropleth(grouped_df, geojson=counties, locations='fips', color='overall',
                           color_continuous_scale="Viridis",
                           range_color=(min_accuracy, max_accuracy),
                           scope="usa",
                           labels={'overall':'overall accuracy'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()