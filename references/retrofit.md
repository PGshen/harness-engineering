# 已有项目：接入 harness

原则：**先包住现状并保持绿，再逐步收紧**。改造本身也走计划 + 人批准，不要在一个 commit 里重写一切。

## 1. 盘点（只读，不改任何文件）

列一张清单给负责人看：

| 项 | 要找什么 |
|---|---|
| 已有 AI 入口 | `AGENTS.md`、`CLAUDE.md`、`.cursorrules`、`.github/copilot-instructions.md` 等 |
| 检查命令 | lint、格式、类型、测试、构建；CI 配置里实际跑的命令；当前是否全绿 |
| 文档 | README、docs/、wiki 链接、设计稿、ADR |
| 模块结构 | 顶层目录、主要包、实际依赖方向（有没有明显的反向依赖） |
| 待办与债 | issue、`TODO`/`FIXME`/`HACK` 注释（`grep -rn`）、已知 bug |
| 外部依赖 | 关键 SDK 及版本、团队踩过的坑 |
| 红线 | 不能碰的目录、生成代码、共享配置、生产数据 |

## 2. 写接入计划并请负责人批准

用 `docs/plans/TEMPLATE.md` 写 `harness-adoption` 计划，任务大致是下面第 3–7 步。范围里写清**不包含**：不改业务代码、不修现有失败测试（登记成 TD）。

## 3. 铺模板（不覆盖）

```bash
SKILL_DIR=~/.claude/skills/harness-engineering   # 本 skill 所在目录，按实际安装位置改
python3 "$SKILL_DIR/scripts/scaffold.py" <repo> --name <项目名> --dry-run
python3 "$SKILL_DIR/scripts/scaffold.py" <repo> --name <项目名>
```

脚本列出的"已存在、跳过"的文件要手工合并：
- **已有 AGENTS.md/CLAUDE.md**：保留原有有效内容，按地图结构重排；细节移到 `docs/`，留链接。`CLAUDE.md` 改成 `@AGENTS.md`（原内容并入 AGENTS.md 或 docs/）。
- **已有 Makefile**：只追加 `check`/`check-fast`/`check-docs`/`setup` 目标，不改原有目标。非 make 项目也可以用 `package.json` scripts、`justfile`、`taskfile`，关键是**一个**命令名。
- **已有 docs/**：模板目录并存；旧文档按类型归入 design/references/runbooks，或在 AGENTS.md 索引里链接原位置。

## 4. 让 `make check` 包住现状并为绿

- `check` 先只调用项目**已有**的检查命令 + `check_docs.py`。
- 现有检查本来就红：不要用 skip 掩盖。和负责人确认后二选一：先修到绿（单独的计划），或把失败项明确排除并登记 TD，写清恢复条件。
- 已有 CI：让 CI 调 `make check`，保证本地和 CI 同一个关口。
- `check_docs.py` 一开始报大量死链时，修链接或把旧文档目录加进 `SKIP_DIRS`（并登记 TD 逐步清理）。被 `.gitignore` 忽略的文件本来就不检查。

## 5. 从代码反推知识库

- `docs/ARCHITECTURE.md`：按**实际**代码写模块表与依赖方向，不写理想状态。理想与现实的差距登记成 TD。
- 依赖契约：只加今天就成立的规则（例如"core 不依赖 api"），让工具保护现状不再恶化；违反中的规则先登记 TD。
- `docs/references/`：把团队口口相传的 SDK 坑写下来，没验证过的标 ⚠️。
- `docs/quality/QUALITY.md`：每个模块给初始评级，诚实写缺口。
- `docs/quality/tech-debt.md`：从 FIXME/HACK、失败测试、盘点中发现的问题建立初始登记表。
- `docs/plans/TODO.md`：把 issue/待办里要排期的条目搬进来，优先级让负责人定。
- `docs/decisions/`：`0001` 采用 harness 流程；已有的重大技术选择补写简短 ADR（背景可以写"追溯记录"）。

## 6. 启用 hook，提交基线

`make setup && make check` 全绿 → `chore(harness): 接入 harness 工程` → 按计划收尾清单验收、合并。

## 7. 之后的节奏

- 新功能一律按 SOP：设计（需要时）→ 计划 → 执行 → 自验证 → 评审 → 收尾。
- 每个里程碑收尾时：从 TD 挑一两项处理；检查是否有文字约定该机器化；按实际补依赖契约。
- 旧代码不必一次性达标：碰到哪里，就让哪里符合规则（童子军原则），并更新 QUALITY.md。

## 常见陷阱

- 一上来就加严格 lint 规则 → 几百个错误，基线红，所有人停工。先保护现状，再逐模块收紧。
- 把旧的长篇 CLAUDE.md 原样塞进 AGENTS.md → 超过行数上限，失去地图作用。
- ARCHITECTURE.md 写成理想架构 → 和代码不一致，AI 按错误地图改代码。
