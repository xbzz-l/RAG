# 大数据：Hadoop 与 Spark

## 一、是什么
Hadoop 是 **Apache 开源的分布式大数据处理框架**（2006 年），让普通服务器集群存储和处理 TB/PB 级数据；Spark 是 **内存计算的大数据引擎**（2014 年成为 Apache 顶级项目），速度比 Hadoop MapReduce 快数十到上百倍。两者是传统大数据方向的核心。

## 二、核心知识
**Hadoop 三大组件**
- HDFS 分布式文件系统：NameNode（元数据）+ DataNode（数据块，默认 128MB，3 副本）；写一次读多次
- MapReduce 计算模型：Map（分而治之）→ Shuffle（分组排序）→ Reduce（汇总）
- YARN 资源调度：统一管理集群 CPU/内存资源

**Spark**
- 核心抽象 RDD（弹性分布式数据集）：不可变、可分区、容错（血缘 Lineage 重算）
- 常用 API：DataFrame / Dataset / Spark SQL（声明式处理，主流写法）
- 运行模式：本地、Standalone、YARN、K8s；Driver + Executor 架构
- 内存计算与 DAG 调度：惰性求值，Action 触发计算
- 生态：Spark SQL（结构化处理）、Spark Streaming（流处理）、MLlib（机器学习）、GraphX（图计算）

**大数据生态周边**
- 数据采集：Flume、Sqoop、Canal
- 消息管道：Kafka
- 数仓：Hive（SQL on Hadoop）、数仓分层 ODS/DWD/DWS/ADS
- 实时计算：Flink（主流，流批一体）
- 协调服务：ZooKeeper

## 三、作用与常用场景
- 海量日志分析与用户行为分析
- 离线数仓建设（Hive/Spark SQL ETL）
- 推荐系统数据处理、风控计算

## 四、基于什么语言/底层原理
- **开发语言**：Hadoop 用 Java；Spark 核心用 Scala，API 支持 Java/Python（PySpark）/SQL
- **分布式原理**：数据分片存储 + 移动计算而非移动数据（本地计算）+ 副本容错 + 主从架构

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 处理海量数据能力强、成本低（普通服务器） | 架构复杂、运维门槛高 |
| 生态完整（采集/存储/计算/数仓） | 不适合低延迟实时场景（Flink 弥补） |
| 容错性好（副本/血缘重算） | 小数据量场景效率反而不如单机 |
| Spark 内存计算速度快 | 资源消耗大，需专门集群 |

## 六、学习建议
前提：Java 或 Python + Linux 基础。路径：理解 HDFS 与 MapReduce 思想 → 搭建单机伪分布式环境实操 → Spark SQL/DataFrame 处理数据 → Hive 数仓分层 → Flink 入门。就业方向：大数据开发工程师。

> 参考来源：菜鸟教程 runoob.com、Apache Hadoop/Spark 官方文档
