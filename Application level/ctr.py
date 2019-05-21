# CTR
import pandas as pd

count_all = 0
count_4 = 0
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'), chunksize=100000):
    try:
        count_user = df['behavior_type'].value_counts()
        count_all += count_user[1] + count_user[2] + count_user[3] + count_user[4]
        count_4 += count_user[4]
    except StopIteration:
        print("Iteration is stopped.")
        break
ctr = count_4 / count_all
print(ctr)
