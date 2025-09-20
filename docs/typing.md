# Typing
本章，我将讨论如何将类型注解和类型检查添加到的项目中。
## 类型注解和类型检查器
类型注解首次在Python 3.5中引入，是一种为函数和变量添加类型注解的方法。结合理解它们的工具，它们可以使你的程序更容易理解、调试和维护。以下是两个类型注解的简单示例：
```py
# This is a variable holding an integer.
answer: int = 42


# This is a function which accepts and returns an integer.
def increment(number: int) -> int:
    return number + 1
```
Python 的运行时环境**并不强制执行类型注解**。作为典型的动态类型语言，Python 仅在代码实际执行阶段才会验证数据类型，且遵循“鸭子类型”（Duck Typing）原则——即“若一个对象走起路来像鸭子、叫起来也像鸭子，那它就可以被当作鸭子”，判断依据是对象的行为而非显式的类型声明。

```{note}
静态的类型注解，在运行代码时并不效果，
`a:int = 1.2`
python解释器并不会报错，即类型注解仅能作为文档使用，后续会介绍可以在运行时验证类型的工具。
```


与之形成鲜明对比的是静态类型检查：这类工具可借助代码中的**类型注解**与自身的**类型推断能力**，在不执行程序的前提下验证类型正确性。这种“提前检查”的特性，能帮助开发者发现许多运行时才会暴露、且易被人工忽略的潜在错误，大幅提升代码健壮性。

事实上，类型注解的引入直接推动了一代 Python 静态类型检查器的诞生：
- **mypy** 堪称该领域的先驱，其开发过程中甚至有多位 Python 核心开发者参与，奠定了静态类型检查在 Python 生态中的基础；
- 科技巨头也纷纷推出专属工具：谷歌开发了 **pytype**，Facebook 推出了 **pyre**，微软则贡献了 **pyright**；
- 主流 IDE 同样集成了该功能，例如 PyCharm 就自带了内置的静态类型检查器。

值得一提的是，VSCode 与 PyCharm 这两款常用开发工具均已原生支持静态类型检查，开发者可直接在日常编码中体验其作用。因此，本文不再对静态类型检查器的技术细节展开过多解释。

## 为modern_python添加类型注解
给这个包添加一些类型注解，从 console.main 开始。不要被它应用的装饰器分散注意力：这是一个简单的函数，接受一个字符串，并返回 None：
```py
# src/modern_python/console.py
def main(language: str) -> None: ...
```
在维基百科模块中，API_URL常量是一个字符串：
```py
API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"
```
`wikipedia.random_page` 接受一个可选参数`str`:
```py
# src/modern_python/wikipedia.py
def random_page(language: str = "en"): ...
```
`wikipedia.random_page`函数返回从维基百科API接收到的JSON对象。在Python中，使用内置类型如`dict`、`list`、`str`和`int`来表示JSON对象。由于JSON对象的递归性质，它们的类型在Python中仍然难以表达，通常被指定为Any：
```py
# src/modern_python/wikipedia.py
from typing import Any


def random_page(language: str = "en") -> Any: ...
```
`Any` 可以容纳任意类型的数据，但对外表现时，却能完全模拟所容纳数据的实际类型特性。作为 Python 类型系统中权限最高的注解，`Any` 可用于标注变量、函数参数或返回值，赋予代码最大的灵活性。

这一点与 `object` 类型形成鲜明对比：尽管object同样能存储任意类型的值（毕竟 Python 中所有类型都默认继承自object），但它仅支持所有类型共有的 “最小接口”—— 比如 `__eq__` （判断相等）、 `__hash__` （计算哈希值）等基础方法，无法直接调用特定类型的专属操作（如字符串的.split()、列表的.append()）。
## 使用pydantic进行数据验证
我们不应满足于返回 `Any`，因为我们明确知道维基百科 API 的 JSON 结构。虽然API 本身并非类型保证，但在运行时验证接收到的数据，我们能将其转化为可靠的类型保证。这恰好也展示了如何在运行时运用类型注解。

第一步是定义验证的目标类型。目前，该函数应该返回一个包含多个键的字典，其中我们只对`title`和`extract`感兴趣。但你的程序可以比在字典上操作做得更好：使用`pydantic`，你可以以简洁直接的方式定义一个功能齐全的数据类型。让我们为我们的应用程序定义一个`wikipedia.Page`类型：
下载`pydantic`:
```bash
$ uv add pydantic
```
### 如何使用pydantic

