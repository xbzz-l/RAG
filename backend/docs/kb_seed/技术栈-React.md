# React

## 一、是什么
React 是 **Meta（Facebook）开源的前端 JavaScript 库**，用于构建用户界面，发布于 2013 年。核心思想：UI 是状态的函数（UI = f(state)），组件化 + 单向数据流。

## 二、核心知识
- **JSX**：JavaScript 语法扩展，在 JS 中直接写类 HTML 结构，编译为 React.createElement 调用
- **组件**：函数组件 + Hooks 是当前主流；类组件为历史写法
- **Hooks**：useState（状态）、useEffect（副作用）、useRef、useMemo、useCallback、自定义 Hook 复用逻辑
- **单向数据流**：父组件通过 props 向下传递，状态变更只能通过 setState 触发，数据流向可预测
- **虚拟 DOM 与 Fiber**：Fiber 架构可中断、可优先级的渲染调度，支撑 Concurrent 并发渲染
- **不可变数据**：状态更新必须返回新对象/数组，配合浅比较优化性能
- **生态**：React Router（路由）、Redux/Zustand（状态管理）、Next.js（SSR/全栈框架）、Ant Design（UI库）

## 三、作用与常用场景
- 中大型单页应用、复杂交互后台、数据密集型界面
- 搭配 Next.js 做服务端渲染/静态站点（SEO 友好）
- React Native 跨端移动开发（同一套组件思想写原生 App）
- 海外市场岗位占比最高的前端技术

## 四、基于什么语言/底层原理
- **开发语言**：JavaScript（现代项目普遍配合 TypeScript）
- **底层实现**：JSX 编译产物 → React 元素树 → Fiber 链表结构 → 协调（Reconciliation）diff 算法 → 提交阶段批量更新真实 DOM；Hooks 基于 Fiber 节点上的链表存储状态

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 生态最大、社区最活跃、岗位需求多 | 学习曲线陡：JSX + Hooks 心智模型需适应 |
| 组件化与函数式编程思想先进 | 只负责视图层，路由/状态管理需自行选型 |
| 性能强：Fiber 并发渲染、虚拟DOM diff 优化 | 技术更新快，旧写法（类组件）资料易过时 |
| 跨端能力（React Native） | 项目配置自由度大，规范依赖团队约定 |

## 六、学习建议
先补 JavaScript 与 ES6 基础，再学 JSX → 组件与 props → Hooks（重点 useState/useEffect）→ 状态管理与路由 → 实战项目（如 Todo 进阶、后台管理系统）。

> 参考来源：菜鸟教程 runoob.com、React 官方文档
