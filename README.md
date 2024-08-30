# Litedoc

### 为你的Python库模块生成结构化的markdown文档

功能：

- i18n多语言支持
- 可选注释风格
- 可选主题支持

## 安装

```shell
pip install litedoc
```

## 使用方法

```shell
python -m litedoc <your_module_path> -o|--output <output_path>
```

#### 详细命令参数

```shell
-o|--output: "doc-output"  输出路径，默认为doc-output
-l|--lang:   "zh-Hans"  语言，支持en, zh-Hans，zh-Hant，ja，默认zh-Hans
-t|--theme: "vitepress"  主题，支持vitepress, vuepress, 默认vitepress
-s|--style: "google"  风格，支持google, numpy, reStructuredText, 默认google，但目前只实现了google，欢迎PR
-f|--frontmatter:  #是否生成frontmatter，即文档的元数据，如title, description等, 格式为key1=value1,key2=value2, 空格用%20代替
-fd|--function_define: "func" 函数定义风格，输出的markdown显示的函数定义，Python原生为def
-md|--method_define: "method" 方法定义风格，输出的markdown显示的方法定义
-cd|--class_define: "class" 类定义风格，输出的markdown显示的类定义
-vd|--var_define: "var" 变量定义风格，输出的markdown显示的变量定义
-ad|--attr_define: "attr" 属性定义风格，输出的markdown显示的属性定义
-c|--contain-top    #是否包含顶部文件夹信息，即在输出目录再套一层module_path的basedir
```

在输出的目录下markdown文档是以模块原有的目录结构生成的，可以直接把输出内容放到目前主流的文档框架项目中，如VuePress，VitePress等，如果想优化用户体验，还可启用动态侧边栏

## 代码编写建议

- 在编写函数的时候，请写上标准的注释，这样对用户和自己都有好处
    - 代码遵循相应的PEP规范，如PEP8，PEP257等
    - 可在文件头部使用`"""`包裹的注释写上文件的说明，会被自动放到文档的顶部
    - 请不要在注释中使用特殊字符例如换行符`\n`，如有请使用`\\n`转义或使用原始字符串`r"""string content"""`，否则会导致解析错误
    - 可以在注释中编写一些你所使用的文档框架支持的markdown增强语法，如表格，容器等，可增强用户阅读体验
- 生成器默认不处理"私有"变量和函数，即以`_`开头的变量和函数（尽管Python没有真正的私有变量），也默认不处理没有注释的变量
- 如果你不想展示某个函数和变量，可以在函数文档字串任意处加上`@litedoc-hide`
- 变量注释支持在同一行内使用`#`添加的注释，也支持在下一行使用`"""注释内容"""`添加的注释

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
    python -m litedoc <your_module> -o docs/dev/api -l zh-Hans -t vuepress
    python -m litedoc <your_module> -o docs/en/dev/api -l en -t vuepress'   # 请自行更改这部分
...
# build your static page
```

## 示例项目

- [轻雪文档](https://bot.liteyuki.icu)

- [MBCP Docs](https://mbcp.sfkm.me)

## 其他

### 函数参数

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

