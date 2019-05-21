# product
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
batch = 0
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H')
df_p = pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_item.csv", 'r'), index_col=False)
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'),
                      parse_dates=['time'], index_col=['time'], date_parser=dateparse,
                      chunksize=100000):
    try:
        df = pd.merge(df.reset_index(), df_p, on=['item_id']).set_index('time')
        for i in range(31):
            if i <= 12:
                date = '2014-11-%d' % (i + 18)
            else:
                date = '2014-12-%d' % (i - 12)
            count_day[date] += df[date].shape[0]
        batch += 1
        print('chunk %d done.' % batch)
    except StopIteration:
        print("finish data process")
        break

row_dict_to_csv(count_day, "../data/count_day_of_p.csv")
df_count_day = pd.read_csv(open("../data/count_day_of_p.csv", 'r'),
                           header=None,
                           names=['time', 'count'])
df_count_day = df_count_day.set_index('time')
df_count_day['count'].plot(kind='bar')
plt.legend(loc='best')
plt.title('behavior count of P by date')
plt.show()
