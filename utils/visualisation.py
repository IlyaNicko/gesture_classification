import pandas as pd
import numpy as np

# графические библиотеки
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_all_sensors_plot(Pilot_id, timesteps:list, mounts, plot_counter=1):
    """
    Функция построения диаграммы показаний датчиков заданного временного периода. Аргументы функции:
    Pilot_id - номер пилота;
    timesteps - лист из двух временных периодов;
    mounts - словарь с данными;
    plot_counter - порядковый номер рисунка.
    """
    
    X_train=mounts[Pilot_id]['X_train']

    df = pd.DataFrame(
        data = X_train, 
        index = [s for s in range(X_train.shape[0])], 
        columns = [s for s in range(X_train.shape[1])]
    )
    
    fig = px.line(data_frame=df.iloc[timesteps[0]:timesteps[1],:])
    
    fig.update_layout(
        title=dict(text=f'Рис. {plot_counter} - сигналы датчиков пилота {Pilot_id}', x=.5, y=0.05, xanchor='center'), 
        xaxis_title_text = 'Время, сек', yaxis_title_text = 'Сигнал датчиков', # yaxis_range = [0, 3000],
        legend_title_text='Индекс <br>датчика',
        width=600, height=400,
        margin=dict(l=100, r=60, t=80, b=100),
    )

    # сохраним результат в папке figures. Если такой папки нет, то создадим её
    if not os.path.exists("figures"):
        os.mkdir("figures")

    fig.write_image(f'figures/fig_{plot_counter}.png', engine="kaleido")


def get_active_passive_sensors_plot(Pilot_id, timesteps:list, mounts, plot_counter=1):
    """
    Функция построения графика показаний активных и пассивных датчиков. Аргументы функции:
    Pilot_id - номер пилота;
    timesteps - лист из двух временных периодов;
    mounts - словарь с данными;
    plot_counter - порядковый номер рисунка.  
    """
    X_train=mounts[Pilot_id]['X_train']

    df = pd.DataFrame(
        data = X_train, 
        index = [s for s in range(X_train.shape[0])], 
        columns = [s for s in range(X_train.shape[1])]
    )

    # списки сенсоров
    active_sensors, passive_sensors = get_sensor_list(Pilot_id, mounts)  #, print_active=True

    #timesteps=[time_start, time_end]

    df = pd.DataFrame(
        data = X_train, 
        index = [s for s in range(X_train.shape[0])], 
        columns = [s for s in range(X_train.shape[1])]
    ).iloc[timesteps[0]:timesteps[1],:]
    
        
    df_1 = pd.DataFrame(df[active_sensors], columns=active_sensors)
    df_2 = pd.DataFrame(df[passive_sensors], columns=passive_sensors)

   
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=('активные датчики', 'пассивные датчики')
    )
    
    for i in df_1.columns: fig.add_trace(go.Scatter(x=df_1.index, y=df_1[i], name=str(df[i].name)), row=1, col=1)

    for i in df_2.columns: fig.add_trace(go.Scatter(x=df_2.index, y=df_2[i], name=str(df[i].name)), row=1, col=2)

    fig.update_layout(title={'text':f'Рис. {plot_counter} - Активные и пассивные датчики пилота {Pilot_id} в период {timesteps[0],timesteps[1]}', 'x':0.5, 'y':0.05}
    )

    fig.update_layout(width=1000, height=400, legend_title_text ='Номер датчика',
                        xaxis_title_text  = 'Время',  yaxis_title_text = 'Сигнал датчика', yaxis_range=  [0, 4000], 
                        xaxis2_title_text = 'Время', yaxis2_title_text = 'Сигнал датчика', yaxis2_range= [0 , 200],
                        margin=dict(l=100, r=60, t=80, b=100), 
                        #showlegend=False # легенда загромождает картинку
    )

    #fig.show()

    fig.write_image(f'figures/fig_{plot_counter}.png', engine="kaleido")
