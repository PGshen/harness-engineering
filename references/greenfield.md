# 新建项目：从零搭 harness

目标：第一个功能 commit 之前，仓库已经有地图、流程、关口，并且 `make check` 为绿。

## 步骤

1. **和负责人确认四件事**（不清楚就问，别猜）：
   - 文档与提交说明用什么语言（模板默认中文，代码标识符和注释英文）。
   - 技术栈与各自的 lint/类型/测试命令。
   - 只用本地关口，还是也有远程 CI（有 CI 就让 CI 调 `make check`）。
   - 红线：哪些目录/仓库只读、哪些数据不进 git、哪些操作必须先问。
2. **初始化仓库并铺模板**：
   ```bash
   git init <repo> && cd <repo>
   python3 <本 skill 目录>/scripts/scaffold.py . --name <项目名>   # 默认安装位置是 ~/.claude/skills/harness-engineering
   ```
3. **改 Makefile**：在 `check-*` 目标里填上真实命令，并删掉占位的警告行；按 Makefile 开头的示例用 `$(wildcard ...)` 让还不存在的子目录自动跳过，这样骨架阶段就能绿。工具路径主动定位（沙箱 PATH 可能不全）。填完后用 `make check STRICT=1` 确认没有遗漏的占位。
4. **填 AGENTS.md**：项目一句话、红线、常用命令表。保持 ≤120 行。
5. **写架构设计**：用 brainstorming 和负责人讨论，产出 `docs/design/<日期>-architecture.md`，**人批准**。从中整理出 `docs/ARCHITECTURE.md` 的模块表与依赖方向，以及里程碑列表（写进设计文档或 TODO）。
6. **写首批 ADR**：`0001` 采用本流程（模板已给）；技术栈、存储、部署方式等关键选择各一份。
7. **配依赖契约工具**（Python: import-linter；JS/TS: dependency-cruiser 或 eslint-plugin-boundaries；Go: 用 `go list` 写结构测试；其他语言写一个结构测试），先放一两条今天就成立的契约，模块出现时再补。
8. **启用 hook 并跑基线**：`make setup && make check`，必须全绿后提交：`chore(harness): 初始化 harness 工程骨架`。
9. **外部依赖先做 spike**：设计里依赖的关键 SDK/服务，先实测关键行为，写进 `docs/references/`（✅/⚠️/❌ + 日期 + 来源）。设计中的风险项也在这里验证。
10. **写第一份计划**（M1 骨架）：复制 `docs/plans/TEMPLATE.md` 到 `docs/plans/active/m1-<slug>.md`，**人批准**后开分支执行。

## 完成标准

- [ ] `make check` 为绿，pre-commit 生效（`git config core.hooksPath` 为 `.githooks`）
- [ ] AGENTS.md 中的每个链接都存在（`check_docs.py` 会查）
- [ ] 至少一份 ADR；架构设计已批准
- [ ] `plans/active/` 有一份已批准的计划，或 TODO 里写着下一件事
