# TypeScript

## 一、是什么
TypeScript（简称 TS）是 **微软开发的 JavaScript 超集**，在 JS 基础上增加静态类型系统，编译后输出纯 JavaScript。定位：用类型约束解决 JS 大型项目可维护性问题。

## 二、核心知识
- **类型注解**：string/number/boolean/数组/元组/枚举/any/unknown/never/void
- **interface 与 type**：描述对象结构；interface 可继承/合并，type 可写联合/交叉类型
- **联合类型与字面量类型**：`string | number` 联合，`'success' | 'error'` 字面量收窄
- **泛型**：`<T>` 参数化类型，写可复用的函数/组件类型（如 Promise<T>、Array<T>）
- **类型推断**：大部分场景自动推导，减少显式注解
- **类型守卫与收窄**：typeof/instanceof/in 操作符、类型谓词 is
- **类与访问修饰符**：public/private/protected/readonly、抽象类、装饰器（实验性）
- **模块与命名空间**：ES Module 为主
- **tsconfig.json**：strict 严格模式、target、module 等编译配置
- **工具类型**：Partial/Required/Pick/Omit/Record/ReturnType 等内置类型体操

## 三、作用与常用场景
- 中大型前端项目（Vue 3 + TS、React + TS 是行业标配）
- 前后端共享类型定义（接口契约，Node 后端同样可用）
- 框架与库开发（源码级类型提示）
- 重构与协作：类型即文档，编译期发现错误

## 四、基于什么语言/底层原理
- **开发语言**：TS 本身；**编译目标**：JavaScript（tsc 编译器做类型擦除转译，类型信息不进入运行时）
- **底层原理**：结构化类型系统（鸭子类型）——形状匹配即兼容；编译期做类型检查，运行时无额外开销

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 编译期捕获错误，减少低级 bug | 需要写类型，初学速度慢于 JS |
| 类型即文档，IDE 提示/重构能力飞跃 | 引入类型体操复杂度（高级类型难读） |
| 与 JS 完全兼容，可渐进迁移 | 编译配置与第三方类型声明（@types）偶有坑 |
| 大型项目可维护性显著提升 | 对小型脚本项目属于额外负担 |

## 六、学习建议
前提是掌握 JavaScript；学习路径：类型基础 → interface/type → 泛型 → 工具类型 → tsconfig 工程配置；用 TS 重写一个小项目比刷教程更有效。

> 参考来源：菜鸟教程 runoob.com、TypeScript 官方文档
