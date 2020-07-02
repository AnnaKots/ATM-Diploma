#!/usr/bin/env python
# coding: utf-8

from tensorflow.keras.models import load_model
from keras import backend as K
import pandas as pd
import sys
import warnings

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        atm_name = sys.argv[1]
        date = sys.argv[2]
        festival = int(sys.argv[3])
        working_day = int(sys.argv[4])

        


        def root_mean_squared_error(y_true, y_pred):
            return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))


        # Восстановим в точности ту же модель, включая веса и оптимизатор из HDF5 файла
        model = load_model('mlp_final.h5', custom_objects={'root_mean_squared_error': root_mean_squared_error})

        from sklearn.externals import joblib

        # Загружаем модель из файла
        encoder = joblib.load("encoder1.save")
        data = pd.DataFrame(
            {u'Банкомат': [atm_name], u'Дата': [date], u'Праздник': [int(festival)], u'Рабочий день': [working_day]})

        data[u'Дата'] = data[u'Дата'].apply(pd.to_datetime)

        week = [u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресенье']
        month = [u'Январь', u'Февраль', u'Март', u'Апрель', u'Май', u'Июнь', u'Июль', u'Август', u'Сентябрь',
                 u'Октябрь',
                 u'Ноябрь', u'Декабрь']

        data[u'День'] = data[u'Дата'].dt.day
        data[u'День недели'] = data[u'Дата'].apply(lambda x: week[x.weekday()])
        data[u'Месяц'] = data[u'Дата'].apply(lambda x: month[x.month - 1])
        data.drop([u'Дата'], inplace=True, axis=1)

        encoded_data = encoder.transform(data)
        result = model.predict(encoded_data)
        print(int(result[0][0]))
