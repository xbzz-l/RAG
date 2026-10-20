# Node.js

## 一、是什么
Node.js 是 **JavaScript 的服务器端运行环境**，基于 Chrome V8 引擎，由 Ryan Dahl 于 2009 年创建。它让 JS 脱离浏览器运行，实现"一门前端语言通吃前后端"。

## 二、核心知识
- **事件循环与异步 I/O**：单线程 + libuv 线程池，非阻塞 I/O 模型，适合高并发 I/O 密集场景
- **模块系统**：CommonJS（require/module.exports）与 ES Module（import/export）
- **npm 包管理**：package.json 依赖声明、node_modules、npm install/update；语义化版本
- **核心模块**：fs（文件）、http（HTTP服务器）、path（路径）、stream（流）、events（事件）、crypto（加密）
- **框架**：Express（老牌轻量）、Koa（洋葱模型中间件）、NestJS（企业级，TS+装饰器）
- **中间件机制**：请求依次经过中间件链处理（Express 核心思想）
- **数据库交互**：mysql2/pg/mongoose 等驱动连接关系型/文档型数据库
- **进程管理**：cluster 多进程、PM2 守护与负载均衡

## 三、作用与常用场景
- Web 后端 API 服务（RESTful 接口）
- 前端工程化工具链：Webpack/Vite 等构建工具本身基于 Node
- 实时应用：聊天室、协作工具（WebSocket 支持好）
- 微服务/BFF（面向前端的后端层）
- CLI 工具、脚本自动化

## 四、基于什么语言/底层原理
- **开发语言**：JavaScript（可配合 TypeScript）
- **底层实现**：V8 引擎编译执行 JS；libuv 提供跨平台事件循环与线程池；单线程执行 JS 逻辑，耗时 I/O 交给系统异步回调

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 前后端同语言，全栈学习成本低 | 单线程，CPU 密集型任务会阻塞主线程 |
| 高并发 I/O 场景性能优秀 | 动态类型，大型后端项目约束弱于 Java/Go |
| 生态庞大（npm），工具链成熟 | 回调历史包袱（回调地狱，已由 async 缓解） |
| 启动快、轻量，适合微服务 | 部分 npm 包质量参差不齐、供应链安全风险 |

## 六、学习建议
前提：JavaScript 基础扎实。路径：Node 模块与事件循环 → http/fs 核心模块 → Express 写 REST API → 连接 MySQL/Redis → 部署（PM2）。用 Express 写一个带鉴权的 CRUD 接口项目即可入门。

> 参考来源：菜鸟教程 runoob.com、Node.js 官方文档
