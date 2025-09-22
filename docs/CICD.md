# CI/CD

## Continuous integration using GitHub Actions
CI即持续集成(Continuous Integration)，CI帮助自动化将代码更改集成到项目中。当更改被推送到项目仓库时，CI服务器会验证其正确性，触发单元测试、代码检查器或类型检查器等工具。

Pull requests 是这个工作流程的重要基石部分。其允许你向仓库提出一系列更改的建议，例如特定的错误修复或新功能。当Pull requests被接受时，其更改会被合并到目标分支，通常是主分支。GitHub会显示通过CI的pull requests为绿色勾选，如果CI未通过，则显示红色叉号。这样，CI就充当了提交需要通过的关卡，才能进入主分支。
> 注意到，这里的pull requests和 git pull无关，pull requests是github自己的服务，不是git的服务,
> pull requests 译为合并请求，关于其操作视频，可以参考 [this](https://www.youtube.com/watch?v=nCKdihvneS0)

在CI方面，有很多选择。传统上，许多开源项目都采用了Travis CI。另一个流行的选择是微软的Azure Pipelines。在本指南中，我们使用GitHub自己的服务，GitHub Actions。

关于 github action的使用可以参考[视频](https://www.bilibili.com/video/BV1aT421y7Ar?vd_source=189ac0e5f555cc7d23863c9d75a86118)

通过将以下YAML文件添加到.github/workflows目录中来配置GitHub Actions：
```yaml
# .github/workflows/tests.yml
name: Tests
on: push
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v5
    - uses: actions/setup-python@v5
      with:
        python-version: 3.11
        architecture: x64
    - run: pip install nox==2025.5.1
    - run: pip install uv==0.8.17
    - run: nox
```
此文件定义了一个的流程。流程是一个自动化的过程，执行一系列步骤，这些步骤被组织成一个或多个作业。流程由事件触发，例如当有人向仓库推送提交，或者当有人创建拉取请求、问题或发布时。

上面的流程在每次向GitHub仓库推送时都会触发，并使用Nox执行测试。它被恰当地命名为“Tests”，由一个在Ubuntu镜像上运行的job组成。该作业执行五个步骤，使用官方GitHub Actions或调用shell命令：

1. 使用 actions/checkout 将当前仓库的代码拉取到运行工作流的虚拟环境中，让后续步骤可以访问和操作代码。
2. 使用 actions/setup-python 安装 Python 3.11。
3. 使用 pip 安装 Nox。
4. 使用 pip 安装 uv。
5. 使用 Nox 运行你的测试。

您可以在官方参考中了解更多关于工作流程语言及其支持的关键字。

在CI过程中使用的每个工具都固定在特定版本。这样做的原因是CI过程应该是可预测和确定的。
你可以使用工具的最新版本，但请明确说明。这会给您的项目带来更高的可审计性，能避免 CI 流程中出现 “偶尔失败、重试又突然成功” 的玄学问题。

在专门的pull requests中升级工具还可以让你调查升级的影响，而不是当新版本可用时破坏整个CI。

当前工作流程仅使用Python 3.11，但你可以所有支持的Python版本上测试你的项目。可以使用构建矩阵来实现这一点。构建矩阵允许你定义变量，例如操作系统或Python版本，并为它们指定多个值。job中可以引用这些变量，并为每个值实例化。

让我们为项目支持的 Python 版本（Python 3.11 和 3.12）定义一个构建矩阵。使用策略和矩阵关键字来定义一个包含 python-version 变量的构建矩阵，并使用语法 ${{ matrix.python-version }} 引用该变量：
```yaml
# .github/workflows/tests.yaml
name: Tests
on: push
jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    name: Python ${{ matrix.python-version }}
    steps:
    - uses: actions/checkout@v5
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        architecture: x64
    - run: pip install nox==2019.11.9
    - run: pip install poetry==1.0.5
    - run: nox
```


[![Tests](https://github.com/gilgamesh1111/modern-python/workflows/Tests/badge.svg)](https://github.com/gilgamesh1111/modern-python/actions?workflow=Tests)


(build)=
## `uv build`
在上传Python包之前，需要生成发行版包。这些是用户可以下载并安装到他们系统中的压缩归档文件。它们有两种类型：源代码（或sdist）归档和wheel格式的二进制包。`uv`支持使用`uv build`命令生成这两种包：

```bash
$ uv build
```

使用该命令后，将会打包`modern_python`的Python包，并将它们保存在`dist`目录中。

关于更细节的信息，请参考[此视频](https://www.bilibili.com/video/BV12NgLzhEKx?vd_source=189ac0e5f555cc7d23863c9d75a86118)。
## 将你的包上传到PyPI
