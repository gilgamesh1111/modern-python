# Testing

在本章，我将讨论如何将自动化测试添加到的项目中。

## 使用pytest进行单元测试

单元测试，正如其名，验证代码单元的功能，例如单个函数或类。关于更多的`pytest`，可以参考[视频](https://www.youtube.com/watch?v=cHYq1MRoyI0)

首先下载`pytest`:
```bash
$ uv add pytest --dev
```
这里的`--dev`为 development dependency，即将`pytest`作为开发依赖，并不作为运行时依赖，在后续的打包中，并不会将该模块打包进去。
关于打包，在后续会讲：[打包](#build)

现在组织你的项目结构如下：
```
modern_python/
├── src
└── tests
    ├── __init__.py
    └── test_console.py
```
该文件 `__init__.py` 为空，用于声明测试套件为一个包。虽然这并非严格必要，但它可以帮助测试套件反映被测试包的布局（`src layout`）。

test_console.py 文件包含对控制台模块的测试用例，该用例检查程序是否以零状态码退出(`exit code 0` 即程序正常退出，表示程序正常运行)。
```python
# tests/test_console.py
import click.testing

from modern_python import console


def test_main_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(console.main)
    assert result.exit_code == 0
```
Click的`testing.CliRunner`可以在测试用例中调用命令行界面。因为该`runner`在测试模块很常用，所以一般使用`text fixture`的方式来提供它，*text fixture*是一个函数，使用`pytest.fixture`装饰器来标记它。该函数的返回值将作为测试用例的参数（使用同一名称）使用。

关于装饰器，可以参考[视频](https://www.bilibili.com/video/BV1Uz421Z79L?vd_source=189ac0e5f555cc7d23863c9d75a86118)，在后面会经常用到

现在代码可以修改为：

```python
# tests/test_console.py
import click.testing
import pytest

from modern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
```
该代码与上方的是等价的。

使用`pytest`运行测试用例:
```bash
$ uv run pytest
============================================================ test session starts ============================================================
platform win32 -- Python 3.11.13, pytest-8.4.2, pluggy-1.6.0
rootdir: D:\git_clone\modern_python
configfile: pyproject.toml
plugins: cov-7.0.0
collected 1 item

tests\test_console.py .                                                                                                                [100%]

============================================================= 1 passed in 4.13s =============================================================
```
使用后，`pytest`会自动找到根目录中的tests文件夹，找到以test_开头的文件，然后运行它们。运行文件时，会运行测试所有以test_开头的函数，如果是class，需要以Test开头，该class中的函数也要以test_开头，才会运行。如：
```python
class TestClass:
    def test_one(self) -> None:
        x = "this"
        assert "h" in x

    def test_two(self) -> None:
        x = "hello"
        with pytest.raises(AssertionError):
            assert hasattr(x, "check")
```
```{note}
在该例子中，`pytest.raises` 用于在测试期间检查异常是否发生。
如果报错（`assert hasattr(x, "check")`），且异常类型是AssertionError，那么`pytest`测试通过。更多的，参考[pytest.raises](https://docs.pytest.org/en/latest/reference.html#pytest-raises)
```

## 使用 `Coverage.py` 进行代码覆盖率
代码覆盖率是指在运行测试时，程序源代码被执行的程度。Python程序的代码覆盖率可以使用名为`Coverage.py`的工具来检测。可以通过`pytest-cov`插件安装它，该插件将`Coverage.py`与`pytest`集成：

```bash
$ uv add --dev pytest-cov coverage[toml]
```
可以使用pyproject.toml配置文件来配置Coverage.py，前提是安装了如上所示的toml扩展（`coverage[toml]`）。更新此文件以告知工具包名和源树布局。配置还启用了分支分析和显示缺失覆盖率的行号：
```toml
# pyproject.toml
[tool.coverage.paths]
source = ["src", "*/site-packages"]

[tool.coverage.run]
branch = true
source = ["modern_python"]

[tool.coverage.report]
show_missing = true
```

要启用覆盖率报告，请使用 --cov 选项调用 pytest：
```bash
$ uv run pytest --cov
============================================================ test session starts ============================================================
platform win32 -- Python 3.11.13, pytest-8.4.2, pluggy-1.6.0
rootdir: D:\git_clone\modern_python
configfile: pyproject.toml
plugins: cov-7.0.0
collected 1 item

tests\test_console.py .                                                                                                                [100%]

============================================================== tests coverage ===============================================================
_____________________________________________ coverage: platform win32, python 3.11.13-final-0 ______________________________________________

Name                            Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------------
src\modern_python\__init__.py       1      0      0      0   100%
src\modern_python\console.py       18      1      2      1    90%   33
---------------------------------------------------------------------------
TOTAL                              19      1      2      1    90%
============================================================= 1 passed in 2.19s =============================================================
```

## 使用`Nox`进行测试自动化

[`Nox`](https://nox.thea.codes/) 是 [`tox`](https://tox.readthedocs.io/)的继任者。该工具能自动化在多个Python环境中的测试。Nox只需安装任务所需的依赖项,就可以简单地隔离环境中运行任何类型的任务。

安装`nox`：
```bash
uv add --dev nox
```
`nox`使用标准的python文件来配置
你可以在 `noxfile.py` 中配置让 `Nox` 使用 `uv` 来创建虚拟环境和安装依赖，这样会比默认方式更快，且会自动安装python版本：
```python
# noxfile.py
import nox

nox.options.default_venv_backend = "uv"
@nox.session(python=["3.11", "3.12"])
def tests(session):
    session.run("uv", "sync", external=True)
    session.run("pytest", "--cov")
```
此文件定义了一个名为tests的session，该session用于安装项目依赖并运行测试。由于`uv`不是由Nox创建的环境的一部分，因此我们指定external以避免关于外部命令泄漏到隔离的测试环境中的警告。

Nox为列出的Python版本（3.11和3.12）创建虚拟环境，并在每个环境中运行会话：

```bash
$ uv run nox
```

Nox每次调用都会从头开始重新创建虚拟环境（这是一个合理的默认设置）。可以通过传递--reuse-existing-virtualenvs（-r）选项来加快速度：

```bash
$ uv run nox -r
```
有时，需要向pytest传递额外的选项，例如选择特定的测试用例。通过session.posargs变量更改session以允许传递给pytest选项：
```python
# noxfile.py
import nox


@nox.session(python=["3.11", "3.12"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("uv", "sync", external=True)
    session.run("pytest", *args)
```
现在可以在虚拟环境中运行特定的测试模块：
```bash
$ uv run nox -- tests/test_console.py
```
这里的`--`是Nox的选项，告诉它将后面的信息作为posargs传递给pytest。
效果类似于
```bash
$ uv run pytest tests/test_console.py --cov
```
## 模拟工具`mock`
[`mock`](https://www.bilibili.com/video/BV1bawPesEZL/?share_source=copy_web&vd_source=189ac0e5f555cc7d23863c9d75a86118)来源于`unittest.mock`，是Python标准库的一部分。该库有三个重要的模块。
- `Mock`：简单的模拟对象。我们可以任意塑造他没有的属性或者方法
    ```python
    from unittest.mock import Mock

    mock = Mock()
    mock.get.return_value = "abc"
    print(mock.get())
    ```
    这里我们捏造了`get`方法，调用该方法会返回字符串`abc`。
- `MagicMock`：是`Mock`的升级版，可以定义魔法方法（关于魔法方法参考[视频](https://www.bilibili.com/video/BV1vx421D7AP/?share_source=copy_web&vd_source=189ac0e5f555cc7d23863c9d75a86118)）。
    ```python
    from unittest.mock import MagicMock

    mock = MagicMock()
    mock.__str__.return_value = "abc"
    print(str(mock))
    ```
    这里对其的魔法方法`__str__`设定了返回值`abc`。
- `patch`：用于替换函数，类，或者模块的行为。
    ```python
    from unittest.mock import patch

    def foo():
        return "abc"

    with patch("__main__.foo") as mock_foo:
        mock_foo.return_value = "123"
        print(foo()) # 123
    print(foo()) # abc
    ```
    这里我们用`patch`来替换函数`foo`，并定义了返回值`123`。
```{note}
`patch("__main__.foo")` 这行代码创建的是一个 **Patcher（补丁）对象**，它本身并不是最终的模拟对象（Mock）。可以把它理解为一个“补丁控制器”。

当这个 Patcher 对象被用于 `with` 语句时：

1.  在进入 `with` 代码块时，它会**创建一个全新的 `MagicMock` 对象**，并用这个 `MagicMock` 来临时替换掉目标函数 `foo`。
2.  为了能够配置这个新创建的 `MagicMock`，你**必须使用 `as` 关键字来捕获它**，例如 `with patch(...) as mock_foo:`。
3.  在这个正确的写法中，变量 `mock_foo` 才是那个真正可以被配置的 `MagicMock` 对象，你可以设置它的 `return_value` 等属性来控制模拟行为。
```


## 使用pytest-mock进行模拟
单元测试应该是快速、隔离和可重复的。但console.main的测试不符合这些要求：
- **不快**：因为它需要完整地往返一次维基百科API才能完成。
- **不在隔离的环境中运行**：因为它会通过网络发送实际请求。
- **不可重复**：因为其结果取决于API的返回。但API的返回是随机的，而且当网络断开时，测试会失败。

`mock`用来将测试中的部分替换为模拟对象,该模块在python的标准库存在：`unittest.mock`，其集成在`pytest`中，可以使用以下指令安装：
```bash
$ uv add --dev pytest-mock
```
该插件提供了`mocker`的`test fixture`，它是标准模拟库的一个微包装。使用`mocker.patch`替换`requests.get`函数为mock对象。这个模拟对象对于涉及维基百科API的任何测试用例都很有用，所以我们为它创建一个`test fixture`：
```python
# tests/test_console.py
@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")
```
将`test fixture`添加到测试用例的函数参数中：
```python
def test_main_succeeds(runner, mock_requests_get):
    ...
```
这里的`mock_requests_get`会替换函数中的`requests.get`。

如果你现在运行`Nox`，测试会失败，因为`click`期望传入一个字符串作为控制台输出，但它接收到了一个`mock`对象。仅仅`requests.get`是不够的。模拟对象还需要返回一些有意义的内容，即包含有效JSON对象的响应。所以我们要配置模拟对象被调用时的返回值，return_value。

让我们再次看看这个例子：
```python
with requests.get(API_URL) as response:
    response.raise_for_status()
    data = response.json()
```
上述代码使用`response `作为上下文管理器。`with`语句是以下略微简化的伪代码的语法糖：
```python
context = requests.get(API_URL)
response = context.__enter__()

try:
    response.raise_for_status()
    data = response.json()
finally:
    context.__exit__(...)
```
所以其本质是一个函数调用链：
```python
data = requests.get(API_URL).__enter__().json()
```
重写`test fixture`，并在配置这个调用链：
```python
@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock
```
再次运行Nox，测试通过。

`Mock`不仅能显著加速测试进程，还支持离线测试场景。由于其返回值固定且可预知，`Mock`还能帮助编写可重复执行的测试用例。这意味着我们可以实现更精准的验证，例如：能够可靠地检查API返回的标题是否已正确打印到控制台。
```python
def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output
```
此外，可以通过检查Mock的 `called` 属性来查看它们是否被调用。
```python
# tests/test_console.py
def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called
```
模拟对象还允许使用 `call_args` 属性来检查它们被调用的参数。这使能够检查传递给 `requests.get` 的 URL：
```python
# tests/test_console.py
def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]
```
若需配置模拟对象，使其抛出异常而非返回值，可将异常实例或异常类直接赋值给该模拟对象的 side_effect 属性。让我们检查程序在请求错误时是否以状态码 1 退出：
```python
# tests/test_console.py
def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1
```
通常情况下，每个测试用例应该只有一个断言，这样可以更容易找出失败原因。

新功能或错误修复的测试应该在实现之前编写。这也被称为“编写失败的测试”。之所以这样做，是因为这可以提供信心，确保测试实际上在测试某些内容，而不是因为测试本身的缺陷而通过。
## Example CLI：重构
一个好的测试的好处是它让你在无需担心破坏代码的情况下重构代码。让我们将维基百科API移动到单独的模块中。创建一个名为`src/modern-python/wikipedia.py`的文件，并包含以下内容：

```python
# src/modern-python/wikipedia.py
import requests

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(HTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    )
}


def random_page():
    with requests.get(API_URL, headers=headers) as response:
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    data = random_page()
    print(data["title"])
    print(data["extract"])
```
现在，`console`模块现在可以简单地调用`wikipedia.random_page`：
```python
import textwrap

import click

from modern_python import __version__, wikipedia


@click.command()
@click.version_option(version=__version__)
def main():
    """The modern Python project."""
    data = wikipedia.random_page()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))


if __name__ == "__main__":
    main()
```
最后，调用Nox进行测试。
## Example CLI：优雅地处理异常
如果在没有互联网连接的情况下运行示例应用程序，终端将充满冗长的错误跟踪信息。这就是当Python解释器因未处理的异常而终止时发生的情况。对于这种常见的错误，最好在屏幕上打印一条方便阅读且具体的消息。

让我们将其表达为一个测试用例，通过配置模拟来引发一个`RequestException`。（requests库有更具体的异常类，但在这个例子中，我们只处理基类。）
```python
# tests/test_console.py
import requests


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
```
为了让该测试通过，可以将RequestException转换为ClickException。当click遇到这个异常时，它会将异常信息打印到标准错误，并以状态码1退出程序。可以通过将原始异常转换为字符串来重用异常信息。

以下是更新后的wikipedia模块：
```python
# src/modern-python/wikipedia.py
import requests
import click

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(HTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    )
}


def random_page():
    try:
        with requests.get(API_URL, headers=headers) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)


if __name__ == "__main__":
    data = random_page()
    print(data["title"])
    print(data["extract"])
```
## Example CLI：选择维基百科的语言版本
在本节中，我们添加了一个命令行选项来选择维基百科的语言版本。

维基百科的版本通过语言代码来识别，该代码用作`wikipedia.org`下的子域名。通常，这是[ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1)和[ISO 639-3](https://en.wikipedia.org/wiki/ISO_639-3)分配给语言的两位或三位字母代码。以下是一些示例：

- `fr` 代表法语维基百科
- `jbo` 代表洛贾班语维基百科
- `ceb` 代表宿务语维基百科

Wiki不支持中文

作为第一步，让我们向`wikipedia.random_page`函数添加一个可选的参数来指定语言代码。当传递了替代语言时，API请求应发送到相应的维基百科版本。测试用例放置在一个名为`test_wikipedia.py`的新测试模块中：
```python
# tests/test_wikipedia.py
from modern_python import wikipedia


def test_random_page_uses_given_language(mock_requests_get):
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]
```
现在`mock_requests_get text fixture`被两个测试模块使用。你可以将其移动到单独的模块中并从那里导入，但Pytest提供了一个更方便的方法：放置在conftest.py文件中的`text fixture`会被自动发现，并且同一目录级别的测试模块可以隐式导入地使用它们。创建文件：
```py
# tests/conftest.py
import pytest


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock
```
为了使测试通过，我们将`API_URL`转换为格式化字符串，并使用`str.format`方法将指定的语言代码插入到URL中：
```py
import click
import requests

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(HTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    )
}


def random_page(language):
    url = API_URL.format(language=language)
    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
```
我们需要新功能能通过命令行添加 `--language` 选项。测试用例模拟了` wikipedia.random_page` 函数，并使用 `assert_called_with` 方法对模拟对象进行检查，以确保用户指定的语言被传递给该函数：
```py
# tests/test_console.py
@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("modern_python.wikipedia.random_page")


def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")
```
现在需要使用`click.option`装饰器来实现新功能。以下是`console`的最终版本：
```py
# src/modern-python/console.py
import textwrap

import click

from moden_python import __version__, wikipedia


@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language):
    """The modern Python project."""
    data = wikipedia.random_page(language=language)

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))
```
## 使用fakes
模拟对象（Mocks）可帮助你测试依赖于庞大子系统的代码单元，但它们并非实现此目的的唯一技术。例如，若你的函数需要数据库连接，传递一个内存数据库往往比使用模拟对象更简单、更高效。

伪实现（Fake Implementations） 是模拟对象的理想替代方案 —— 模拟对象在面对错误使用时可能过于 “宽容”，且与被测系统的实现细节耦合过紧（`mock_requests_get fixture`就是典型例子）。对于大型数据对象，可通过测试对象工厂生成，而非用模拟对象替代（推荐你了解优秀的 [`factoryboy`](https://factoryboy.readthedocs.io/) 包）。

实现一个伪 API（Fake API）超出了本教程的范围，但我们会涵盖其中一个方面：如何编写同时需要清理代码（tear down code）和初始化代码（set up code）的`test fixture`。假设你已编写了如下伪 API 实现：

```py
class FakeAPI:
    url = "http://localhost:5000/"

    @classmethod
    def create(cls):
        ...

    def shutdown(self):
        ...
```
以下将不会工作：
```py
@pytest.fixture
def fake_api():
    return FakeAPI.create()
```
API在使用后需要关闭，以释放资源。可以通过以下`test fixture`为生成器来实现这一点：
```py
@pytest.fixture
def fake_api():
    api = FakeAPI.create()
    yield api
    api.shutdown()
```
其中，关于生成器可以参考[视频](https://www.bilibili.com/video/BV1jt421c7yN?vd_source=189ac0e5f555cc7d23863c9d75a86118)

Pytest 会自动处理生成器的运行：将生成器中 `yield` 产出的值传递给测试函数，并在测试函数执行完成后，自动执行 `yield` 之后的清理代码。
如果`fixture`的初始化（set up）和清理（tear down）操作开销较大（例如启动 / 停止伪 API 服务耗时较长），你还可以考虑扩展`fixture`的作用域（scope）。默认情况下，`fixture`的作用域是 “每个测试函数”—— 即每个测试函数执行时都会重新创建一次夹具实例；反之，你可以将伪 API 服务器配置为 “每个测试会话（per test session）” 仅创建一次。
```py
@pytest.fixture(scope="session")
def fake_api():
    api = FakeAPI.create()
    yield api
    api.shutdown()
```
## 端到端测试
对实时生产服务器开展测试非单元测试的范畴，但亲眼见证代码在真实环境中运行是最可靠的。这类测试被称为端到端测试——尽管往往速度迟缓、稳定性差且结果难以预测，不适合在CI服务器或开发过程中进行自动化执行，但依然有着不可替代的应用场景。

我们可以还原原始测试用例，并借助Pytest的标记功能添加自定义标记。于是以后，可通过Pytest的-m选项灵活选择执行特定测试或跳过某些测试。

关于pytest的`mark`功能参考[视频](https://www.youtube.com/watch?v=cHYq1MRoyI0)

```py
# tests/test_console.py
@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
```
我们使用自定义的`mark`，pytest无法识别，需要在`conftest.py`文件中使用`pytest_configure`注册该`mark`。如下所示：
```py
# tests/conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
```
最后，传递 `-m "not e2e"` 到 Pytest 中排除端到端测试的自测试：
```py
# noxfile.py
import nox


@nox.session(python=["3.11", "3.12"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("uv", "install", external=True)
    session.run("pytest", *args)
```
现在可以通过向Nox会话传递`-m e2e`来运行端到端测试，使用双横线（--）将它们与`Nox`的自身选项分开。以下是如何在Python 3.12的测试环境中运行端到端测试的方法：

```bash
$ uv run nox -rs tests-3.12 -- -m e2e
```