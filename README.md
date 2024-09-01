# Litedoc

### 为你的Python库模块生成结构化的markdown文档

功能：

- i18n多语言支持
- frontmatter支持
- 可选注释风格
- 可选主题支持
- 支持对象带有相对链接跳转

## 安装

```shell
pip install litedoc
```

## 使用方法

```shell
litedoc <your_module_path> -o|--output <output_path>
```

#### 详细命令参数

```shell
-o|--output: "doc-output"  输出路径，默认为doc-output
-l|--lang:   "zh-Hans"  语言，支持en, zh-Hans，zh-Hant，ja，默认zh-Hans
-t|--theme: "vitepress"  主题，支持vitepress, vuepress, 默认vitepress
-s|--style: "google"  风格，支持google, numpy, reStructuredText, 默认google，但目前只实现了google，欢迎PR
-f|--frontmatter:  #是否生成frontmatter，即文档的元数据，如title, description等, 格式为key1=value1,key2=value2, 空格用%20代替
-b|--base-url: ""  基础URL，用于生成文档中的跳转链接，通常指向Github仓库下的包路径根目录，
    如果为空字符串将不生成，末尾带/，例如https://github.com/snowykami/mbcp/tree/main/mbcp/
-fd|--function-define: "func" 函数定义风格，输出的markdown显示的函数定义，Python原生为def
-md|--method-define: "method" 方法定义风格，输出的markdown显示的方法定义
-cd|--class-define: "class" 类定义风格，输出的markdown显示的类定义
-vd|--var-define: "var" 变量定义风格，输出的markdown显示的变量定义
-ad|--attr-define: "attr" 属性定义风格，输出的markdown显示的属性定义
-c|--contain-top    # 是否包含顶部文件夹信息，即在输出目录再套一层module_path的basedir
-cs|--create-same  # 是否在包下创建和包名相同的md文件储存__init__文件的内容(有同名文件时请勿使用，例如client/client.py)
```

在输出的目录下markdown文档是以模块原有的目录结构生成的，可以直接把输出内容放到目前主流的文档框架项目中，如VuePress，VitePress等，如果想优化用户体验，还可启用动态侧边栏

## 代码编写建议

- 在编写函数的时候，请写上标准的注释，这样对用户和自己都有好处
    - 代码遵循相应的PEP规范，如PEP8，PEP257等
    - 可在文件头部使用`"""`包裹的注释写上文件的说明，会被自动放到文档的顶部
    - 请不要在注释中使用特殊字符例如换行符`\n`，如有请使用`\\n`转义或使用原始字符串`r"""string content"""`，否则会导致解析错误
    - 可以在注释中编写一些你所使用的文档框架支持的markdown增强语法，如表格，容器等，可增强用户阅读体验
    - 可在参数注释中使用markdown的链接语法和哈希路由，如```p ([`Point3`](./point#class-point3))```: 点，以支持跳转到其他文档的链接
- 生成器默认不处理"私有"变量和函数，即以`_`开头的变量和函数（尽管Python没有真正的私有变量），也默认不处理没有注释的变量
- 如果你不想展示某个函数和变量，可以在函数文档字串任意处加上`@litedoc-hide`
- 变量注释支持在同一行内使用`#`添加的注释，也支持在下一行使用`"""注释内容"""`添加的注释
- 可在文件顶部的注释顶部添加frontmatter，如`---\ntitle: liteyuki\n---`，会被自动追加更新到传入的frontmatter中

## 自动化构建(Github workflows)

- 如果你了解并正在使用github workflow自动构建文档，那么可以把生成API markdown的步骤也添加进去，无需手动生成文档。
- 需在构建静态页面之前生成API markdown

```yaml
...
- name: Set up Python
  uses: actions/setup-python@v2
  with:
    python-version: '3.10'


- name: Build API markdown
  run: |-
    python -m pip install litedoc
    litedoc <your_module> -o docs/dev/api -l zh-Hans -t vuepress
    litedoc <your_module> -o docs/en/dev/api -l en -t vuepress'   # 请自行更改这部分
    # ...可以添加更多语言
...
# build your static page
```

