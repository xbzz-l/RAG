# Elasticsearch（ES）

## 一、是什么
Elasticsearch 是 **基于 Lucene 的分布式全文搜索引擎**，属于 ELK 技术栈核心（Elasticsearch + Logstash + Kibana）。定位：海量数据的近实时搜索与分析引擎。

## 二、核心知识
- **倒排索引**：词项（Term）→ 文档列表的映射，全文搜索快的根本原因
- **文档与索引**：Index（索引，类比数据库）→ Type（已废弃）→ Document（JSON 文档）→ Field（字段）；Mapping 定义字段类型
- **分片 Shard**：索引水平拆分为主分片（可配）+ 副本分片（冗余），实现分布式与高可用
- **检索**：全文查询 match、短语匹配 match_phrase、多字段 multi_match、精确查询 term、范围 range、复合查询 bool（must/should/must_not/filter）
- **聚合 Aggregation**：桶聚合（terms/date_histogram）、指标聚合（avg/max/sum）、嵌套聚合，数据分析利器
- **分词器**：standard/ik（中文）、自定义词典；分词结果直接影响搜索召回
- **相关性评分**：TF-IDF → BM25 算法（默认），explain 查看评分依据
- **集群**：节点角色（master/data/coordinating）、健康状态（green/yellow/red）
- **写入原理**：近实时（refresh 1 秒可见）、translog 防丢失、段合并

## 三、作用与常用场景
- 站内搜索/商品搜索（中文场景配合 ik 分词）
- 日志分析（ELK 收集展示海量日志）
- 数据分析与监控大盘（聚合 + Kibana 可视化）
- 与 MySQL 配合：MySQL 存原始数据，ES 建索引供搜索

## 四、基于什么语言/底层原理
- **开发语言**：Java 编写，底层 Lucene 索引库；RESTful JSON API 交互（HTTP 9200 端口）
- **与 MySQL 对比**：ES 靠倒排索引做模糊/全文搜索（MySQL LIKE 无法命中索引），但事务与写入可靠性弱于 MySQL

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 全文搜索与聚合分析能力极强 | 内存/磁盘资源消耗大 |
| 分布式近实时，扩展性好 | 写入一致性弱（不适合做主存储） |
| REST API 易用，生态（ELK）完整 | 查询语法（DSL）学习成本不低 |
| 水平扩展、自动分片 | 运维调优复杂（分片/JVM/分词） |

## 六、学习建议
先理解倒排索引原理（面试必问）→ DSL 查询与聚合实操 → ik 分词器 → 集群概念 → 用 ELK 做一个日志收集项目巩固。菜鸟教程有 Elasticsearch 教程可打基础。

> 参考来源：菜鸟教程 runoob.com、Elasticsearch 官方文档
