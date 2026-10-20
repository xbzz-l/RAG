# Go（Golang）

## 一、是什么
Go 是 **Google 2009 年发布的静态类型、编译型语言**，由 Ken Thompson、Rob Pike 等设计。定位：云原生基础设施与高并发后端服务语言，兼顾开发效率与运行性能。

## 二、核心知识
- **语法**：包与导入、变量声明、结构体 struct、接口 interface（鸭子类型，隐式实现）、切片 slice、映射 map、defer 延迟执行
- **并发核心**：goroutine（轻量协程，栈可增长，数万并发无压力）+ channel（goroutine 间通信，CSP 模型）；select 多路复用；sync 包（Mutex/WaitGroup）
- **并发哲学**：不要通过共享内存来通信，而应通过通信来共享内存
- **错误处理**：error 返回值模式（无 try/catch 异常）；panic/recover 处理致命错误
- **指针**：有指针但无指针运算；值传递 vs 引用传递
- **工具链**：go mod 依赖管理、go fmt 统一格式、go test 测试、go build 编译
- **生态**：Web（Gin/Echo）、ORM（GORM）、微服务（go-micro/Kratos）、容器（Docker/K8s 本身用 Go 写）

## 三、作用与常用场景
- 高并发后端服务（API 网关、IM 通讯）
- 云原生基础设施（Docker/K8s/Prometheus 均为 Go）
- 中间件与工具链开发
- 微服务与分布式系统

## 四、基于什么语言/底层原理
- **编译型**：直接编译为机器码，单二进制部署（无运行时依赖）
- **并发原理**：GMP 调度模型（G goroutine、M 系统线程、P 处理器）实现协程调度；channel 基于环形队列 + 锁实现
- **垃圾回收**：并发三色标记清除，低停顿

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 并发模型简洁强大（goroutine+channel） | 错误处理样板代码繁琐 |
| 编译产物单文件，部署极简 | 泛型支持较晚（1.18+），生态成熟度弱于 Java |
| 性能接近 C/C++，远超解释型语言 | 语法简单但理念（CSP）需适应 |
| 云原生第一语言，岗位增长快 | GUI/前端领域几乎无用武之地 |

## 六、学习建议
前提：有任一语言编程基础。路径：语法基础 → slice/map/struct/interface → goroutine/channel 并发（重点）→ 标准库（net/http）→ Gin + GORM 写一个 CRUD 服务 → 进阶 GMP 调度原理（面试重点）。

> 参考来源：菜鸟教程 runoob.com、Go 官方文档
