# Vite与Webpack（前端构建工具）

## 一、是什么
构建工具将**源码打包/转换为浏览器可运行产物**：处理模块化、编译 TS/JSX、压缩代码、注入环境变量等。**Webpack** 是上一代打包霸主（配置驱动），**Vite** 是新一代开发服务器+构建器（基于原生 ESM，秒级启动）。

## 二、核心知识
**Webpack**
- 入口 entry、输出 output、loader（转换：babel-loader/css-loader）、plugin（扩展：HtmlWebpackPlugin）
- 代码分割（Code Splitting）、Tree Shaking（摇树优化删除未用代码）
- devServer 开发服务器、热更新 HMR
- 配置繁琐：webpack.config.js 为核心学习点

**Vite**
- 开发模式：不打包，浏览器原生 ES Module 按需加载，冷启动秒开
- 依赖预构建：用 esbuild 预打包第三方依赖（速度是 Babel 数十倍）
- 生产构建：Rollup 打包
- 开箱即用：零配置支持 Vue/React/TS；vite.config.js 简洁
- 插件生态：@vitejs/plugin-vue 等
- 环境变量：.env 文件 VITE_ 前缀暴露给前端

**共性概念**
- 热更新 HMR：改代码浏览器即时生效不刷新
- 资源处理：图片/字体/样式导入
- Source Map：调试时映射回源码

## 三、作用与常用场景
- Vue/React 项目标配（官方脚手架均内置 Vite 或 Webpack）
- 性能优化：代码压缩、分包、按需加载
- 老项目兼容：Webpack 定制能力强，历史项目存量巨大

## 四、基于什么语言/底层原理
- **开发语言**：Node.js（JavaScript）
- **底层实现**：Webpack 基于 Node 做依赖图分析 + loader/plugin 转换管道；Vite 开发态利用浏览器原生 ESM，用 esbuild（Go 编写）做转译，生产态用 Rollup（JS）打包

## 五、优缺点
| 工具 | 优点 | 缺点 |
| --- | --- | --- |
| Vite | 启动快、配置简单、开发体验好 | 生态/兼容深度不如 Webpack（老插件） |
| Webpack | 生态最全、定制能力极强、存量项目多 | 配置复杂、冷启动慢、学习成本高 |

## 六、学习建议
日常开发优先学 Vite（新一代项目默认选择）；Webpack 至少懂 loader/plugin/常用配置（面试与老项目维护需要）。重点理解：为什么需要构建、HMR 原理、环境变量机制。

> 参考来源：菜鸟教程 runoob.com、Vite/Webpack 官方文档
