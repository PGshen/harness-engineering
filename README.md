# harness-engineering

一个给 Claude Code / Codex 用的 skill：把仓库搭成一套"挽具"，让 AI 能**长期、跨会话、少打扰人**地开发。

> A Claude Code / Codex skill that scaffolds a repository for AI-led development: a short `AGENTS.md` map, a versioned docs knowledge base, plan files that double as session handoffs, and a single `make check` quality gate. Templates are in Chinese.

## 它提供什么

- **入口地图**：`AGENTS.md`（≤120 行）+ 只有一行 `@AGENTS.md` 的 `CLAUDE.md`，Claude Code 和 Codex 读同一份。
- **流程与人类关口**：`docs/SOP.md`，设计 → 计划 → 执行 → 自验证 → 评审 → 收尾；人只批准设计、批准计划、验收。
- **计划即交接文件**：`docs/plans/active/<id>.md`，必需「进度」「下一步」等章节，新会话可以直接接着干。
- **唯一质量关口**：`make check`；pre-commit 跑 `make check-fast`。
- **知识库**：ADR、外部 SDK 的已验证知识（✅/⚠️/❌）、技术债、模块质量评级、runbooks。
- **机器检查**：`scripts/check_docs.py`（只用标准库）检查文档链接、计划/ADR 必需章节、ADR 编号、AGENTS.md 行数、技术债编号。

适用于新建项目，也适用于把已有项目接入（脚手架**从不覆盖已有文件**）。

## 安装

依赖：Python 3.9+、git、make、bash（Windows 请用 WSL 或 Git Bash）。

Claude Code：

```bash
git clone https://github.com/PGshen/harness-engineering.git ~/.claude/skills/harness-engineering
```

Codex 或其他支持 skills 的工具：clone 到对应的 skills 目录即可，使用时把文档里的 `SKILL_DIR` 换成实际路径。

## 使用

在 Claude Code 里直接说"用 harness 工程初始化这个仓库"或"把这个已有项目接入 harness"，skill 会被触发并按 [references/greenfield.md](references/greenfield.md) / [references/retrofit.md](references/retrofit.md) 引导。

也可以手动运行脚手架：

```bash
python3 ~/.claude/skills/harness-engineering/scripts/scaffold.py <目标仓库> --name <项目名> --dry-run
python3 ~/.claude/skills/harness-engineering/scripts/scaffold.py <目标仓库> --name <项目名>
cd <目标仓库> && make setup && make check
```

之后把 `Makefile` 里 `check-code` / `check-fast-code` 的占位换成项目真实的 lint/类型/测试命令。占位期间 `make check` 会打印警告；`make check STRICT=1` 会让占位直接失败，用来确认没有漏配。

## 目录

| 路径 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | skill 入口：七个支柱速查、常见错误 |
| [references/](references/) | 新建项目、已有项目接入、原则与理由、把约定机器化 |
| [templates/](templates/) | 复制到目标仓库的模板（中文） |
| [scripts/scaffold.py](scripts/scaffold.py) | 脚手架脚本 |
| [tests/](tests/) | 脚手架与 `check_docs.py` 的测试 |

## 可选配套

规划和执行环节可以配合 [superpowers](https://github.com/obra/superpowers) 的 brainstorming、writing-plans、test-driven-development 等技能，但不是必需的。

## 开发

```bash
python3 -m unittest discover -v tests
```

## License

[MIT](LICENSE)
