# Documentation
在本章，我将讨论如何为您的项目添加文档。
## 使用Python docstrings注释代码
[文档字符串](https://peps.python.org/pep-0257/#what-is-a-docstring)，也称为docstrings，允许你直接将文档嵌入到您的代码中。一个docstring的例子是`console.main`的第一行，由Click用于生成您命令行界面的使用信息：
```py
# src/modern_python/console.py
def main(language: str) -> None:
    """The modern Python project."""
```
文档字符串用于向阅读你代码的其他开发者传达模块、类或函数的 目的 和 用法 。与注释不同，Python 字节码编译器不会丢弃它们，而是将它们添加到对象的 `__doc__` 属性中。这允许像 Sphinx 这样的工具从你的代码中生成 API 文档。

你可以通过在 `__init__.py` 的顶部添加文档字符串来记录整个包：
```py
# src/modern_python/__init__.py
"""The modern Python project."""
```
在软件包的各个源文件顶部添加文档字符串，以此对软件包中的模块进行文档说明。为`console module`添加文档字符串：
```py
# src/modern_python/console.py
"""Command-line interface."""
```
为`wikipedia module`添加文档字符串：
```py
# src/modern_python/wikipedia.py
"""Client for the Wikipedia REST API, version 1."""
```
截至目前，我们使用的一直是单行文档字符串。实际上，文档字符串也支持多行形式，且遵循一项通用惯例：其首行（摘要行）与后续内容之间需用一个空行隔开。这种结构能清晰划分出**简短摘要**与**详细说明**两部分，让文档信息层次更分明。

在详细说明中，可补充类的属性定义、函数的参数说明、返回值类型及含义等关键信息——这种结构化的文档格式，不仅可读性大幅提升，还能更好地适配各类自动化文档生成工具（如`pdoc`、`Sphinx`等）。

文档字符串的风格有多种选择，常见的包括谷歌（Google）风格、Sphinx风格与NumPy风格。其中，**谷歌风格**以简洁直观、易于编写的特点被广泛采用，因此本章将统一使用该风格进行讲解与实践。

以下示例展示了 `wikipedia.Page` 类的多行文档字符串，其中采用谷歌风格对类属性进行了描述。类的文档字符串需添加在类定义的第一行。
```py
# src/modern_python/wikipedia.py
class Page(BaseModel):
    """Page resource.

    Attributes:
        title: The title of the Wikipedia page.
        extract: A plain text summary.

    """

    title: str
    extract: str
```
同样，可以通过在函数体第一行添加文档字符串来记录函数。以下是对`wikipedia.random_page`函数的多行文档字符串，描述了函数的参数和返回值，以及函数抛出的异常：
```py
# src/modern_python/wikipedia.py
def random_page(language: str = "en") -> Page:
    """Return a random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        language: The Wikipedia language edition. By default, the English
            Wikipedia is used ("en").

    Returns:
        A page resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    """
    url = API_URL.format(language=language)
    ...
```
## 使用Ruff对代码文档进行代码审查
配置`pyproject.toml`以启用插件警告（D代表 docstring）并采用Google文档字符串风格：
```toml
#pyproject.toml
[tool.ruff]
select = ["C","E","F","W","I","B","B9","S","ANN","D"]

[tool.ruff.pydocstyle]
convention = "google"
```
现在运行`uv run nox -rs lint`，插件将报告缺少文档字符串。这是因为tests和 Nox session仍然没有文档。

## 为 Nox Session添加docstrings
在Nox会话中的文档字符串使您的noxfile.py成为一个对贡献者友好、欢迎的地方（同样，几个月后对自己也是如此）。这一点尤其正确，因为当您使用--list-sessions列出会话时，Nox会显示它们。
```py
# noxfile.py
"""Nox sessions."""

def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""

def black(session: Session) -> None:
    """Run black code formatter."""

def lint(session: Session) -> None:
    """Lint using flake8."""

def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""

def mypy(session: Session) -> None:
    """Type-check using mypy."""

def pytype(session: Session) -> None:
    """Type-check using pytype."""

def tests(session: Session) -> None:
    """Run the test suite."""

def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""

def audit(session: Session) -> None:
    """Audit installed packages for security vulnerabilities."""
```
Nox现在提供了自动化快速且信息丰富的概览：
% missing from source
## 向tests添加docstrings