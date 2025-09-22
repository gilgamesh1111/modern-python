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
在nox session中添加文档字符串，当使用--list-sessions列出session时，Nox会显示它们。
```py
# noxfile.py
"""Nox sessions."""
def tests(session: Session) -> None:
    """Run the test suite."""

def audit(session: Session) -> None:
    """Scan dependencies for insecure packages."""

def lint(session: Session) -> None:
    """Lint using ruff."""

def format(session: Session) -> None:
    """Format using ruff."""

def typeguard(session):
    """Run typeguard when testing."""
```
查看概览：
```bash
$ uv run nox --list-sessions

nox sessions.

Sessions defined in D:\git_clone\modern_python\noxfile.py:

* tests-3.11 -> Run the test suite.
* tests-3.12 -> Run the test suite.
* audit -> Scan dependencies for insecure packages.
* lint-3.11 -> Lint using ruff.
* lint-3.12 -> Lint using ruff.
- format -> Format using ruff.
- typeguard-3.11 -> Run typeguard when testing.

sessions marked with * are selected, sessions marked with - are skipped.
```
## 为tests添加docstrings
以下是关于记录测试用例的三个有用指南：
- 明确说明预期的行为，并对此进行具体说明。
- 省略所有从它是测试用例这一事实中已经可以推断出来的内容。例如，避免使用像“测试是否”、“正确”、“应该”这样的词。
- 使用'It'来指代被测试的系统。无需反复写出被测试的具体函数、类或模块的名称。（更好的地方可能是测试模块的文档字符串，或者如果使用测试类，那么就在测试类中。）

以下示例演示了如何为测试用例编写文档字符串：
```py
# tests/test_console.py
def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code of zero."""
```

## 使用ruff验证文档字符串与函数的一致性

文档很容易与代码库脱节。将其嵌入代码库可以减轻这个问题，这也是docstrings如此有用的原因之一：它们紧挨着它们所描述的内容，因此很容易保持同步。

然而，在没有严格限制下docstrings依然容易与代码脱节。好消息是，通过遵循像Google风格这样的docstring约定，你可以让工具检测到这种偏差。

Ruff可以检查docstring描述是否与函数定义匹配，其使用pydoclint内核检查。例如，假设你将wikipedia.random_page的language参数重命名为lang，但忘记更新docstring。Ruff会注意到并提醒你以下警告：
```
Missing argument description in the docstring for `random_page`: `lang`
```
在pyproject.toml中启用这个功能：
```toml
#pyproject.toml
[tool.ruff]
select = ["C","E","F","W","I","B","B9","S","ANN","D","DOC"]
```
在我写该文档时，需要启用ruff的`preview`功能才会进行docstring检查
```toml
# pyproject.toml
[tool.ruff]
preview = true
```
默认情况下，Ruff要求每个文档字符串必须完全指定参数、返回值和异常。在某些情况下，这可能不是我们想要的的。例如，记录测试函数或Nox session的参数通常会创建冗余。通过配置文件配置ruff以接受单行文档字符串：
```toml
# pyproject.toml
[tool.ruff.lint.pydoclint]
ignore-one-line-docstrings = true
```
## 使用 xdoctest 运行文档示例
好的示例可以替代冗长的解释，人们擅长从示例中学习。

按照惯例，文档字符串示例应像在Python环境中输入一样编写。下面是`wikipedia.random_page`文档中的一个示例：

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

    Example:
        >>> from modern_python import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
