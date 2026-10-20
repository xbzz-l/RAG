# Angular

## 一、是什么
Angular 是 **Google 维护的前端框架**（2016 年发布的 Angular 2+，与 AngularJS 1.x 完全不同），定位：**企业级**单页应用框架。它是"全家桶"式框架，路由、表单、HTTP、依赖注入开箱即用。

## 二、核心知识
- **TypeScript 一等公民**：Angular 本身就是用 TS 写的，官方推荐 TS 开发
- **组件与模板**：装饰器 @Component 声明组件，模板支持指令（*ngIf/*ngFor/[property]绑定/(event)事件）
- **双向绑定**：[(ngModel)] 数据双向同步
- **依赖注入（DI）**：@Injectable 服务 + 构造函数注入，层级注入器管理实例
- **RxJS 响应式编程**：Observable 流式处理异步（HttpClient 返回 Observable）
- **路由**：@angular/router 支持懒加载、路由守卫、子路由
- **表单**：模板驱动表单（Template-driven）与响应式表单（Reactive Forms）两套体系
- **CLI**：Angular CLI（ng 命令）脚手架生成、构建、测试一体化
- **模块化**：NgModule 组织功能（Angular 15+ 支持 Standalone 组件免模块）

## 三、作用与常用场景
- 大型企业级后台管理系统（尤其外企、银行、政务类）
- 需要强规范、强约束的团队协作项目
- 单体框架需求：不想要 Vue/React 的"自由选型"，希望官方给出全套标准答案

## 四、基于什么语言/底层原理
- **开发语言**：TypeScript（必用）；**模板**：Angular 专用模板语法编译为 JS 指令
- **底层实现**：Zone.js 脏检查触发变更检测；编译器（AOT/JIT）把模板编译成 JS 代码；依赖注入框架在编译期生成注入器代码

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 全家桶方案统一，官方规范完备 | 学习曲线三框架中最陡（TS+RxJS+DI 三座大山） |
| 依赖注入、模块化适合大型团队 | 包体积大、首屏较重 |
| 类型安全 + 强约束，代码风格统一 | 国内岗位需求少于 Vue/React |
| 长期支持版本（LTS）稳定，升级有官方迁移工具 | 响应式编程 RxJS 心智成本高 |

## 六、学习建议
需先掌握 TypeScript 与 ES6；学习顺序：CLI 与项目结构 → 组件/模板 → 依赖注入 → 路由 → 表单 → RxJS → 实战一个后台项目。适合目标为外企/大型企业的开发者。

> 参考来源：菜鸟教程 runoob.com、Angular 官方文档
