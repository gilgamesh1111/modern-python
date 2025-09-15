# Testing

在本章，我将讨论如何将自动化测试添加到您的项目中。

## 使用pytest进行单元测试

单元测试，正如其名，验证代码单元的功能，例如单个函数或类。

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

## 使用 `Coverage.py` 进行代码覆盖率
代码覆盖率是指在运行测试时，程序源代码被执行的程度。Python程序的代码覆盖率可以使用名为`Coverage.py`的工具来检测。可以通过`pytest-cov`插件安装它，该插件将`Coverage.py`与`pytest`集成：

```bash
$ uv add --dev pytest-cov coverage[toml]
```
可以使用pyproject.toml配置文件来配置Coverage.py，前提是它已如上所示安装了toml扩展（`coverage[toml]`）。更新此文件以告知工具您的包名和源树布局。配置还启用了分支分析和显示缺失覆盖率的行号：
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
```
% missing from source

## 使用`Nox`进行测试自动化

[`Nox`](https://nox.thea.codes/) 是 [`tox`](https://tox.readthedocs.io/)的继任者。该工具自动化了在多个Python环境中的测试。Nox只需安装任务所需的依赖项,就可以简单地隔离环境中运行任何类型的任务。

安装`nox`：
```bash
uv add --dev nox
```
`nox`使用标准的python文件来配置

```python
# noxfile.py
import nox


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
% missing from source
Nox每次调用都会从头开始重新创建虚拟环境（这是一个合理的默认设置）。可以通过传递--reuse-existing-virtualenvs（-r）选项来加快速度：

```bash
$ uv run nox -r
```
有时，您需要向pytest传递额外的选项，例如选择特定的测试用例。通过session.posargs变量更改session以允许传递给pytest选项：
```python
# noxfile.py
import nox


@nox.session(python=["3.11", "3.12"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("uv", "install", external=True)
    session.run("pytest", *args)
```
现在您可以在虚拟环境中运行特定的测试模块：
```bash
$ uv run nox -- tests/test_console.py
```
这里的`--`是Nox的选项，告诉它将后面的信息作为posargs传递给pytest。
效果类似于
```bash
$ uv run pytest tests/test_console.py --cov
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
该插件提供了`mocker`的`test fixture`，它是标准模拟库的一个微包装。