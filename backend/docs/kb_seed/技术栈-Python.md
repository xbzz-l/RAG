# Python

## 一、是什么
Python 是 **解释型、动态类型的高级编程语言**，由 Guido van Rossum 于 1991 年发布。设计哲学：代码可读性优先、语法简洁。定位：全场景通用语言，当前 AI/数据科学事实标准。

## 二、核心知识
- **基础语法**：缩进即代码块、动态类型、序列（列表/元组/字符串）、字典、集合
- **函数与模块**：def 定义、默认参数、*args/**kwargs、装饰器、lambda、包导入
- **面向对象**：class、继承、多态、魔术方法（__init__/__str__/__call__）、property
- **高级特性**：生成器与 yield、迭代器、上下文管理器 with、异常处理 try/except
- **标准库**：os/sys/json/datetime/re/collections/threading 等开箱即用
- **pip 与虚拟环境**：venv 隔离依赖，requirements.txt 声明依赖
- **热门方向库**：Web（Django/Flask/FastAPI）、爬虫（requests/Scrapy）、数据（NumPy/pandas）、AI（PyTorch/TensorFlow/scikit-learn）

## 三、作用与常用场景
- AI/机器学习/深度学习（行业第一语言）
- 数据分析与可视化（pandas + matplotlib）
- Web 后端（FastAPI 异步、Django 全家桶、Flask 轻量）
- 爬虫、自动化脚本、运维工具
- 量化交易、科学计算

## 四、基于什么语言/底层原理
- **官方实现 CPython**：解释器用 C 编写，将源码编译为字节码后在虚拟机上解释执行
- **内存管理**：引用计数为主 + 分代垃圾回收（GC）兜底；GIL 全局解释器锁限制多线程并行执行 Python 字节码

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 语法简洁，学习曲线最平缓的语言之一 | 解释执行，运行速度慢于 C/Java/Go |
| 生态覆盖 AI/数据/Web/自动化全领域 | GIL 导致 CPU 密集多线程受限（多进程/异步弥补） |
| 开发效率高、胶水语言 | 动态类型大项目维护性弱（类型注解弥补） |
| 社区庞大、文档与第三方库丰富 | 移动端/桌面端能力弱 |

## 六、学习建议
菜鸟教程 Python 教程打基础 → 标准库 → 面向对象与高级特性 → 选定方向（AI 学 NumPy/PyTorch；Web 学 FastAPI；数据学 pandas）→ 项目实战。

> 参考来源：菜鸟教程 runoob.com、Python 官方文档
