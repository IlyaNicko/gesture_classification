import pandas as pd


def get_sensor_list(Pilot_id, mounts, print_active=False):
    """
    Функция печати и импорта в память всех номеров датчиков
    Аргументы функции:
    Pilot_id - номер пилота,
    mounts - словарь с данными. 
    """
    X_train=mounts[Pilot_id]['X_train']

    df = pd.DataFrame(
        data = X_train, 
        index = [s for s in range(X_train.shape[0])], 
        columns = [s for s in range(X_train.shape[1])]
    ).T

    # Создадим список индексов активных и пассивных датчиков. Среднее значение сигнала не превышает 200 единиц.
    active_sensors, passive_sensors = list(), list()
      
    for i in range(df.shape[0]):
        # если средняя амплитуда превышает 200, то добавляем индекс в список 'active_sensors' (надежных датчиков). 
        if df.iloc[i].mean() > 200:
            active_sensors.append(i)
        
        #Остальные датчики с малой амплитудой - в список ненадёжных.      
        else:
            passive_sensors.append(i)

    if print_active is True:
        print(f"Активные датчики пилота " + str(Pilot_id) + ": ", active_sensors)
        print(f"Пассивные датчики пилота " + str(Pilot_id) + ": ", passive_sensors) 
    
    return active_sensors, passive_sensors #, reliable_sensors, unreliable_sensors
