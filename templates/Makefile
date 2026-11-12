# make check 是唯一的质量关口（docs/SOP.md）。
# 把 check-code / check-fast-code 里的占位换成项目真实的命令，并删掉占位的警告行。
# 占位期间 make check 只打印警告；用 `make check STRICT=1` 可以让占位直接失败，确认没有漏配。

SHELL := /bin/bash
PYTHON ?= python3
STRICT ?= 0

# AI 工具的沙箱里 PATH 可能不完整，需要时在这里主动定位工具，例如：
# UV   ?= $(shell command -v uv 2>/dev/null || echo $(HOME)/.local/bin/uv)
# PNPM ?= $(shell command -v pnpm 2>/dev/null || ls -d $(HOME)/.nvm/versions/node/*/bin/pnpm 2>/dev/null | tail -1)

# 子项目目录还不存在时跳过对应检查，让骨架阶段也能保持绿，例如：
# HAS_BACKEND  := $(wildcard backend/pyproject.toml)
# HAS_FRONTEND := $(wildcard frontend/package.json)
#
# check-code:
# ifneq ($(HAS_BACKEND),)
# 	cd backend && $(UV) run ruff check . && $(UV) run pytest
# endif
# ifneq ($(HAS_FRONTEND),)
# 	cd frontend && $(PNPM) run lint && $(PNPM) exec vitest run
# endif

.PHONY: setup check check-fast check-docs check-code check-fast-code

setup:
	git config core.hooksPath .githooks
	@# 在这里加安装依赖的命令，例如：cd backend && $(UV) sync

check: check-docs check-code
	@echo "make check 全部通过"

# pre-commit 运行的快速子集：文档检查 + lint。
check-fast: check-docs check-fast-code

check-docs:
	@$(PYTHON) scripts/check_docs.py

check-code:
	@# 按顺序填入：lint、格式检查、类型检查、分层契约、测试。例如：
	@#   cd backend && $(UV) run ruff check . && $(UV) run ruff format --check .
	@#   cd backend && $(UV) run pyright && $(UV) run lint-imports && $(UV) run pytest
	@#   cd frontend && $(PNPM) run lint && $(PNPM) run typecheck && $(PNPM) exec vitest run
	@echo "警告：check-code 尚未配置项目检查命令，代码没有经过任何检查（见 Makefile）" >&2; test "$(STRICT)" != 1

check-fast-code:
	@echo "警告：check-fast-code 尚未配置 lint 命令（见 Makefile）" >&2; test "$(STRICT)" != 1
