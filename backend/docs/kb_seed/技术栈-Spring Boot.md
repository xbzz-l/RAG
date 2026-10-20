# Spring Boot

## 一、是什么
Spring Boot 是 **Java 企业级微服务快速开发框架**，基于 Spring 框架构建，2014 年发布。核心价值：约定优于配置，自动装配 + 内嵌服务器，让 Spring 项目"开箱即用"。

## 二、核心知识
- **自动装配**：@SpringBootApplication（含 @Configuration/@EnableAutoConfiguration/@ComponentScan）按依赖自动配置组件
- **starter 依赖**：spring-boot-starter-web/mybatis/redis 等，一键引入整套依赖
- **内嵌容器**：默认内嵌 Tomcat，java -jar 直接运行，无需外部部署
- **配置体系**：application.yml/properties、多环境 profile、@Value/@ConfigurationProperties 绑定、配置优先级
- **IoC 与 DI**：Bean 生命周期、@Component/@Service/@Repository、@Autowired 注入、@Bean/@Configuration
- **AOP 切面**：@Aspect 切面做日志、事务、权限拦截
- **Web 开发**：@RestController/@RequestMapping、参数校验（@Valid + Validation）、全局异常处理（@ControllerAdvice）、拦截器与过滤器
- **数据访问**：Spring Data JPA（ORM）、MyBatis-Plus（SQL 为主）；声明式事务 @Transactional
- **生态集成**：Redis 缓存（Spring Cache）、消息队列、定时任务 @Scheduled、接口文档 Swagger/Knife4j
- **微服务**：Spring Cloud（注册中心/网关/配置中心/熔断）

## 三、作用与常用场景
- 企业级后端 API 服务（国内 Java 岗位绝对主流）
- 微服务架构的基石
- 快速原型与单体应用（开发效率较传统 Spring 大幅提升）
- 与大数据/中间件（Redis/Kafka/ES）集成场景

## 四、基于什么语言/底层原理
- **开发语言**：Java
- **底层实现**：基于 Spring 核心容器（IoC/DI）与自动配置条件注解 @Conditional；启动时扫描依赖并按条件装配 Bean；内嵌 Tomcat 由 SpringApplication.run 启动

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 开发效率高：约定优于配置，快速起步 | 版本兼容矩阵复杂（Boot/Cloud/Java 版本对应关系） |
| 生态完整，中间件集成官方支持 | 黑盒自动装配，排查底层问题门槛高 |
| 内嵌容器，部署简单 | JVM 内存占用较高 |
| 社区活跃、国内资料与岗位极多 | 对新手隐藏了 Spring 底层细节 |

## 六、学习建议
前提：Java 基础 + Spring 核心（IoC/AOP）概念。路径：starter 与配置 → Web 开发 → 数据访问（JPA 或 MyBatis-Plus）→ 异常处理与校验 → 集成 Redis → 项目实战（前后端分离的后台项目）。

> 参考来源：菜鸟教程 runoob.com、Spring 官方文档
