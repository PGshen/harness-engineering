---
name: harness-engineering
description: Use when starting a new repository that AI agents (Claude Code, Codex) will mainly develop, or when bringing an existing repository under AI-led development with docs-as-knowledge-base, plan handoff files and a single quality gate. 触发词：harness 工程、新建项目脚手架、已有项目接入 harness、AGENTS.md、SOP、计划交接、make check 质量关口、AI 主导开发流程。
---

# Harness 工程

## 概述

让 AI 在仓库里**长期、跨会话、少打扰人**地开发，靠的不是更好的提示词，而是仓库本身这套"挽具"：
一张短的入口地图 + 版本化的知识库 + 能接力的计划文件 + 唯一的机器质量关口 + 明确的人类关口与升级条件。

**核心原则**：会话会断，上下文会丢，所以一切关键信息必须落在仓库里；一切能机器检查的约定都要变成机器检查。

## 何时使用

- 新建一个主要由 AI 开发的项目 → 读 [references/greenfield.md](references/greenfield.md)
- 已有项目要改成 AI 主导、按 harness 方式开发 → 读 [references/retrofit.md](references/retrofit.md)
- 想知道每条做法为什么这样定、踩过什么坑 → 读 [references/principles.md](references/principles.md)
- 想把一条反复被违反的文字约定改成机器检查 → 读 [references/mechanization.md](references/mechanization.md)

**不适用**：一次性脚本、几天就扔的原型、多人走 GitHub PR + CI 且已有成熟流程的团队仓库（可以只借用其中的计划交接和 references 做法）。

## 七个支柱（速查）

| 支柱 | 落在哪里 | 机器怎么保证 |
|---|---|---|
| 入口地图，不是手册 | `AGENTS.md`（≤120 行）+ `CLAUDE.md` 只写 `@AGENTS.md` | `check_docs.py` 限行数 |
| 流程与关口 | `docs/SOP.md`：设计→计划→执行→自验证→评审→收尾；人只批准设计、批准计划、验收 | 计划的「批准记录」 |
| 计划即交接文件 | `docs/plans/active/<id>.md`，必需章节含「进度」「下一步」 | `check_docs.py` 查章节 |
| 唯一质量关口 | `make check`（lint/类型/测试/分层/文档）；pre-commit 跑 `check-fast` | git hook |
| 架构分层可执行 | `docs/ARCHITECTURE.md` + 依赖契约（import-linter、dependency-cruiser 等） | `make check` |
| 外部知识要验证 | `docs/references/`：✅/⚠️/❌ + 日期 + 来源 | 人工 + 评审 |
| 决定和债有出处 | `docs/decisions/NNNN-*.md`（ADR）、`quality/tech-debt.md`（TD-N）、`quality/QUALITY.md`、`plans/TODO.md` | `check_docs.py` 查编号与章节 |

## 落地

模板在 `templates/`（中文，按需改语言），用脚手架脚本复制到目标仓库——**从不覆盖已有文件**，已存在的会列出来让你手工合并：

```bash
SKILL_DIR=~/.claude/skills/harness-engineering   # 本 SKILL.md 所在目录，按实际安装位置改
python3 "$SKILL_DIR/scripts/scaffold.py" <目标仓库> --name <项目名> --dry-run
python3 "$SKILL_DIR/scripts/scaffold.py" <目标仓库> --name <项目名>
```

然后按 greenfield / retrofit 文档把 `Makefile` 的占位命令换成项目真实的检查命令（占位期间 `make check` 会打印警告，`make check STRICT=1` 会直接失败），`make setup && make check` 跑绿，写第一份 ADR 和第一份计划。

## 常见错误

| 错误 | 后果 | 正确做法 |
|---|---|---|
| 把细节都写进 AGENTS.md | 入口膨胀，每次会话都在读手册 | AGENTS.md 只放链接，细节进 `docs/` |
| 计划写完整实现代码 | 计划过时快、评审难 | 只写目标、文件、接口、验收标准、验证命令 |
| 「下一步」写成"继续做 X" | 新会话接不上 | 写成可直接执行的指令：文件、函数、哪些测试已写好还在失败 |
| 沉默或"先这样吧"当批准 | 越过人类关口 | 只有明确同意才算，且只对当时那份产出有效 |
| 文字约定被反复违反还继续加文字 | 约定持续失效 | 改成 lint/结构测试，并删掉对应文字 |
| 已有项目一次性改造所有东西 | 基线变红，没人能干活 | 先让 `make check` 包住现有检查并为绿，再逐步加规则 |
| 验收标准没证据就写"通过" | 虚假完成 | 写明命令和输出；验证不了就写"未验证"和原因 |
| 凭训练记忆写 SDK 用法 | 用到过时 API | 先查官方文档或实测，再写进 `references/` |

## 相关技能

规划和执行环节可配合 superpowers：brainstorming（设计）、writing-plans（计划）、subagent-driven-development / executing-plans（执行，执行方式由负责人按计划选择）、test-driven-development、verification-before-completion、requesting-code-review、finishing-a-development-branch。