```
- 为什么示例在打印到控制台之前将页面标题转换为布尔值?
诚然，这使得示例的表达性降低，但另一方面，示例变得可重复。毕竟，事先无法知道函数返回哪些数据。

- 为什么想让示例可重复？因为这使得可以将示例作为测试运行。

xdoctest包运行你的文档字符串中的示例，并将实际输出与文档字符串中预期的输出进行比较。这具有多重作用：

- 检查示例的正确性。
- 确保文档是最新的。
- 为你的代码库提供额外的测试覆盖率。

将此工具添加到你的开发者依赖项：
```bash
$ uv add xdoctest --dev
```
在终端运行：
```bash
$ uv run xdoctest src/modern_python/wikipedia.py
```
或者使用包名：
```bash
$ uv run xdoctest modern_python.wikipedia
```
将以下Nox session添加。此session会安装依赖包，因为工具本身以及示例都需要能够导入它。
```py
# noxfile.py
@nox.session(python=["3.11", "3.12"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("uv", "sync", external=True)
    session.run("xdoctest", package, *args)
```
默认情况下，Nox会话使用all子命令来运行所有示例。您也可以使用list子命令列出示例，或者运行特定的示例：

Xdoctest以及作为插件与Pytest集成，因此也可以将此工具安装到现有的Nox会话中用于Pytest，并通过--xdoctest选项启用它。在这里，我们使用的是独立模式，其优点是保持单元测试和doctest分离。

## 使用 Sphinx 创建文档
Sphinx是一个Python文档工具，它可以生成文档，包括HTML，PDF和其他格式。本书的文档就是使用Sphinx生成的。其他竞品，比如[mkdocs](https://www.mkdocs.org/)，当前也被广泛使用，许多大型项目也使用mkdocs生成文档，如[fastapi](https://fastapi.tiangolo.com/)和[uvicorn](https://www.uvicorn.org/)。个人来说更喜欢sphinx的效果，于是这里将会讲解如何使用sphinx来生成文档。

将sphinx添加到你的开发者依赖项：
```bash
$ uv add sphinx --dev
```
创建一个名为docs的目录。主文档位于文件docs/index.md中。让我们从一个简单的占位文本开始：
> 从sphinx来说，其使用的是rst文件（Restructured Text）,但其糟糕的语法和难以忍受的编码体验，令我去寻找更好的工具。
>
> 了解到[myst-parser](https://myst-parser.readthedocs.io/)可以通过编写md文本的方式来构建文档，而md文本的语法更加简单，更加易读，编写体验更好，而且广泛的应用在大模型中，并且你可以注意到，README文档即是使用md编写。
>

为了使用md编写，我们需要添加依赖：
```bash
$ uv add myst-parser --dev
```

创建Sphinx配置文件docs/conf.py。这提供了关于项目的元信息：
```py
# docs/conf.py
"""Sphinx configuration."""
project = "modern-python"
author = "Your Name"
copyright = f"2025, {author}"
# Enable MyST in Sphinx
extensions = ["myst_parser"]
```
添加一个Nox session来构建文档：
```py
# noxfile.py
@nox.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.install("sphinx","myst-parser")
    session.run("sphinx-build", "docs", "docs/_build")
```
为了保险起见，将docs/conf.py包含在代码检查session：
```py
# noxfile.py
locations = "src", "tests", "noxfile.py", "docs/conf.py"
```
运行 Nox session：
```bash
$ uv run nox -s docs
```
现在可以在浏览器中打开文件docs/_build/index.html，以离线查看您的文档。
## 使用Myst编写文档
关于md语法，可以参考[文档](https://markdown.com.cn/basic-syntax/)

Sphinx文档可以分散在多个相互连接的文件中。我们可以通过在文档中加入许可证来查看这是如何工作的。创建文件docs/license.md，该文件使用include指令包含父目录中的LICENSE文件：

    ```{eval-rst}

    .. include:: ../LICENSE

    ```
这里的eval-rst，是myst的拓展语法，表示在其内部可以使用rst语法。这里的include指令是rst语法：将外部文件的内容 “嵌入” 到当前文档中。
其效果可见LICENSE。

通过在docs/index.md的主文档中添加toctree指令，将许可证添加到导航侧边栏。

    ```{toctree}
    :hidden:
    :caption: 目录

    LICENSE
    ```
`:hidden:`选项防止目录被插入到主文档本身，目录已经包含在侧边栏中。

这里的toctree其基本格式如下
```
{toctree}
:选项1: 值1
:选项2: 值2

文档路径1
文档路径2
...
```

使用Nox构建文档。在浏览器中重新加载页面后，你应该可以在导航侧边栏中看到许可证。

```bash
$ uv run nox -rs docs
```
## 使用autodoc2生成API文档

我们使用 Sphinx 从包中的文档字符串和类型注解生成 API 文档，使用了三个 Sphinx 扩展：

- sphinx-autodoc2 允许 Sphinx 从包中的文档字符串生成 API 文档。
- napoleon 预处理 Google 风格的文档字符串为 reStructuredText。
- sphinx-autodoc-typehints 使用类型注解来记录函数参数和返回值的类型。

autodoc 和 napoleon 扩展为 Sphinx 内置 ，无需显式安装。

将 sphinx-autodoc-typehints 添加到开发依赖项中：
```bash
$ uv add sphinx-autodoc-typehints sphinx-autodoc2 --dev
```
将扩展和的你的依赖安装到Nox session中。包是必需的，这样Sphinx才能读取其文档字符串和类型注解。
```py
# noxfile.py
@nox.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("uv", "sync", external=True)
    session.install("myst-parser", "sphinx", "sphinx-autodoc2")
    session.run("sphinx-build", "docs", "docs/_build")
```

激活拓展：
```py
# docs/conf.py
project = "modern-python"
author = "Your Name"
copyright = f"2025, {author}"
extensions = [
    "myst_parser",
    "autodoc2",
]

# -- Autodoc2 配置 ---------------------------------------------------

# 启用自动模式并指定要文档化的包
autodoc2_packages = [
    {
        "path": "../src/modern_python",  # 从 conf.py 到您的包的相对路径
        "auto_mode": True,
    },
]

# 将默认输出格式设置为 MyST Markdown
autodoc2_render_plugin = "myst"

```
在 index.md 中添加以下内容：

    ```{toctree}
    :hidden:
    :caption: 目录

    apidocs/index
    LICENSE
    ```

其效果可在 API Reference 中看到。


当然存在其他生成api reference的方法，例如fastapi的[文档](https://fastapi.tiangolo.com/reference/fastapi/#fastapi.FastAPI--example)使用mkdocs生成

若读者对其感兴趣可以在issue中向我提交，我会在后续加入。