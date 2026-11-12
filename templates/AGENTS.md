# AGENTS.md — {{PROJECT_NAME}}

本文件是给 AI 开发者（Claude Code、Codex）的**入口地图**：只说明去哪里找什么，细节在 `docs/` 里。
保持在 100 行左右（`scripts/check_docs.py` 限制 120 行）；新增内容优先写进对应文档，这里只加链接。

## 项目是什么

<一两句话：这个项目做什么、给谁用。>

- 模块地图与分层规则：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 术语表：[docs/glossary.md](docs/glossary.md)
- 架构设计（权威来源）：`docs/design/` 中已批准的设计文档

## 每次会话开始时

1. 读本文件。
2. 读 [docs/SOP.md](docs/SOP.md)，确认当前所处的 SOP 阶段和你的职责。
3. 打开 `docs/plans/active/` 中的计划，先读 **「进度」** 和 **「下一步」** 两节。
4. 读 [docs/plans/TODO.md](docs/plans/TODO.md)。`active/` 中没有计划时，从这里挑下一件事，和负责人确认后再开工。
5. 运行 `make check`，确认基线是绿的。基线不绿时先处理这个问题，或者按升级条件停下来问人。
6. 从计划的「下一步」继续；新发现的、不属于当前计划的事项记进 TODO。

## 常用命令

| 命令 | 作用 |
|---|---|
| `make setup` | 安装依赖，启用 git hooks |
| `make check` | **唯一的质量关口**：lint、类型检查、测试、分层契约、文档检查。合并前必须全部通过 |
| `make check-fast` | pre-commit 运行的快速子集 |

运行和自验证的方法见 [docs/runbooks/verification.md](docs/runbooks/verification.md)，环境搭建见 [docs/runbooks/dev-setup.md](docs/runbooks/dev-setup.md)。

## 文档索引

| 需要 | 去哪里 |
|---|---|
| 工作流程、关口、升级条件 | [docs/SOP.md](docs/SOP.md) |
| 当前任务和交接信息 | `docs/plans/active/` |
| 待办（还没写成计划的工作） | [docs/plans/TODO.md](docs/plans/TODO.md) |
| 过去为什么这么决定 | `docs/decisions/` |
| 外部 SDK 和库的已验证行为 | [docs/references/](docs/references/README.md) |
| 模块质量与已知缺口 | [docs/quality/QUALITY.md](docs/quality/QUALITY.md) |
| 技术债 | [docs/quality/tech-debt.md](docs/quality/tech-debt.md) |

## 红线（违反任何一条都要停下来问人）

- 不跳过或削弱 `make check`；不用 skip、xfail、`type: ignore`、`noqa` 等绕过失败，除非计划里写明了理由。
- 不引入计划之外的新依赖，不改变计划之外的公共接口。
- 不修改 `docs/design/` 中已批准的设计；发现设计有问题就走升级流程。
- <项目特有的红线：只读目录、不进 git 的数据、必须先问的操作……>

## 工作约定

- **语言**：面向用户的回复、文档、提交说明都用中文；代码标识符和注释用英文。
- **计划的写法**：计划只写结构和意图（目标、涉及的文件、接口、验收标准、验证命令），不写完整的实现代码。
- **测试先行**：每个任务先写失败的测试，再实现。
- **外部 SDK 的知识**：以 `docs/references/` 中已验证的内容为准；训练知识可能已经过时。遇到没有记录的行为，先查官方文档或实测，然后把结论补进 references，注明日期和来源。
- **记录**：计划执行中的决定、意外和发现随时写进计划；影响范围超出当前计划的决定写成 ADR。
- **提交**：每个任务至少一个 commit，说明格式为 `<type>(<scope>): <中文说明>`，例如 `feat(auth): 实现登录接口`。
