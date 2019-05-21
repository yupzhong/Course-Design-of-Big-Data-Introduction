# user
import pandas as pd
import matplotlib.pyplot as plt
import csv


def row_dict_to_csv(raw_dict={}, csv_file=""):
    with open(csv_file, 'w') as f:
        w = csv.writer(f)
        w.writerows(raw_dict.items())


count_day = {}
for i in range(31):
    if i <= 12:
        date = '2014-11-%d' % (i + 18)
    else:
        date = '2014-12-%d' % (i - 12)
    count_day[date] = 0
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H')
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'),
                      parse_dates=['time'], index_col=['time'], date_parser=dateparse,
                      chunksize=100000):
    try:
        for i in range(31):
            if i <= 12:
                date = '2014-11-%d' % (i + 18)
            else:
                date = '2014-12-%d' % (i - 12)
            count_day[date] += df[date].shape[0]
    except StopIteration:
        print("finish data process")
        break
row_dict_to_csv(count_day, "../data/count_day.csv")
df_count_day = pd.read_csv(open("../data/count_day.csv", 'r'), header=None, names=['time', 'count'])
df_count_day = df_count_day.set_index('time')
df_count_day['count'].plot(kind='bar')
plt.title('behavior count of U by date')
plt.legend(loc='best')
plt.show()
