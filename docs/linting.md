# Linting

在本章中，我们将探讨如何为你的项目集成代码检查、代码格式化和使用静态分析工具。

## 使用 Ruff 进行代码检查

代码检查器（Linter）会分析源代码，以标记潜在的编程错误、代码异味、风格问题和可疑的构造。

在 Python 生态中，最常见的检查器包括 [Pylint](https://pylint.pycqa.org/en/latest/)，以及像 [Flake8](https://flake8.pycqa.org/en/latest/)、[pylama](https://github.com/klen/pylama) 和 [prospector](https://prospector.landscape.io/en/master/) 这样的工具。

此外，[Ruff](https://docs.astral.sh/ruff/) 作为一个新兴的高性能工具，正迅速普及。Ruff 是一个用 Rust 编写的、速度极快的 Python linter 和代码格式化工具。它的设计目标是作为 Flake8、isort、Black 等多种工具的替代品，并提供显著的性能提升。值得一提的是，Ruff 和本项目使用的包管理工具 uv 都是由 Astral 公司开发的，它们都旨在为 Python 开发提供一个用 Rust 构建的高性能工具链。

除了这些，还有一些多语言的代码检查框架，例如 [pre-commit](https://pre-commit.com/) 和 [coala](https://coala.io/)。

在本章中，我们将介绍如何使用 Ruff 和 pre-commit 来提升代码质量。
下载Ruff
```bash
$ uv add ruff --dev
```
在代码库上添加一个Nox session，以运行Ruff：
```python
# noxfile.py
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.11", "3.12"])
def lint(session):
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff","check", *args)
```
`locations`设置了lint运行的路径。由于设置了`session.posargs`，这将允许在命令行中传递额外的参数。`session.install`方法通过`pip`将`Ruff`安装到虚拟环境中。

如果使用VSCode，最好安装插件`Ruff`和`Error Lens`，
和配置用户设置
```json
//settings.json
{"editor.defaultFormatter": "charliermarsh.ruff",
"editor.formatOnSave": true,
"editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"}
}
```
这样会显著增强代码格式化的体验。

在`ruff`中，我们可以显式要求`ruff`需要检查什么，比如
- F 会解析源文件并查找无效的Python代码。
- W 和 E是警告和错误，其会检查你的Python代码是否符合PEP 8中的一些样式约定。
- C会检查你的Python包的代码复杂度是否超过了配置的限制。

其中，代码复杂度一般与以下有关：
- 分支结构：包含的条件判断（如 if、elif、switch）、循环（for、while）、异常处理（try/except）等控制流语句的数量和嵌套深度。
- 路径数量：程序执行过程中可能的不同路径数量，路径越多，理解和测试难度越大。
- 嵌套深度：代码块（如循环内的循环、条件内的条件）的嵌套层次，过深的嵌套会显著增加复杂度

在配置文件`pyproject.toml`中，可以添加以下，以启用其内置违规类并设置复杂度限制：
```toml
# pyproject.toml
[tool.ruff.lint]
select = ["C","E","F","W","C901"]
```
默认情况下，Nox会运行在noxfile.py中定义的所有session。使用--session(-s)选项来限制它只运行特定的session：
```bash
$ uv run nox -rs lint
```

### 使用 Ruff 进行代码格式化
在`noxfile.py`添加以下session：
```python
# noxfile.py
@nox.session(python="3.11")
def format(session):
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff","check",*args,"--fix")
```
在Nox session设置好之后，可以像这样重新格式化代码：
```bash
$ uv run nox -rs format
```
% missing from source
不提供参数调用 nox 会触发所有session，包括 format。最好只验证代码风格而不修改冲突的文件。通过在顶部设置 nox.options.sessions 来默认排除 format session：
```python
# noxfile.py
nox.options.sessions = "lint", "tests"
```
### 使用 Ruff 检查 `import` 顺序
Ruff可以检查import语句是否符合[`PEP-8`](https://www.python.org/dev/peps/pep-0008/#imports)规范的方式分组和排序。导入应分为三个组，如下所示：
```python
# 标准库
import time

# 第三方库
import click

# 本地库
from modern_python import wikipedia
```
启用Ruff导入检查（`I` 为 `import`）：
```toml
# pyproject.toml
[tool.ruff.lint]
select = ["C","E","F","W","I","C901"]
```
Ruff 会自动识别哪个是本地库。

### 使用Ruff 发现更多 bug
ruff 可以帮助你在程序中找到各种错误和设计问题。

在配置文件中启用插件警告（B代表bugbear）：
```toml
# pyproject.toml
[tool.ruff.lint]
select =  ["C","E","F","W","I","B","B9","C901"]
```
`B9`会提供比`B`更具有意见性的建议（如代码可读性，可维护性），这些建议默认是禁用的。特别是，`B901`会检查最大行长度，就像内置的`E501`一样，但有一个10%的容忍度。忽略内置`E501`并将最大行长度设置为合理的值：
```toml
# pyproject.toml
[tool.ruff.lint]
ignore = ["E203","E501"]

[tool.ruff]
line-length = 100
```
### 使用Ruff识别安全漏洞
`Ruff`中的安全功能来源于`Bandit`，当前仅实现了其核心功能。

在配置文件中启用安全插件（S代表security）：
```toml
#pyproject.toml
[tool.ruff.lint]
select = ["C","E","F","W","I","B","B9","S"]
```
该模式会标记出 `assert` 语句（警告代码 B101），因为`assert`主要用于调试，并且在 Python 以优化模式（使用 -O 标志）运行时会被移除。这意味着如果在生产代码 (
运行在生产环境的程序逻辑本体) 中使用`assert` 来强制执行接口约束或进行任何形式的输入验证，那么当代码被优化时，这些检查将被完全删除，从而可能引入安全漏洞。

与在生产代码中的使用不同，assert 语句是 Pytest 测试框架的核心组成部分。在 Pytest 中，assert 用于验证测试的期望结果是否为真。如果 assert 的条件为假，Pytest 会捕获 AssertionError 并将测试标记为失败，同时提供详细的失败报告。

所以在文件夹`tests`中，我们需要禁用`S`检查，即：
```toml
[tool.ruff]
per-file-ignores = { "tests/*" = ["S101"] }
```
Ruff通过静态文件检查发现已知问题。如果你非常关注安全问题，应该考虑使用额外的工具，例如一个模糊测试工具，比如`python-afl`。

## 使用`pip-audit`在依赖项中查找安全漏洞
`pip-audit` 工具有一个的不安全 Python 包数据库，其会根据该数据库检查你项目的依赖项是否存在已知安全漏洞。请添加以下 Nox session，在你的项目中运行 `pip-audit` 工具进行检查：
下载:
```bash
$ uv add pip-audit --dev
```
在终端运行：
```
$ uv run pip-audit
```
在nox中：
```py
from nox.sessions import Session

@nox.session(python="3.11")
def audit(session: Session) -> None:
    """Check for known security vulnerabilities in dependencies."""
    session.run("pip-audit", external=True)
```
通过将 audit 添加到 nox.options.sessions 中，将其包含在默认的 Nox session中：
```py
# noxfile.py
nox.options.sessions = "lint", "audit", "tests"
```
为了了解`pip-audit`如何工作，安装[`insecure-package`](https://pypi.org/project/insecure-package/)：
```bash
$ uv add insecure-package
```
然后运行
```bash
$ uv run nox -rs audit
```
最后别忘了删除该包：
```bash
$ uv remove insecure-package
```
## 使用 uv 在 Nox session 中管理依赖

## 使用 pre-commit 管理Git Hooks
Git提供了Hook，允许你在执行重要操作（如提交，推送）时运行自定义命令。你可以利用这一点在提交更改时运行自动化检查。pre-commit是一个用于管理和维护此类Hook的框架。使用它可以将最佳行业标准代码检查工具集成到你的工作流程中，即使这些工具是用除Python以外的语言编写的。

安装pre-commit：
```bash
$ uv add pre-commit --dev
```
使用 `.pre-commit-config.yaml` 配置文件配置 `pre-commit`，在您的仓库顶层目录中。关于什么是`yaml`文件，可以参考[视频](https://www.bilibili.com/video/BV1VybzzoEcC?vd_source=189ac0e5f555cc7d23863c9d75a86118)。我们从以下示例配置开始：
```yaml
#.pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml #检查 YAML 文件的语法是否正确

  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.13.0
    hooks:
      # Run the linter.
      - id: ruff-check
        args: [ --fix ]
      # Run the formatter.
      - id: ruff-format
```
类似一个开关，你需要手动打开`pre-commit`功能，打开后，后续更改文件`.pre-commit-config.yaml`并不用再次执行打开功能的操作。

```bash
$ uv run pre-commit install
```
Hooks会在每次`git commit`时自动运行，对任何新创建或修改的文件应用检查。当你添加新的Hooks（就像现在这样）时，你可以使用以下命令手动对所有文件触发它们：
```bash
$ uv run pre-commit run --all-files

[INFO] Initializing environment for https://github.com/astral-sh/ruff-pre-commit.
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/astral-sh/ruff-pre-commit.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
```

不过，这里有个问题：示例配置将 `Ruff` 锁定到特定版本，`uv.lock` 也是如此。这种设置要求手动保持版本一致，并且当由 `pre-commit`、`uv` 和 `Nox` 管理的环境出现偏差时，可能会导致检查失败。

让我们使用仓库本地`Hook`替换`Ruff`条目，并在`uv`创建的开发环境中运行`Ruff`：
```yaml
#.pre-commit-config.yaml
  - repo: local
    hooks:
    - id: check
      name: check
      entry: uv run ruff check --fix
      language: system
      types: [python]
    - id : format
      name: format
      entry: uv run ruff format
      language: system
      types: [python]
```

此方法允许依赖 `uv` 来管理开发依赖项，无需担心其他工具引起的版本不匹配问题。

检查运行速度略快于相应的Nox会话，原因有两个：
- 它们只运行由所讨论的提交更改的文件；
- 它们假设工具已经安装。