## 示例项目

- [轻雪文档](https://bot.liteyuki.icu)

- [MBCP Docs](https://mbcp.sfkm.me)

## 其他

### Liteyuki Docstring
Liteyuki Docstring是Google风格docstring的超集，可以更好地配合Litedoc生成更美观的文档
支持
- `@litedoc-hide` 隐藏函数或变量
- 链接跳转（需文档框架支持）
- 更多的markdown语法

示例
- 以下是一个Google docstring示例
```python
def add(a: int, b: int) -> int:
    """
    This is a function to add two numbers
    Args:
        a: The first number
        b: The second number
    Returns:
        The sum of a and b
    """
    return a + b
```
- 以下是一个Liteyuki docstring示例
```python
def add(a: int, b: int) -> int:
    """
    This is a function to add two numbers
    Args:
        a ([`int`](https%3A//docs.python.org/3/library/functions.html#int)): The first number
        b (`int`) : The second number
    Returns:
        [`int`](https%3A//docs.python.org/3/library/functions.html#int): The sum of a and b
    @litedoc-hide
    """
    return a + b
```
- 还可以在模块内部使用相对链接和哈希路由跳转到其他文档
```python
def add(a: int, b: int) -> int:
    """
    This is a function to add two numbers
    Args:
        a ([`int`](./int#class-int)): The first number
        b (`int`) : The second number
    Returns:
        [`int`](./int#class-int): The sum of a and b
    """
    return a + b
```
以上写法不影响主流编辑器的Google docstring解析，但可以更好地配合Litedoc生成更美观的文档

### Python函数参数

- 一个Python函数可以有五种传参方式：仅位置参数(posonlyargs)、位置参数(args)、可变参数(vararg)、仅关键字参数(kwonlyargs)及关键字参数(kwarg)。以下是一个函数的参数的例子。

<details>
<summary>代码示例</summary>

```python
def example1(poa1, poa2, /, a1, a2, *args, kwoa1, kwoa2, **kwargs):
    """
    这是一个示例函数
    Args:
        poa1: 仅位置参数1
        poa2: 仅位置参数2，此后的/用于分隔仅位置参数，在/之前的只能使用位置参数传参
        a1: 位置参数3
        a2: 位置参数4
        args: 可变参数，在此之后定义的形参需要使用关键字传参
        kwoa1: 关键字参数1
        kwoa2: 关键字参数2
        kwargs: 关键字可变参数
    """

example1(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, kwoa1=11, kwoa2=12, kwoa3=13, kwoa4=14)
"""
传参结果
Posonlyargs:
    pos1: 1
    pos2: 2
Args:
    a1: 3
    a2: 4
Vararg:
    args: (5, 6, 7, 8, 9, 10)
Kwonlyargs:
    kwoa1: 11
    kwoa2: 12
Kwarg:
    kwargs: {'kwoa3': 13, 'kwoa4': 14}
"""


def example2(poa1, poa2, /, a1, a2, *, kwoa1, kwoa2):
    """
    这是一个示例函数
    Args:
        poa1: 仅位置参数1
        poa2: 仅位置参数2，此后的/用于分隔仅位置参数，在/之前的只能使用位置参数传参
        a1: 位置参数3
        a2: 位置参数4
        kwoa1: 关键字参数1
        kwoa2: 关键字参数2，此后的*用于分隔关键字参数，在*之后的只能使用关键字传参
    """
    pass


example2(1, 2, 3, 4, kwoa1=5, kwoa2=6)
"""
传参结果
Posonlyargs:
    pos1: 1
    pos2: 2
Args:
    a1: 3
    a2: 4
Kwonlyargs:
    kwoa1: 5
    kwoa2: 6
"""
```

</details>


### 相关PEP

- [PEP 3102 - Keyword-Only Arguments](https://www.python.org/dev/peps/pep-3102/)
- [PEP 570 - Python Positional-Only Parameters](https://www.python.org/dev/peps/pep-0570/)
- [PEP 3107 - Function Annotations](https://www.python.org/dev/peps/pep-3107/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)

