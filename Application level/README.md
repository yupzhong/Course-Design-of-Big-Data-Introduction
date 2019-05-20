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

> 数据脱敏的定义为：指对某些敏感信息通过脱敏规则进行数据的变形，实现敏感隐私数据的可靠保护。在涉及客户安全数据或者一些商业性敏感数据的情况下，在不违反系统规则条件下，对真实数据进行改造并提供测试使用，如身份证号、手机号、卡号、客户号等个人信息都需要进行数据脱敏。

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

```python
import pandas as pd
count_all = 0
count_4 = 0
for df in pd.read_csv(open("../../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv", 'r'), chunksize=100000):
    count_user = df['behavior_type'].value_counts()
    count_all += count_user[1] + count_user[2] + count_user[3] + count_user[4]
    count_4 += count_user[4]
ctr = count_4 / count_all
print(ctr)
```
```CTR = 购买数/操作总数 = 232579 / 23291027 = 0.009985776926023916 ≈ 1%```
#### 用户行为统计

## 心得体会


  [1]: https://tianchi.aliyun.com/competition/entrance/231522/information
  [2]: https://gtms01.alicdn.com/tps/i1/TB1WNN4HXXXXXbZaXXXwu0bFXXX.png
