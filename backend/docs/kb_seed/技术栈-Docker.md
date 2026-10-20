# Docker

## 一、是什么
Docker 是 **开源容器化平台**（2013 年发布）。核心思想：将应用及其全部依赖打包成标准化的"容器"，实现"一次构建，处处运行"，解决环境不一致问题。

## 二、核心知识
- **镜像 Image**：只读模板，分层构建（每一层对应 Dockerfile 一条指令）；Dockerfile 指令：FROM/RUN/COPY/CMD/ENTRYPOINT/EXPOSE
- **容器 Container**：镜像的运行实例，在镜像层之上加可写层；生命周期：run/start/stop/rm
- **仓库 Registry**：镜像托管与分发（Docker Hub、阿里云镜像仓库）
- **网络**：bridge（默认桥接）、host、none、自定义网络；容器间通过服务名互访
- **数据卷 Volume**：持久化容器数据（-v 挂载），与容器生命周期解耦
- **常用命令**：docker build/pull/push/run/exec/logs/ps/images/rmi/compose
- **Docker Compose**：docker-compose.yml 编排多容器应用（一键启动整套服务）
- **资源限制**：--cpus/--memory 限制容器资源
- **多阶段构建**：构建与运行分离，压缩镜像体积

## 三、作用与常用场景
- 开发环境一致性：新成员一键起全套依赖（MySQL/Redis 等）
- 持续集成/持续部署（CI/CD）：流水线标准化产物
- 微服务部署：每服务一容器
- 应用交付：交付镜像而非源码+部署文档

## 四、基于什么语言/底层原理
- **开发语言**：Go 编写
- **底层原理**：不是虚拟机！基于 Linux 内核特性——命名空间 Namespace（进程/网络/文件系统隔离）+ 控制组 Cgroup（资源限制）+ UnionFS 联合文件系统（镜像分层）；共享宿主机内核，轻量秒级启动

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 环境一致，消除"我电脑上能跑"问题 | Windows/Mac 上跑 Linux 容器有虚拟化开销 |
| 轻量高效：秒级启动，资源占用远小于虚拟机 | 镜像体积膨胀、层数滥用需治理 |
| 部署简单，迁移方便 | 容器安全（逃逸/镜像供应链）需关注 |
| 生态庞大（K8s 默认容器运行时） | 学习曲线：镜像/网络/卷概念体系 |

## 六、学习建议
先理解容器 vs 虚拟机差异 → Dockerfile 写镜像 → 常用命令实操 → Volume 与网络 → Docker Compose 编排（如 MySQL+Redis+应用三件套）→ 进阶了解 K8s。菜鸟教程 Docker 教程适合打基础。

> 参考来源：菜鸟教程 runoob.com、Docker 官方文档
