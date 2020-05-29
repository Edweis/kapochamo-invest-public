import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
import csv
import os
from datetime import datetime 

center_index = 99
data_path = '../data/ticks'

files = os.listdir(data_path)
files.sort()
files

def get_figure_for_df(df, name):
   return go.Candlestick(
          name= name,
          x=df['openTime'],
          open=df['open'],
          high=df['high'],
          low=df['low'],
          close=df['close']
      )

def get_file(file):
    method = 'RAW'
    df = pd.read_csv(f'{data_path}{file}')
    df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')
    
    if method == 'RAW':
        return df
    
    std = df['open'].std()
    mean = df['open'].mean()
    if method == 'NORMALIZE':
        df['open'] = (df['open'] - mean) / std
        df['high'] = (df['high'] - mean) / std
        df['low'] = (df['low'] - mean) / std
        df['close'] = (df['close'] - mean) / std
        return df
    
    center = df.loc[center_index, 'close']
    if method == 'CENTRAL':
        df['open'] = 100*(df['open'] - center) / df['open']
        df['high'] = 100*(df['high'] - center) / df['high']
        df['low'] = 100*(df['low'] - center) / df['low']
        df['close'] = 100*(df['close'] - center) / df['close']
        return df
    return df

def candlestick(files):
  first = get_file(files[0])
  max_ = first['high'].max()
  min_ = first['low'].min()
  event_time = first.loc[center_index, 'openTime']

  figures = []
  for file in files:
      df = get_file(file)
      max_ = max(max_, df['high'].max())
      min_ = min(min_, df['low'].min())
      figure = get_figure_for_df(df, file)
      figures.append(figure)

  fig = go.Figure(data=figures)
  fig.update_layout(
    title= {
     'text': ', '.join(files),
     'y':0.9,
     'x':0.5,
     'xanchor': 'center',
     'yanchor': 'top'
    },
   font=dict(
    family="Courier New, monospace",
    size=20,
    color="#7f7f7f"
  ))
  fig.add_shape(
    # Line Vertical
    dict(
        type="line",
        x0=event_time,
        y0=min_,
        x1=event_time,
        y1=max_,
        line=dict(
            color="RoyalBlue",
            width=1
        )
  ))
  fig.show()
 
 
candlestick(files)





