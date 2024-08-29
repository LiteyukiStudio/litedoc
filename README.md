# liteyuki-autodoc

## 为你的Python库模块生成清晰的markdown文档

### 功能：i18n支持，多风格注释支持，多主题支持

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
-c|--contain-top    #是否包含顶部文件夹信息，即在输出目录再套一层module_path的basedir
```
在输出的目录下markdown文档是以模块原有的目录结构生成的，可以直接把输出内容放到目前主流的文档框架项目中，如VuePress，VitePress等，如果想优化用户体验，还可启用动态侧边栏

## 代码编写建议
- 在编写库的时候，尽量写上标准的注释，这样对用户和自己都有好处
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