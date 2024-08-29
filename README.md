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

### 