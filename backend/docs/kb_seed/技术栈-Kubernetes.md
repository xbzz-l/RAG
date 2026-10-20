# Kubernetes（K8s）

## 一、是什么
Kubernetes 是 **Google 开源的容器编排平台**（2014 年，现由 CNCF 托管），简称 K8s。定位：自动化部署、扩缩容和管理容器化应用，是云原生时代的"操作系统"。

## 二、核心知识
- **集群架构**：控制平面（Master：API Server/etcd/Scheduler/Controller Manager）+ 工作节点（Node：kubelet/kube-proxy/容器运行时）
- **Pod**：最小调度单元，一个 Pod 可含多个共享网络与存储的容器
- **控制器**：Deployment（无状态应用，滚动更新/回滚）、StatefulSet（有状态应用，稳定标识）、DaemonSet（每节点一个）、Job/CronJob（任务）
- **Service**：稳定的虚拟 IP 与负载均衡入口（ClusterIP/NodePort/LoadBalancer）；Service + Deployment 解耦
- **网络模型**：扁平网络，Pod 间互通；Ingress 做七层 HTTP 路由
- **存储**：PV（持久卷）/PVC（卷声明）抽象底层存储
- **配置管理**：ConfigMap（配置）、Secret（敏感信息）
- **调度与资源**：requests/limits 资源声明；label/selector 标签选择；亲和性与污点容忍
- **探针**：liveness（存活）/readiness（就绪）健康检查
- **弹性伸缩**：HPA 按 CPU/内存/指标自动扩缩副本

## 三、作用与常用场景
- 微服务生产级编排与自动运维
- 弹性伸缩、滚动发布、故障自愈
- 混合云/多云统一管理
- CI/CD 流水线落地环境

## 四、基于什么语言/底层原理
- **开发语言**：Go；声明式 API：用户提交期望状态（YAML），控制器循环（Reconcile）对比实际状态并持续调谐
- **etcd**：分布式键值库存储集群状态，保证一致性

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 自动化运维：自愈、扩缩容、滚动发布 | 概念繁多（30+ 核心对象），学习曲线极陡 |
| 云原生标准，生态庞大 | 集群搭建与维护成本高（资源消耗大） |
| 声明式管理，基础设施即代码 | 中小项目属于"杀鸡用牛刀" |
| 大规模分布式场景的业界标准 | 网络/存储问题排查门槛高 |

## 六、学习建议
前提：Docker + Linux 基础。路径：核心概念（Pod/Deployment/Service）→ minikube 本地实操 → 配置与存储 → Ingress → 生产实践。岗位方向偏运维/DevOps/云原生才需要深入学习。

> 参考来源：菜鸟教程 runoob.com、Kubernetes 官方文档
