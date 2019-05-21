# 应用级
## 方案简介
移动推荐算法
### 整体方案简介
以移动电商平台的真实用户-商品行为数据为基础来构建商品推荐模型
### 分级任务简介
1. 完成基础的数据可视化
2. 简单的基于规则的预测
## 数据集说明
- 数据集大小
1.0GB
- 数据集来源
[阿里天池][1]
## 工具说明
- CPU：Intel® Core™ i5-7300HQ Processor
- 内存：8GB
## 成果展示
### 数据内容
20000用户的完整行为数据以及百万级的商品信息。数据包含两个部分。

| 字段 | 字段说明 | 提取说明 |
| ---  | -------- | -------- |
| user_id | 用户标识 | 抽样&字段脱敏 |
|  item_id | 商品标识 | 字段脱敏 |
| behavior_type | 用户对商品的行为类型 | 包括浏览、收藏、加购物车、购买，对应取值分别是1、2、3、4|
| item_category | 商品分类标识 | 字段脱敏 |
| time | 行为时间 | 精确到小时级别 |

第二个部分是商品子集（P）,表名为tianchi_fresh_comp_train_item，包含如下字段：

| 字段 | 字段说明 | 提取说明 |
| ---  | -------- | -------- |
|  item_id | 商品标识 | 字段脱敏 |
| item_category | 商品分类标识 | 字段脱敏 |

> 数据脱敏：指对某些敏感信息通过脱敏规则进行数据的变形，实现敏感隐私数据的可靠保护。在涉及客户安全数据或者一些商业性敏感数据的情况下，在不违反系统规则条件下，对真实数据进行改造并提供测试使用，如身份证号、手机号、卡号、客户号等个人信息都需要进行数据脱敏。

### 最终目标
通过训练数据建立推荐模型,预测12.19这一天用户在P上的购买情况。
### 评估指标
采用经典的精确度(precision)、召回率(recall)和F1值作为评估指标。具体计算公式如下：
![计算公式][2]  
其中PredictionSet为算法预测的购买数据集合，ReferenceSet为真实的答案购买数据集合。
### 数据可视化
在建立模型之前,我们先进行一些简单的可视化,对数据内涵进行初步挖掘。
#### 点击购买转化率(CTR)

> CTR（Click-Through-Rate）即点击通过率，是互联网广告常用的术语，指网络广告（图片广告/文字广告/关键词广告/排名广告/视频广告等）的点击到达率，即该广告的实际点击次数（严格的来说，可以是到达目标页面的数量）除以广告的展现量（Show content）。对于电商平台来说,即为购买数/操作总数。

源代码如下：
```python
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
```
```CTR = 购买数/操作总数 = 232579 / 23291027 = 0.009985776926023916 ≈ 1%```
即用户平均操作100次才会执行一次购买操作。
#### 用户行为统计
11月18-12月18，用户每日操作次数如下图：
![user][3]  
可见用户操作只在双十二期间剧增，而其他操作较为均衡，这为我们下一步的操作提供思路。
源代码如下：
```python
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
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_trai    n_user.csv", 'r'),
    parse_dates=['time'],
    index_col=['time'], 
    date_parser=dateparse,
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
```
#### 商品行为统计
11月18-12月18，商品每日操作次数如下图：
![product][4]  
与我们上一步的结果相互印证。  
源代码如下：
```python
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
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H')
df_p = pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_item.csv", 'r'), index_col=False)
for df in pd.read_csv(open("../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'),
    parse_dates=['time'], 
    index_col=['time'], 
    date_parser=dateparse,
    chunksize=100000):
    try:
        df = pd.merge(df.reset_index(), df_p,on=['item_id']).set_index('time')
        for i in range(31):
            if i <= 12:
                date = '2014-11-%d' % (i + 18)
            else:
                date = '2014-12-%d' % (i - 12)
            count_day[date] += df[date].shape[0]
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
```
#### 双十二考察
经过上面的分析，下面来考察12-11与12-12这两天，来观察用户在这两天内的操作习惯：
![double12][5]  
可以看出用户操作的高峰期都在晚上9点到11点，而浏览（0号）的操作数都比其他操作（加购物车，收藏，购买）要多得多，但是这并不能体现双十二的特点，下面来特别观察购买操作。
![double12_2][6]  
显然，双十二0点购买数与其他时段相比剧增，这正体现了双十二的特点。  
源代码如下：
```python
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
```
### 基于规则的预测
#### 规则提出
根据生活常识，我们很容易就得出加购物车与购买操作有强关联性，于是我们提出一条规则：
```
在 T 时间内加购物车而未购买的用户最终会选择购买
```
接下来我们来确定这个最优参数T。
#### 数据分析
我们对数据中的加购物车、购买的时间做差，得到时间差，绘制出“加购物车-购买”时间差图：
![此处输入图片的描述][7]  
由图可知，绝大部分用户“加购物车-购买”时间差都在20-30小时内，这里为简单起见，取T=一天24小时。则最终规则为：
```
在12月18日加购物车而未购买的用户最终会在12月19日选择购买
```
事实上这也符合我们的购物习惯。
#### 规则验证
导出预测集如下：  
![excel][8]  
将所生成的csv文件`tianchi_mobile_recommendation_predict.csv`提交阿里天池，得到F1评分如下：  
![predict][9]  
可见简单的方法效果并不算特别差。  
源代码如下：
```python
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
```
## 心得体会
1. 学习了pandas，numpy，matplotlib等python库
2. 初步了解了数据可视化
3. 初步了解了数据分析的基本流程

  [1]: https://tianchi.aliyun.com/competition/entrance/231522/information
  [2]: https://gtms01.alicdn.com/tps/i1/TB1WNN4HXXXXXbZaXXXwu0bFXXX.png
  [3]: https://s2.ax1x.com/2019/05/21/EzUev4.png
  [4]: https://s2.ax1x.com/2019/05/21/EzaoTI.png
  [5]: https://s2.ax1x.com/2019/05/21/Ez0bfx.png
  [6]: https://s2.ax1x.com/2019/05/21/EzsUEQ.png
  [7]: https://s2.ax1x.com/2019/05/21/Ez63m8.png
  [8]: https://s2.ax1x.com/2019/05/21/Ez6DmT.jpg
  [9]: https://s2.ax1x.com/2019/05/21/Ezck3n.png
