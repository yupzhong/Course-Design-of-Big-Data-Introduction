# rule
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H')
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'),
                      chunksize=100000):
    try:
        df_act_34 = df[df['behavior_type'].isin([3, 4])]
        df_act_34.to_csv('../data/act_34.csv',
                         columns=['time', 'user_id', 'item_id', 'behavior_type'],
                         index=False, header=False,
                         mode='a')
    except StopIteration:
        print("finish.")
        break

data_file = open('../data/act_34.csv', 'r')
try:
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H')
    df_act_34 = pd.read_csv(data_file,
                            parse_dates=[0],
                            date_parser=dateparse,
                            index_col=False)
    df_act_34.columns = ['time', 'user_id', 'item_id', 'behavior_type']
    df_act_34 = df_act_34.drop_duplicates(['user_id', 'item_id', 'behavior_type'])
finally:
    data_file.close()

df_time_3 = df_act_34[df_act_34['behavior_type'].isin(['3'])][['user_id', 'item_id', 'time']]
df_time_4 = df_act_34[df_act_34['behavior_type'].isin(['4'])][['user_id', 'item_id', 'time']]
df_time_3.columns = ['user_id', 'item_id', 'time3']
df_time_4.columns = ['user_id', 'item_id', 'time4']
del df_act_34
df_time = pd.merge(df_time_3, df_time_4, on=['user_id', 'item_id'], how='outer')
df_time_34 = df_time.dropna()
df_time_3 = df_time[df_time['time4'].isnull()].drop(['time4'], axis=1)
df_time_3 = df_time_3.dropna()
df_time_3.to_csv('../data/time_3.csv',
                 columns=['user_id', 'item_id', 'time3'],
                 index=False)
df_time_34.to_csv('../data/time_34.csv',
                  columns=['user_id', 'item_id', 'time3', 'time4'],
                  index=False)

data_file = open('../data/time_34.csv', 'r')
try:
    df_time_34 = pd.read_csv(data_file,
                             parse_dates=['time3', 'time4'],
                             index_col=False)
finally:
    data_file.close()

delta_time = df_time_34['time4'] - df_time_34['time3']
delta_hour = []
for i in range(len(delta_time)):
    d_hour = delta_time[i].days * 24 + delta_time[i]._h
    if d_hour < 0:
        continue
    else:
        delta_hour.append(d_hour)

f1 = plt.figure(1)
plt.hist(delta_hour, 30)
plt.xlabel('hours')
plt.xticks(np.arange(0, 100, 10))
plt.ylabel('count')
plt.title('cart - buy time decay')
plt.show()

data_file = open('../data/time_3.csv', 'r')
try:
    df_time_3 = pd.read_csv(data_file,
                            parse_dates=['time3'],
                            index_col=['time3'])
finally:
    data_file.close()
ui_pred = df_time_3['2014-12-18']
data_file = open('../data/fresh_comp_offline/tianchi_fresh_comp_train_item.csv', 'r')
try:
    df_item = pd.read_csv(data_file, index_col=False)
finally:
    data_file.close()
ui_pred_in_P = pd.merge(ui_pred, df_item, on=['item_id'])
ui_pred_in_P.to_csv('../data/tianchi_mobile_recommendation_predict.csv',
                    columns=['user_id', 'item_id'],
                    index=False)
