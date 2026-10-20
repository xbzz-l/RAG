# Linux

## 一、是什么
Linux 是 **开源类 Unix 操作系统内核**（Linus Torvalds 1991 年发布），配合 GNU 工具链组成完整操作系统（发行版如 Ubuntu/CentOS/Debian）。定位：服务器操作系统事实标准（超 90% 服务器运行 Linux）。

## 二、核心知识
- **文件系统**：一切皆文件；目录结构（/etc 配置、/var 日志、/usr 程序、/home 家目录、/tmp 临时）；权限体系 rwx + 属主/属组（chmod/chown）
- **常用命令**：ls/cd/pwd/mkdir/rm/cp/mv（文件操作）、cat/tail/head/less（查看）、grep（过滤）、find（查找）、ps/top（进程）、df/du（磁盘）、chmod/chown（权限）
- **文本三剑客**：grep（检索）、sed（流编辑）、awk（列处理）
- **管道与重定向**：| 管道串联命令、>/>> 重定向、2>&1
- **进程管理**：前台/后台、kill 信号、systemctl 服务管理
- **用户与组**：useradd/passwd/sudo 提权
- **网络**：ip/ss/netstat/curl/ping；端口与防火墙（firewalld/iptables）
- **Shell 脚本**：bash 语法（变量/条件/循环/函数），crontab 定时任务
- **软件安装**：apt（Debian 系）/yum（RedHat 系）、源码编译、解压即用
- **日志**：/var/log 下系统与应用日志，journalctl

## 三、作用与常用场景
- 服务器运维（部署 Web 服务、数据库、中间件）
- 开发环境（后端开发日常操作服务器）
- 云原生基础（Docker/K8s 均基于 Linux）
- 嵌入式与 Android 底层

## 四、基于什么语言/底层原理
- **内核**：C 与汇编编写；宏内核架构；进程调度（CFS）、虚拟内存（页表）、虚拟文件系统 VFS、网络协议栈
- **发行版**：内核 + 包管理器 + 工具链的整合

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 免费开源、稳定、安全 | 桌面生态与软件丰富度弱于 Windows |
| 服务器性能与资源利用率高 | 命令行操作有学习门槛 |
| 高度可定制、可脚本化 | 图形界面操作习惯差异大 |
| 云计算/AI 场景第一选择 | 部分硬件驱动兼容性问题 |

## 六、学习建议
菜鸟教程 Linux 教程入门 → 动手装一个 Ubuntu 虚拟机 → 常用命令形成肌肉记忆 → Shell 脚本 → 部署一个真实项目到服务器（最能检验学习成果）。

> 参考来源：菜鸟教程 runoob.com、Linux 官方文档
