# double_12
import pandas as pd
import matplotlib.pyplot as plt

count_hour_1211 = {}
count_hour_1212 = {}
for i in range(24):
    time_str11 = '2014-12-11 %02.d' % i
    time_str12 = '2014-12-12 %02.d' % i
    count_hour_1211[time_str11] = [0, 0, 0, 0]
    count_hour_1212[time_str12] = [0, 0, 0, 0]
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H')
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'),
                      parse_dates=['time'],
                      index_col=['time'],
                      date_parser=dateparse,
                      chunksize=50000):
    try:
        for i in range(24):
            time_str11 = '2014-12-11 %02.d' % i
            time_str12 = '2014-12-12 %02.d' % i
            tmp11 = df[time_str11]['behavior_type'].value_counts()
            tmp12 = df[time_str12]['behavior_type'].value_counts()
            for j in range(len(tmp11)):
                count_hour_1211[time_str11][tmp11.index[j] - 1] += tmp11[tmp11.index[j]]
            for j in range(len(tmp12)):
                count_hour_1212[time_str12][tmp12.index[j] - 1] += tmp12[tmp12.index[j]]
    except StopIteration:
        print("finish data process")
        break

df_1211 = pd.DataFrame.from_dict(count_hour_1211, orient='index')
df_1212 = pd.DataFrame.from_dict(count_hour_1212, orient='index')
df_1112 = pd.concat([df_1211, df_1212])

f1 = plt.figure(1)
df_1112.plot(kind='bar')
plt.legend(loc='best')
plt.title('behavior count of U in 12-11~12-12')
plt.show()

f2 = plt.figure(2)
df_1112[3].plot(kind='bar')
plt.legend(loc='best')
plt.title('buy in 12-11~12-12')
plt.show()
