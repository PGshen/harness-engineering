# 把约定变成机器检查

判断标准：一条约定**能用正则、文件结构、依赖图或工具权限判断对错**，就不该只靠文字。文字留给需要判断力的事。

## 已有的检查（模板自带）

`templates/scripts/check_docs.py`（只用标准库，依赖没装好也能跑）：

| 检查 | 防的是什么 |
|---|---|
| 相对 markdown 链接存在（支持 URL 编码和以 `/` 开头的仓库根路径；跳过代码块、模板、git 忽略的文件） | 文档移动/改名后地图失效 |
| 计划必需章节 | 交接信息缺失 |
| `active/` 多于一份计划 → 警告 | 并行计划互相干扰 |
| ADR 文件名 `NNNN-标题.md`、编号唯一、必需章节 | 决定无法引用 |
| AGENTS.md 行数上限 | 入口膨胀成手册 |
| 技术债 TD 编号在未处理区唯一、且不与「已处理」撞号 | 编号歧义 |

章节名、行数上限、跳过目录都在脚本顶部常量里，换语言或改结构时改那里。

## 常用的机器化手段

| 约定 | 手段 |
|---|---|
| 模块分层 / 禁止反向依赖 | Python: import-linter（`forbidden`、`independence`、`layers` 契约）；JS/TS: dependency-cruiser、eslint-plugin-boundaries；Go/Java: 架构测试（go list、ArchUnit） |
| 某目录/仓库只读 | Claude Code `.claude/settings.json` 的 `permissions.deny`（`Edit(//abs/path/**)`、`Write(...)`）；Codex 用 sandbox 配置 |
| 提交前必须过检查 | `.githooks/pre-commit` 跑 `make check-fast`，`make setup` 里 `git config core.hooksPath .githooks` |
| 提交说明格式 | `commit-msg` hook 用正则检查 `<type>(<scope>): ...` |
| 冒烟测试不被宿主环境污染 | `env -i` + 白名单变量运行 |
| 运行时数据不进 git / 不被热重载监听 | `.gitignore` + 启动命令的 `--reload-dir src` |
| 某类文件必须满足格式（如 JSON schema、frontmatter） | 写成结构测试放进测试套件 |
| 文档和代码一致（如命令表） | 测试里解析 AGENTS.md 命令表，断言 Makefile 有对应目标 |

## 新增一条检查的流程

1. 发现同一条约定第二次被违反 → 在当前计划的「意外与发现」记一笔。
2. 写检查（先写一个会失败的用例证明它能抓到违规）。
3. 接入 `make check`。
4. 删掉或缩短 SOP/AGENTS.md 里对应的文字，改成一句"由 X 检查"。
5. 检查脚本本身也要有测试（例如 `scripts/tests/test_check_docs.py`；本 skill 仓库的 `tests/` 可作参考）。
