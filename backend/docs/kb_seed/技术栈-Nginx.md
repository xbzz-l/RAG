# Nginx

## 一、是什么
Nginx 是 **高性能开源 Web 服务器与反向代理服务器**（俄罗斯 Igor Sysoev 2004 年开发，为解决 C10K 并发问题）。定位：静态资源服务、反向代理、负载均衡，是 Web 架构的流量入口标配。

## 二、核心知识
- **反向代理**：客户端请求先到 Nginx，由其转发到后端服务器；隐藏后端拓扑、统一入口（正向代理则是代理客户端上网）
- **负载均衡**：upstream 配置后端集群；策略：轮询（默认）、权重 weight、ip_hash（会话保持）、least_conn（最少连接）
- **静态资源服务**：直接返回 HTML/CSS/JS/图片，性能远高于应用服务器处理
- **配置文件**：nginx.conf 结构：events/http/server/location 层级；location 匹配规则（前缀/正则/精确）与优先级
- **常用指令**：listen、server_name、location、proxy_pass、root、alias、rewrite、try_files
- **HTTPS**：SSL 证书配置（listen 443 ssl）、HTTP 强制跳转 HTTPS
- **性能参数**：worker_processes（工作进程）、keepalive、gzip 压缩
- **限流**：limit_req（请求频率）、limit_conn（连接数）
- **日志**：access.log 访问日志、error.log 错误日志

## 三、作用与常用场景
- 反向代理 + 负载均衡（多实例应用分发流量）
- 静态资源与前端项目部署（Vue/React 打包产物）
- 网关层：HTTPS 终止、跨域处理、请求限流
- 解决单机 C10K 高并发

## 四、基于什么语言/底层原理
- **开发语言**：C 编写
- **高性能原理**：**事件驱动（epoll）+ 异步非阻塞**模型：一个 worker 进程同时处理数万连接（对比 Apache 传统模型每连接一线程）；master-worker 多进程架构

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 高并发性能极强，内存占用低 | 动态内容处理能力弱（需配合应用服务器） |
| 配置灵活，功能丰富（代理/限流/缓存） | 配置语法学习有门槛（location 匹配易错） |
| 稳定性高，久经生产验证 | 商业高级功能（Nginx Plus）收费 |
| 社区版免费开源 | 动态模块加载不如 OpenResty 方便 |

## 六、学习建议
路径：正向/反向代理概念 → 静态站点配置 → 反向代理与 location 匹配 → 负载均衡实验（起两个后端服务验证）→ HTTPS 配置；结合菜鸟教程 Nginx 教程与官方文档。

> 参考来源：菜鸟教程 runoob.com、Nginx 官方文档
