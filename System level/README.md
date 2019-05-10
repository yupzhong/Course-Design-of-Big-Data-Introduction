# 系统级
## 方案简介
### 整体方案简介
- 待定
### 分级任务简介
- 安装hadoop 3.1.2，并完成master-node集群搭建
## 数据集说明
- 数据集大小
- 数据集来源
## 工具说明
### 工作环境
- Windows 10 ，Vitualbox 6.0
### 虚拟化环境
- Ubuntu 18.04.2 LTS
- master 内存3G 分配储存空间10G host：10.12.223.57
- node   内存1G 分配储存空间10G host：10.12.217.189
### 分布式系统特征及选取原因
1. 分布式文件系统是大数据时代解决大规模数据存储问题的有效解决方案，HDFS 开源实现了GFS，可以利用由廉价硬件构成的计算机集群实现海量数据的分布式存储。
2. HDFS 具有兼容廉价的硬件设备、流数据读写、大数据集、简单的文件模型、强大的跨平台兼容性等特点。但是也要注意到，HDFS 也有自身的局限性，比如不适合低延迟数据访问、无法高效存储大量小文件和不支持多用户写入及任意修改文件等。
3. 块是HDFS的核心概念，一个大的文件会被拆分成很多个块。HDFS采用抽象的块概念，具有支持大规模文件存储、简化系统设计、适合数据备份等优点。
4. HDFS采用了主从（Master/Slave）结构模型，一个HDFS集群包括一个名称节点和若干个数据节点。名称节点负责管理分布式文件系统的命名空间；数据节点是分布式文件系统HDFS的工作节点，负责数据的存储和读取。
5. HDFS 采用了冗余数据存储，增强了数据可靠性，加快了数据传输速度。HDFS 还采用了相应的数据存放、数据读取和数据复制策略，来提升系统整体读写响应性能。HDFS 把硬件出错看成一种常态，设计了错误恢复机制。
## 问题挑战
- 问题
1. 安装过程中踩了不少坑，对Linux系统仍然不是很熟悉
2. 配置集群间网络连接有困难，计算机的网络原理有待进一步学习
3. hadoop的进一步操作有待学习
## 成果展示
[![ERK8Et.md.jpg](https://s2.ax1x.com/2019/05/10/ERK8Et.md.jpg)](https://imgchr.com/i/ERK8Et)
![ERKN8S.jpg](https://s2.ax1x.com/2019/05/10/ERKN8S.jpg)
[![ERK0Ds.md.jpg](https://s2.ax1x.com/2019/05/10/ERK0Ds.md.jpg)](https://imgchr.com/i/ERK0Ds)
[![ERKy5V.md.jpg](https://s2.ax1x.com/2019/05/10/ERKy5V.md.jpg)](https://imgchr.com/i/ERKy5V)
![ERKq2D.jpg](https://s2.ax1x.com/2019/05/10/ERKq2D.jpg)
[![ER1CPx.md.jpg](https://s2.ax1x.com/2019/05/10/ER1CPx.md.jpg)](https://imgchr.com/i/ER1CPx)
[![ERMwRO.jpg](https://s2.ax1x.com/2019/05/10/ERMwRO.jpg)](https://imgchr.com/i/ERMwRO)
[![ERMsLd.jpg](https://s2.ax1x.com/2019/05/10/ERMsLd.jpg)](https://imgchr.com/i/ERMsLd)
[![ERQVSO.md.jpg](https://s2.ax1x.com/2019/05/10/ERQVSO.md.jpg)](https://imgchr.com/i/ERQVSO)
![ERlGU1.jpg](https://s2.ax1x.com/2019/05/10/ERlGU1.jpg)
[![ERlzZ9.md.jpg](https://s2.ax1x.com/2019/05/10/ERlzZ9.md.jpg)](https://imgchr.com/i/ERlzZ9)
[![ER1dJ0.md.jpg](https://s2.ax1x.com/2019/05/10/ER1dJ0.md.jpg)](https://imgchr.com/i/ER1dJ0)
## 心得体会
- 完成了大数据入门环境hadoop的搭建，有助于进一步的学习并巩固各方面的知识
- 搭建过程中学到了很多知识，比如HDFS，Hbase，Hive，YARN，ssh，虽然限于知识水平有很多不能理解，但是我相信在今后的学习中会逐渐体现价值
## 参考资料
- http://hadoop.apache.org/docs/current/
- http://dblab.xmu.edu.cn/blog/install-hadoop-cluster/
- https://juejin.im/post/5c9643c05188252d805c77fa
