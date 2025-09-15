# Get Start

本章将引导你配置一个健壮、高效的本地开发环境。我们将利用现代化工具来管理项目、依赖和代码质量，为后续的开发工作流奠定坚实的基础。

## IDE (集成开发环境)

IDE (Integrated Development Environment) 是现代软件开发的基石。它远不止是文本编辑器，更是一个集成了代码编写、调试、测试和项目管理的强大平台，是保障代码质量的第一道防线。

*   **静态分析与 Linting:** 优秀的 IDE (如 [VS Code](https://code.visualstudio.com/) 或 [PyCharm](https://www.jetbrains.com/pycharm/)) 能在你编码时进行实时分析，即时指出潜在的语法错误、代码风格问题 (Linter) 和逻辑缺陷 (Static Analysis)。这能极大地减少低级错误。
*   **智能提示与自动补全:** IDE 通过分析代码上下文和依赖库，提供精准的函数、变量提示和自动补全，这不仅提升了开发速度，也有效避免了因拼写或 API 误用而导致的运行时 Bug。
*   **强大的调试器 (Debugger):** 可视化的调试器是定位问题的最强工具。你可以设置断点、单步执行、检查任意时刻的变量状态，从而高效地理解代码的实际行为，无需依赖繁琐的 `print` 语句。
*   **重构工具 (Refactoring):** 代码的可读性和结构对可维护性至关重要。IDE 提供的重构功能（如安全重命名、提取函数、移动模块）让你能在不破坏逻辑的前提下，轻松优化代码结构。

你可以选择你最顺手的 IDE。

## 版本控制：Git

Git 是一个分布式版本控制系统，它追踪文件的每一次变更，是项目可维护性的核心保障。

*   **变更历史与可追溯性:** Git 记录了每一次代码提交 (commit)，包含作者、时间和变更内容。当出现问题时，你可以迅速定位到引入该问题的具体提交，实现快速回滚 (revert) 或修复。
*   **分支策略 (Branching):** 开发新功能或修复 Bug 时，应创建一个独立的分支，在不影响主线 (如 `main` 分支) 稳定性的情况下开发测试。只有当功能完善并通过测试后，才将其合并 (merge) 回主线。这种隔离机制是保证主代码库时刻健壮的关键。
*   **团队协作的基石:** 配合 [GitHub](https://github.com/) 或 [GitLab](https://gitlab.com/) 等平台，Git 的 Pull Request (或 Merge Request) 机制让团队可以进行代码审查 (Code Review)，在代码合并前发现潜在问题，传播知识，并统一代码风格。

没有版本控制的项目是脆弱的。Git 为代码库提供了“后悔药”和“保险”，确保任何改动都可控、可查、可恢复。

### 如何使用Git

该部分可以参考up主Alex的[教程](https://www.bilibili.com/video/BV1Hkr7YYEh8?vd_source=189ac0e5f555cc7d23863c9d75a86118)，建议观看1、2、4节。

### Fork

对于不熟悉命令行的开发者，[Fork](https://git-fork.com/) 这类 Git 图形用户界面 (GUI) 工具可以显著提升效率，降低操作复杂性。它能将分支、提交历史和文件变更直观地展示出来，并简化了变基 (Rebase)、合并 (Merge) 等复杂操作。

## 环境与包管理：uv

[`uv`](https://docs.astral.sh/uv/) 是一个革命性的 Python 工具，由开发了著名 Linter `Ruff` 的 Astral 公司用 Rust 语言编写。它旨在成为 `pip`、`pip-tools` 和 `venv` 的一个极速、一体化的替代品，其核心优势是 **“快”**。

对于绝大多数不依赖 `conda-forge` 特殊科学计算包的项目，`uv` 提供了一个更现代、更轻量、更高效的开发工作流。

> `uv` 目前只支持 `pypi.org` 上的依赖包。如果你的项目强依赖 `conda-forge`，可以关注另一个新兴工具 [`pixi`](https://pixi.sh/latest/)，但它目前在 Python 支持上尚不如 `uv` 成熟。

关于`Python`环境管理的历史，可以参考[此视频](https://www.bilibili.com/video/BV13WGHz8EEz?vd_source=189ac0e5f555cc7d23863c9d75a86118)。

### uv 的基础指令

`uv` 的命令与 `pip` 和 `venv` 的设计一脉相承，非常容易上手。

*   **创建虚拟环境**:
    在你的项目根目录下运行，`uv` 会创建一个名为 `.venv` 的虚拟环境。
    ```bash
    uv init modern_python -p 3.11.13
    ```
    这里的 `-p` 参数用于指定 Python 版本，默认为 `3.11`。
    而modern_python会生成新的文件夹，并且该文件夹有以下结构：

    ```
    modern_python/
    ├── .git/
    ├── .gitignore
    ├── .python-version
    ├── main.py
    ├── pyproject.toml
    └── README.md
    ```
    其中 `pyproject.toml` 用于定义项目依赖项和其他元数据。
    `python-version` 用于定义 Python 版本。

**安装与管理依赖：**

使用`uv`管理依赖，其速度非常快。

*   **安装依赖**: 和 `pip` 一样，你可以直接安装一个或多个包。
    ```bash
    $ uv add numpy pandas
    ```

    `uv add` 命令执行后：
    *   依赖项（如 `numpy`）会被添加到 `pyproject.toml` 文件中。
    *   所有包（包括子依赖）的精确版本会被计算并记录在 `uv.lock` 文件中，这保证了环境的**可复现性**——即任何人在任何机器上都能安装完全相同的版本。
    *   所有包的实际文件会被下载并安装到 `.venv` 这个隔离的虚拟环境中。

*   **从文件安装**: 在早期的`python`项目中，一般会有一个`requirements.txt`文件，用于记录依赖项。`uv` 可以高效地处理 `requirements.txt` 文件。
    ```bash
    $ uv pip install -r requirements.txt
    ```

*   **卸载依赖**:
    ```bash
    $ uv remove numpy
    ```

*   **生成依赖文件**: 使用 `freeze` 命令可以生成当前环境中所有包的列表。
    ```bash
    $ uv pip freeze > requirements.txt
    ```

*   **同步环境**: 这是 `uv` 的一个强大功能。`uv sync` 命令可以确保你的虚拟环境与 `pyproject.toml` 文件的内容 **完全一致**。它会自动安装缺失的包，并卸载文件中未列出的包，是实现环境可复现性的利器。
    ```bash
    $ uv sync
    ```

*   **卸载依赖**:
    ```bash
    $ uv remove numpy
    ```

*   **运行代码 (`uv run`)**:
    `uv run` 命令允许你在项目的虚拟环境中执行任意命令或脚本.

    ```bash
    # uv run 可以直接运行 .py 文件
    $ uv run main.py

    # 运行安装在虚拟环境中的工具 (例如 pytest)，这里我们以后会介绍
    $ uv run pytest
    ```

**IDE 解释器设置：**

由于 `uv` 创建的是标准的虚拟环境，因此 IDE 一般会自动找到 `.venv` 环境。


## 项目文件结构

在 Python 项目中，主要有两种组织源代码的布局（Layout）风格：`flat layout`（扁平布局）和 `src layout`（源目录布局）。

### 扁平布局 (Flat Layout)

扁平布局将你的 Python 包（即可导入的目录，如此处的 `modern_python`）直接放置在项目根目录下。

```
.
├── modern_python/      # 你的包
│   ├── __init__.py
│   └── module.py
├── pyproject.toml    # 项目配置文件
├── noxfile.py        # 自动化任务文件
└── README.md         # 项目说明
```

这种结构在简单项目中很常见，但随着项目变得复杂，根目录会变得越来越混乱，混合了源代码、文档、测试和各种配置文件，可维护性随之下降。

### 源目录布局 (Src Layout)

为了解决上述问题，Python 社区现在更推崇 `src layout`。这种布局将所有可安装的源代码都集中在一个 `src` 目录中。

```
.
├── src/                # 源代码目录
│   └── modern_python/  # 你的包
│       ├── __init__.py
│       └── module.py
├── pyproject.toml    # 项目配置文件
├── noxfile.py        # 自动化任务文件
└── README.md         # 项目说明
```

**采用 `src layout` 的优势在于：**

*   **分离项目:** 它清晰地将项目的**源代码** (`src` 目录) 与**项目管理和配置**文件 (如 `pyproject.toml`, `noxfile.py`, `README.md` 等) 分开，使目录结构更加整洁、直观。
*   **提升打包可靠性:** 打包工具可以明确地知道 `src` 目录是唯一的源代码来源，减少了错误地将测试、脚本或文档打包进去的风险。

关于打包，可以在后续[文档](#build)中会讲

因此，我们将在本项目中坚持使用 `src layout`。可以参考python官方的介绍[this](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

`uv`提供了`src layout`的快捷方式：`uv init --lib modern_python`
## 自安装

假设我们有以下项目结构
```
modern_python/
├── src/                # 源代码目录
│   └── modern_python/  # 你的包
│       ├── __init__.py
│       ├── foo.py
|       └── bar.py
├── pyproject.toml    # 项目配置文件
├── noxfile.py        # 自动化任务文件
└── README.md         # 项目说明
```

那么我们如何从`bar.py`导入`foo.py`呢？

一个简单的做法就是相对导入

```python
import .foo
```
该种方法VSCode 依然可以识别，但是对于使用我们包的人来说，他们更希望使用
```python
import modern_python.foo
```
为了保持一致，我们最好也这样写，但是
```python
>>> import sys,pprint
>>> pprint.pp(sys.path)
[
 "",
 "C:\\Users\\Administrator\\AppData\\Roaming\\uv\\python\\cpython-3.11.13-windows-x86_64-none\\python311.zip",
 "C:\\Users\\Administrator\\AppData\\Roaming\\uv\\python\\cpython-3.11.13-windows-x86_64-none\\DLLs",
 "C:\\Users\\Administrator\\AppData\\Roaming\\uv\\python\\cpython-3.11.13-windows-x86_64-none\\Lib",
 "C:\\Users\\Administrator\\AppData\\Roaming\\uv\\python\\cpython-3.11.13-windows-x86_64-none",
 "D:\\git_clone\\modern_python\\.venv",
 "D:\\git_clone\\modern_python\\.venv\\Lib\\site-packages"
]
```
该列表代表python包在哪个路径查找，
列表第一个代表模块查找的路径是在`src/modern_python`中，找模块`modern_python`，这样当然是找不到的，所以，我们需要将我们自己的模块安装到虚拟环境中（使用最后一种查找方式）。

自安装的操作`uv`帮我们做了（当使用`--lib`方式init时），但并不是真的安装，而是在虚拟环境中添加了一个快捷方式。

## 命令行工具 `click`

[`click`](https://click.palletsprojects.com/) 是一个用于快速创建命令行界面(CLI)的库。它通过装饰器来声明命令、参数和选项。

**基本用法**

下面是一个独立的、可直接运行的 `click` 脚本示例：

首先下载 `click`：`uv add click`

```python
import click

@click.command()
@click.option("--count", default=1, help="重复问候的次数。" )
@click.argument("name")
def hello(name, count):
    """一个向 NAME 问好的简单程序。"""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    hello()
```
这里的`name`是必须参数，`count`是一个可选参数，默认值为`1`，`click.echo`用于在终端输出信息。将以上代码保存为 `hello.py`，你可以这样运行它：

```bash
# 传入必需的参数 NAME
$ uv run hello.py World
Hello, World!

# 使用 --count 选项
$ python hello.py World --count=3
Hello, World!
Hello, World!
Hello, World!

# 查看自动生成的帮助信息
$ uv run hello.py --help
Usage: hello.py [OPTIONS] NAME

  一个向 NAME 问好的简单程序。

Options:
  --count INTEGER  重复问候的次数。
  --help           Show this message and exit.
```

## Example:

我们来构建一个示例应用程序，该程序将随机内容打印到控制台。其中数据是从[维基百科API](https://www.mediawiki.org/wiki/REST_API)检索的。
初始化项目：`uv init modern_python --lib -p 3.11`

下载依赖项：`uv add requests`

接下来，将文件 `src/modern_python/console.py` 替换为如下所示的源代码。

```python
# src/modern_python/console.py
import textwrap

import click
import requests

from modern_python import __version__


API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@click.command()
@click.version_option(version=__version__)
def main():
    """The modern Python project."""
    with requests.get(API_URL) as response:
        response.raise_for_status()
        data = response.json()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))

if __name__ == "__main__":
    main()
```
现在你的文件结构应该是这样的：

```
modern_python/
├── .git
├── src/                # 源代码目录
│   └── modern_python/  # 你的包
│       ├── __init__.py
│       └── py.typed
├── .gitignore
├── .python-version
├── pyproject.toml    # 项目配置文件
└── README.md         # 项目说明
```

首先来看模块顶部的导入语句。

```python
import textwrap

import click
import requests

from modern_python import __version__
```

标准库中的 [textwrap](https://docs.python.org/3/library/textwrap.html) 模块允许你在向控制台打印文本时换行。我们还导入了新安装的 `requests` 包。空行用于按照 [PEP 8](https://www.python.org/dev/peps/pep-0008/#imports) 的建议对导入进行分组（标准库–第三方包–本地导入）。

```python
API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
```

`API_URL` 常量指向英语维基百科的 [REST API](https://restfulapi.net/)，或者更具体地说，指向其 `/page/random/summary` 端点，该端点会返回随机维基百科文章的摘要。

```python
with requests.get(API_URL) as response:
    response.raise_for_status()
    data = response.json()
```

在 `main` 函数的主体中，`requests.get` 调用向维基百科 API 发送一个 [HTTP GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) 请求。`with` 语句确保在块结束时关闭 HTTP 连接。在查看响应体之前，我们检查 HTTP 状态码，如果它表示错误则抛出异常，程序结束。否则，响应体包含 [JSON](https://www.json.org/) 格式的资源数据，可以使用 `response.json()` 方法访问。

```python
title = data["title"]
extract = data["extract"]
```

我们只对 `title` 和 `extract` 属性感兴趣，它们分别包含维基百科页面的标题和简短的纯文本摘录。

```python
click.secho(title, fg="green")
click.echo(textwrap.fill(extract))
```

最后，我们使用 `click.echo` 和 `click.secho` 函数将标题和摘录打印到控制台。后者函数允许你使用 `fg` 关键字属性指定颜色。`textwrap.fill` 函数将 `extract` 中的文本换行，使每行最多 70 个字符。

```bash
$ uv run src/modern_python/console.py

Jägersbleeker Teich
The Jägersbleeker Teich in the Harz Mountains of central Germany is a
storage pond near the town of Clausthal-Zellerfeld in the county of
Goslar in Lower Saxony. It is one of the Upper Harz Ponds that were
created for the mining industry.
```