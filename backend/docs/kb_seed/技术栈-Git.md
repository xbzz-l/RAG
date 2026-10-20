# Git

## 一、是什么
Git 是 **分布式版本控制系统**（Linus Torvalds 2005 年开发）。定位：管理代码历史版本、支持多人协作开发，是软件行业必备基础工具。

## 二、核心知识
- **三个区域**：工作区（Working Directory）→ 暂存区（Staging/Index）→ 本地仓库（Repository）；`git add` 工作区→暂存区，`git commit` 暂存区→仓库
- **对象模型**：commit（提交快照）/tree（目录）/blob（文件）以 SHA-1 哈希寻址，内容寻址
- **分支**：指针而非拷贝，创建/切换极快；git branch / git checkout / git switch；合并 merge（三方合并）与 rebase（变基线性化）
- **远程协作**：remote 远程仓库（GitHub/Gitee/GitLab）、clone/pull/push/fetch；origin 约定名
- **冲突解决**：同位置不同修改合并时产生冲突，人工裁决后 add + commit
- **撤销与回退**：checkout -- file（丢弃工作区）、reset（移动 HEAD，--soft/--mixed/--hard）、revert（生成反向提交，安全回退）、stash（暂存改动）
- **常用工作流**：Git Flow（main/develop/feature/release/hotfix 多分支）、GitHub Flow（main + feature 分支 + PR）
- **提交规范**：Conventional Commits（feat/fix/docs/style/refactor/test/chore + 简述）
- **常用命令**：status/log/diff/blame/tag

## 三、作用与常用场景
- 代码历史管理与回溯
- 多人并行开发（分支隔离互不干扰）
- 代码托管平台协作（Pull Request 评审、Issue 跟踪）
- CI/CD 触发源（push 自动构建部署）

## 四、基于什么语言/底层原理
- **开发语言**：C 编写（部分 Shell）；快照模型：每次提交保存全部文件快照（未变文件存引用）；分布式：每个克隆都是完整仓库，无单点依赖

## 五、优缺点
| 优点 | 缺点 |
| --- | --- |
| 分布式，离线可提交、无单点故障 | 命令繁多，初学者易混乱 |
| 分支操作轻量快速 | 概念抽象（暂存区/HEAD 等需理解） |
| 历史完整、可追溯、可恢复 | 大文件/二进制管理能力弱（需 LFS） |
| 生态：GitHub 等平台繁荣 | 复杂历史操作（rebase 等）易出错 |

## 六、学习建议
先理解三个区域与快照模型（不理解原理只会死记命令）→ 熟练 20 个高频命令 → 学会解决冲突 → 掌握一个分支工作流 → 用 GitHub 托管自己的项目并练习 PR 流程。

> 参考来源：菜鸟教程 runoob.com、Git 官方文档（Pro Git）