#### 创建模型
Pydantic 的核心是 BaseModel 类，通过继承它可以创建数据模型：
```python
from pydantic import BaseModel

# 定义一个数据模型
class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

# 创建模型实例
user = User(
    id=1,
    name="Alice",
    age=30,
    email="alice@example.com"
)

# 访问模型字段
print(user.name)  # 输出: Alice
print(user.dict())  # 转换为字典
```
#### 数据验证
Pydantic 会自动验证输入数据是否符合模型定义的类型和约束：
```python
# 尝试传入错误类型的数据
try:
    User(
        id="not_an_integer",  # 错误类型：应为int
        name="Bob",
        age=25,
        email="bob@example.com"
    )
except Exception as e:
    print(e)  # 会抛出验证错误
```
#### 添加验证约束
可以使用 Pydantic 提供的装饰器和字段约束来添加更复杂的验证规则：
```py
from pydantic import BaseModel, EmailStr, Field, validator

class User(BaseModel):
    id: int = Field(..., gt=0)  # id必须大于0
    name: str = Field(..., min_length=2, max_length=50)  # 名字长度限制
    age: int = Field(..., ge=0, le=120)  # 年龄范围限制
    email: EmailStr  # 自动验证邮箱格式

    # 自定义验证器
    @validator('name')
    def name_must_not_contain_numbers(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError('姓名不能包含数字')
        return v

# 测试验证规则
user = User(id=1, name="Alice", age=30, email="alice@example.com")  # 有效
# user = User(id=0, name="A", age=150, email="invalid-email")  # 无效，会抛出错误
```
#### 从字典或json加载数据
```py
# 从字典加载
user_data = {
    "id": 2,
    "name": "Bob",
    "age": 25,
    "email": "bob@example.com"
}
user = User.model_validate(user_json)

# 从JSON字符串加载
import json
user_json = '{"id": 3, "name": "Charlie", "age": 35, "email": "charlie@example.com"}'
user=User.model_validate_json(user_json)
```
### 添加到modern_python中
```py
# src/modern_python/wikipedia.py
from pydantic import BaseModel

class Page(BaseModel):
    title: str
    extract: str
```
我们将从这个wikipedia.random_page返回这个数据类型：
```py
# src/modern_python/wikipedia.py
def random_page(language: str = "en") -> Page: ...
```
数据类型对代码库的结构有积极的影响。通过对`wikipedia.Page`的适配，代码变成了清晰简洁的三行代码：
```py
# src/modern_python/console.py
def main(language: str) -> None:
    """The modern Python project."""
    page = wikipedia.random_page(language=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
```
当然，我们仍然缺少创建`wikipedia.Page`对象的实际代码。让我们从一个测试案例开始，执行运行时类型检查：
```py
# tests/test_wikipedia.py
def test_random_page_returns_page(mock_requests_get):
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)
```
转换为wikipedia.Page对象:
```py

def random_page(language: str = "en") -> Page:
    url = API_URL.format(language=language)
    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            return Page.model_validate(response.json())
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
```
类似第2章中处理请求错误那样,我们也需要处理验证错误，将它们转换为`ClickException`。例如，假设由于一个虚构的错误，维基百科响应体返回“null”而不是实际资源。

我们可以通过配置`requests.get`模拟来产生`None`作为JSON对象，并使用`pytest.raises`来检查正确的异常:
```py
# tests/test_wikipedia.py
def test_random_page_handles_validation_errors(mock_requests_get) -> None:
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()
```
向异常处理子句中添加 `pydantic.ValidationError`：
```py
# src/modern_python/wikipedia.py
except (requests.RequestException, pydantic.ValidationError) as error:
```
这是带有类型注解和验证的维基百科模块：
```py
# src/modern_python/wikipedia.py
import click
import pydantic
import requests
from pydantic import BaseModel

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(HTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    )
}


class Page(BaseModel):
    title: str
    extract: str


def random_page(language: str = "en") -> Page:
    url = API_URL.format(language=language)
    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            return Page.model_validate(response.json())
    except (requests.RequestException, pydantic.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
```
## 运行时类型检查
由于 python 在运行时的检查为鸭子类型，并不会真正的进行检查类型，在这里我们将会讨论如何让python在运行时进行类型检查。

这里的类型检查有两种：

- 在测试时检查，即只在 pytest 运行时激活，在实际的生产环境中，代码依然会运行，并且如果遇到类型不匹配的问题，它会像原来一样抛出错误（或者更糟，静默地产生错误数据）。

- 在生产环境检查，即在实际的生产环境中，如果遇到类型不匹配的问题，它会抛出错误，停止运行。

当然，在生产环境中运行会导致一定程度上的性能问题，这引出了一个核心的软件工程决策：我们应该在多大程度上进行运行时检查？
这个问题的答案不是非黑即白的，而是一个关于 性能、安全性和开发哲学的权衡。
### 测试时类型检查
在测试环境中捕获类型错误，可以帮助开发者弄清楚函数参数传递时的类型，并且可以帮助测试人员写更好的测试用例。

