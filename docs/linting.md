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
- F 会解析源文件并查找无效Python代码的工具。
- W 和 E是警告和错误，其会检查你的Python代码是否符合PEP 8中的一些样式约定。
- C会检查你的Python包的代码复杂度是否超过了配置的限制。

其中，代码复杂度一般与以下有关：
- 分支结构：包含的条件判断（如 if、elif、switch）、循环（for、while）、异常处理（try/except）等控制流语句的数量和嵌套深度。
- 路径数量：程序执行过程中可能的不同路径数量，路径越多，理解和测试难度越大。
- 嵌套深度：代码块（如循环内的循环、条件内的条件）的嵌套层次，过深的嵌套会显著增加复杂度

在配置文件`pyproject.toml`中，可以添加以下，以启用其内置违规类并设置复杂度限制：
```toml
# pyproject.toml
[tool.ruff]
select = ["C","E","F","W"]
max-complexity = 10
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
在Nox session设置好之后，您可以像这样重新格式化代码：
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
from hypermodern_python import wikipedia
```
启用Ruff导入检查（`I` 为 `import`）：
```toml
# pyproject.toml
[tool.ruff]
select = ["C","E","F","W","I"]
```
Ruff 会自动识别哪个是本地库。

### 使用Ruff 发现更多 bug
ruff 可以帮助你在程序中找到各种错误和设计问题。

在配置文件中启用插件警告（B代表bugbear）：
```toml
# pyproject.toml
[flake8]
select =  ["C","E","F","W","I","B","B9"]
```
`B9`会提供比`B`更具有意见性的建议（如代码可读性，可维护性），这些建议默认是禁用的。特别是，`B901`会检查最大行长度，就像内置的`E501`一样，但有一个10%的容忍度。忽略内置`E501`并将最大行长度设置为合理的值：
```toml
# pyproject.toml
[ruff.tool]
ignore = ["E203","E501"]

[tool.ruff.lint.pycodestyle]
max-line-length = 100
```
### 使用Bandit识别安全漏洞

### 使用Safety在依赖项中查找安全漏洞