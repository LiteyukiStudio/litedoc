# liteyuki-autodoc

## 为你的Python模块生成markdown文档

### 支持i18n，Google Style，Numpy Style，reStructuredText Style(待支持)

### 安装

```shell
pip install litedoc
```

### 使用

```shell
python -m litedoc <your_module_path> -o|--output <output_path>
```

### 详细参数

```shell
-o|--output: "doc-output"  输出路径，默认为doc-output
-l|--lang:   "zh-Hans"  语言，支持en, zh-Hans，zh-Hant，ja等，默认zh-Hans
-t|--theme: "vitepress"  主题，支持vitepress, vuepress, 默认vitepress
-s|--style: "google"  风格，支持google, numpy, reStructuredText, 默认google，但目前只实现了google，欢迎PR
-c|--contain-top    #是否包含顶部文件夹信息，即在输出目录再套一层module_path的basedir
```

### 代码编写小提示
- 生成器默认不处理"私有"变量和函数，即以`_`开头的变量和函数（尽管Python没有真正的私有变量），也默认不处理没有类型注释的变量
- 如果你不想展示某个函数和变量，可以在函数文档字串任意处加上`@litedoc-hide`
- 变量注释支持在同一行内使用`#`添加的注释，也支持在下一行使用`"""注释内容"""`添加的注释

### 示例项目
- [轻雪文档](https://bot.liteyuki.icu)

- [MBCP Docs](https://mbcp.sfkm.me)