# HTML与CSS

## 一、是什么
HTML（超文本标记语言）定义网页**结构与内容**，CSS（层叠样式表）定义网页**外观与布局**。两者是前端开发的根基：HTML5 与 CSS3 是现行标准。

## 二、核心知识
**HTML**
- 语义化标签：header/nav/main/article/section/footer 替代无语义 div
- 常用元素：标题 h1-h6、段落 p、链接 a、图片 img、列表 ul/ol、表格 table、表单 form/input/select
- 属性：class/id/data-* 自定义属性、alt 无障碍
- HTML5 新增：canvas（绘图）、video/audio（媒体）、localStorage（本地存储）、WebSocket

**CSS**
- 选择器：标签/类/ID/后代/子代/兄弟/属性/伪类（:hover/:nth-child）/伪元素（::before）
- 盒模型：content+padding+border+margin；box-sizing: border-box 统一计算
- 布局：文档流 → 浮动 float → 定位 position（relative/absolute/fixed/sticky）→ **Flexbox**（一维布局）→ **Grid**（二维布局）
- 层叠与优先级：!important > 内联 > ID > 类 > 标签；z-index 控制层级
- 响应式：媒体查询 @media、rem/vw 弹性单位、移动优先
- CSS3：过渡 transition、动画 animation、变形 transform、渐变

## 三、作用与常用场景
- 一切网页与 Web 应用的界面基础
- 静态页面/官网/落地页直接由 HTML+CSS 构成
- 前端框架（Vue/React）的组件模板与样式同样基于 HTML/CSS
- 邮件模板、小程序 WXML/WXSS 语法同源

## 四、基于什么语言/底层原理
- **本身即标记语言与样式语言**：浏览器 HTML 解析器构建 DOM 树，CSS 解析器构建 CSSOM，两者合成渲染树，经布局（Layout）与绘制（Paint）上屏
- **重排（reflow）与重绘（repaint）**：几何属性变化触发重排（代价高），仅颜色等变化只重绘

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 上手极快，所见即所得 | 本身无逻辑能力，交互需 JS |
| 浏览器原生支持，无任何依赖 | CSS 全局作用域易冲突（BEM/模块化缓解） |
| 学习门槛低、资料海量 | 浏览器兼容性差异需处理 |
| 布局体系（Flex/Grid）现代且强大 | 只掌握 HTML/CSS 就业面窄（需配合 JS） |

## 六、学习建议
用菜鸟教程 HTML/CSS 教程打底，重点练：盒模型、Flex/Grid 布局、响应式三件套；建议以"仿写一个静态页面"作为结业作业（如仿写菜鸟教程首页布局）。

> 参考来源：菜鸟教程 runoob.com、MDN Web Docs
