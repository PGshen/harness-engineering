# 开发环境搭建

## 前置依赖

| 依赖 | 用途 | 安装 |
|---|---|---|
| <工具> | <用途> | <安装命令> |

## 命令行路径

AI 工具的沙箱中 `PATH` 可能不完整。Makefile 自己定位关键工具（见 `Makefile` 开头），不依赖调用方的 `PATH`。

## 初始化

```bash
make setup
```

安装依赖，并执行 `git config core.hooksPath .githooks`，启用 pre-commit（跑 `make check-fast`）。

## 环境变量与密钥

<列出需要的变量；密钥放在不进 git 的 `.env`，提供 `.env.example`。>
