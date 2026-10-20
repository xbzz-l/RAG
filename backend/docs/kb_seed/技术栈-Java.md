# Java

## 一、是什么
Java 是 **Sun 公司（现 Oracle）1995 年发布的静态类型、面向对象编程语言**，口号"一次编写，到处运行"。定位：企业级后端开发第一语言，运行于 JVM（Java 虚拟机）之上。

## 二、核心知识
- **语法基础**：强类型、类与对象、封装继承多态、接口、抽象类、异常体系（受检/非受检）
- **集合框架**：List（ArrayList/LinkedList）、Set（HashSet/TreeSet）、Map（HashMap/TreeMap）、HashMap 底层（数组+链表+红黑树）
- **泛型**：编译期类型检查与类型擦除
- **并发编程**：Thread/Runnable、线程池 ThreadPoolExecutor、synchronized、volatile、Lock、JUC 并发包、CAS 与 AQS
- **JVM 核心**：内存区域（堆/栈/方法区）、垃圾回收（GC 算法与 G1/ZGC 收集器）、类加载机制（双亲委派）、字节码
- **IO 与网络**：BIO/NIO/AIO、Netty 网络框架
- **JDK 8 特性**：Stream 流、Lambda、Optional、新日期 API
- **生态**：Spring 全家桶、Maven/Gradle 构建、JUnit 测试

## 三、作用与常用场景
- 企业级后端服务（金融、电商、政务系统首选）
- Android 开发（Kotlin 之前的主语言）
- 大数据生态（Hadoop/Spark/Flink 均基于 JVM）
- 微服务架构（Spring Cloud / Dubbo）

## 四、基于什么语言/底层原理
- **编译模型**：.java 源码 → javac 编译为字节码 .class → JVM 解释执行 + JIT 即时编译为机器码
- **跨平台原理**：JVM 屏蔽操作系统差异，字节码在任何平台的 JVM 上运行
- **内存管理**：JVM 自动垃圾回收，开发者无需手动释放内存

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 生态成熟庞大，企业岗位需求巨大 | 语法冗长（样板代码多） |
| 性能优秀（JIT 编译接近 C++） | 内存占用高，启动慢（不适宜 Serverless 短任务） |
| 强类型 + 编译检查，大型项目可靠 | 学习曲线长（语言+JVM+框架三层面） |
| 跨平台、稳定，20+ 年企业验证 | 版本碎片化（大量项目仍停留在 JDK 8） |

## 六、学习建议
路线：Java 基础（含集合/IO）→ 面向对象与泛型 → JVM 与并发（面试重点）→ MySQL → Spring/Spring Boot → 微服务 → 项目实战。菜鸟教程 Java 系列覆盖基础，JVM 与并发建议配合《深入理解 Java 虚拟机》等书籍。

> 参考来源：菜鸟教程 runoob.com、Oracle Java 官方文档