下载 `typeguard`:
```bash
$ uv add typeguard --dev
```
```py
# noxfile.py
package = "modern_python"


@nox.session(python=["3.11"])
def typeguard(session):
    args = session.posargs or ["-m", "not e2e"]
    session.run("uv", "sync", external=True)
    session.run("pytest", f"--typeguard-packages={package}", *args)
```
运行：
```bash
$ uv run nox -rs typeguard
```

### 生产环境中类型检查
pydantic提供了在生产环境中类型检查的方式：
```py
from pydantic import validate_call, ValidationError

@validate_call
def process_user_data(user_id: int, name: str, age: int):
    """
    一个用 pydantic 装饰器保护的函数。
    """
    return f"Processed user {user_id} ({name}), age {age}."

# --- 非法调用 ---
try:
    # "one-two-three" 无法被解析为整数
    process_user_data(user_id="one-two-three", name="Charlie", age=25)
except ValidationError as e:
    print("\nCaught a validation error:")
    print(e)
    # 输出会非常清晰地告诉你哪个参数出了什么问题
    # Caught a validation error:
    # 1 validation error for process_user_data
    # user_id
    #   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='one-two-three', input_type=str]
```
这样，虽然开销增加，但是更安全。

## 使用Ruff进行类型警告
配置`pyproject.toml`以启用由插件生成的警告（ANN即annotations）：
```toml
#pyproject.toml
[tool.ruff]
select = ["C","E","F","W","I","B","B9","S","ANN"]
```
运行
```bash
$ uv run nox -rs lint
```
其会输出关于Nox会话和测试套件中缺少类型注解的警告。可以使用`per-file-ignores`选项来禁用这些位置的警告：
```toml
#pyproject.toml
[tool.ruff]
per-file-ignores = { "tests/*" = ["ANN","S101"] }
```
## 为Nox Session添加类型注解
在本节中，将展示如何为Nox session添加类型注解。如果已禁用Nox会话的类型覆盖警告（ANN），请为本节的目的重新启用它们。

Nox session的核心类型是nox.sessions.Session，它是session函数唯一的参数。这些函数的返回值是None。按照以下方式注解您的会话函数：
```py
# noxfile.py
from nox.sessions import Session

def tests(session: Session) -> None: ...

#以此类推
```
% missing from source
## 为tests添加类型注解
在本节中，将展示如何向tests添加类型注解。如果已禁用tests的类型覆盖率警告（ANN），本节需要重新启用它们。

Pytest中的测试函数使用参数(parameter)来声明它们使用的`test fixture`。你不需要指定`test fixture`的类型，而是指定`test fixture`提供给测试函数的值的类型。例如，`mock_requests_get`返回一个标准的mock对象，类型为`unittest.mock.Mock`。（实际类型是`unittest.mock.MagicMock`，但这里使用更通用的类型来注释测试函数。）我们从注释`test_wikipedia.py`中的测试函数开始：

```py
# tests/test_wikipedia.py
from unittest.mock import Mock


def test_random_page_uses_given_language(mock_requests_get: Mock) -> None: ...
# 以此类推
```
下面，注释一下`mock_requests_get`本身。这个函数的返回类型为`unittest.mock.Mock`。该函数接受一个参数，即pytest-mock中的`mocker fixture`，其类型为`pytest_mock.MockFixture`：
```py
# tests/conftest.py
from unittest.mock import Mock

from pytest_mock import MockFixture


def mock_requests_get(mocker: MockFixture) -> Mock: ...
```
在`tests/test_console.py`中使用相同的类型签名：
```py
# tests/test_console.py
from unittest.mock import Mock

from pytest_mock import MockFixture


def mock_wikipedia_random_page(mocker: MockFixture) -> Mock: ...
```
`tests/test_console.py`中还定义了一个返回click.testing.CliRunner的简单 fixture：
```py
# tests/test_console.py
from click.testing import CliRunner


def runner() -> CliRunner: ...
```
关于`pytest_configure`。该函数接受一个Pytest配置对象作为其唯一参数。但该对象类型（目前）不是Pytest的公共接口的一部分。可以选择使用Any或者深入Pytest内部导入`_pytest.config.Config`。我们选择后者：
```py
# tests/conftest.py
from _pytest.config import Config

def pytest_configure(config: Config) -> None: ...
```


我们探索Python类型系统的旅程结束。类型注解使你的程序更容易理解、调试和维护。静态类型检查器使用类型注解和类型推断来验证程序的类型正确性，而无需执行它，帮助你发现许多否则可能被忽视的bug。