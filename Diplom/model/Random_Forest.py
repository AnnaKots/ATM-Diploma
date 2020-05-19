import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor
import statistics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_excel('dataset.xlsx', sheet_names='Sheet1', parse_dates=['Transaction Date'])
df.rename(columns={'ATM Name': u'Банкомат',
                   'Festival Religion': u'Религиозный фестиваль', 'Working Day': u'Рабочий день',
                   'Holiday Sequence': u'День в последовательности рабочих дней',
                   'No Of Withdrawals': u'Общее число снятий',
                   'No Of XYZ Card Withdrawals': u'Число снятий с карт банка',
                   'No Of Other Card Withdrawals': u'Число снятий с карт других банков',
                   'Total amount Withdrawn': u'Общая сумма снятий',
                   'Amount withdrawn XYZ Card': u'Сумма снятий с карт банка',
                   'Amount withdrawn Other Card': u'Сумма снятий с карт других банков'}, inplace=True)

df.index = df['Transaction Date']

master_df = df.loc[(df['Transaction Date'] >= '2013-01-01') & (df['Transaction Date'] < '2016-06-02')]

master_df.index.names = [u'Дата транзакции']

week = [u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресенье']
month = [u'Январь', u'Февраль', u'Март', u'Апрель', u'Май', u'Июнь', u'Июль', u'Август', u'Сентябрь', u'Октябрь',
         u'Ноябрь', u'Декабрь']

master_df[u'День'] = master_df.index.to_series().dt.day
master_df[u'День недели'] = master_df.index.to_series().apply(lambda x: week[x.weekday()])
master_df[u'Месяц'] = master_df.index.to_series().apply(lambda x: month[x.month - 1])
master_df[u'Год'] = master_df.index.to_series().dt.year

master_df.drop([u'Банкомат', 'Transaction Date', u'Общее число снятий', u'Число снятий с карт банка',
                u'Число снятий с карт других банков', u'Сумма снятий с карт банка',
                u'Сумма снятий с карт других банков', 'Weekday', u'Год'], axis='columns', inplace=True)

x = master_df.drop(u'Общая сумма снятий', axis='columns')  # матрица "объекты-признаки"
y = master_df[u'Общая сумма снятий']  # вектор ответов


# преобразовываем series к задаче контролируемого обучения
def series_to_supervised(data, n_in=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # входная последовательность (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
    # соединяем их вместе
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # удаляем строки с пустыми значениями
    if dropnan:
        agg.dropna(inplace=True)
    return agg


values = x.values
onehotencoder = make_column_transformer((OneHotEncoder(), [0, 1, 2, 3, 4, 5]), remainder="passthrough")
values = onehotencoder.fit_transform(values).toarray()

# делаем все данные типом float
values = values.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))

scaled = scaler.fit_transform(values)

# frame as supervised learning
X = series_to_supervised(scaled, 1)

X.index = x.loc[(x.index < '2016-06-01')].index
y = y.loc[y.index < '2016-06-01']
y.index = x.loc[(x.index < '2016-06-01')].index

n_size = -580
X_train, y_train = X[:n_size], y[:n_size]
X_test, y_test = X[n_size:], y[n_size:]

model = RandomForestRegressor(n_estimators=500, max_features=3, random_state=42).fit(X_train, y_train)
predictions = model.predict(X_test)

# Calculate the absolute errors
print('R^2 ' + str(r2_score(y_test, predictions)))
print('MAE ' + str(mean_absolute_error(y_test, predictions)))
print('MSE ' + str(mean_squared_error(y_test, predictions)))
print('Максимальное отклонение ' + str(max(abs(y_test - predictions))))
print('Медианное отклонение ' + str(statistics.median(abs(y_test - predictions))))
