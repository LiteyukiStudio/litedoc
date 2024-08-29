---
title: litedoc.style.markdown
---
### ***func*** `generate(parser: AstParser = None, lang: str = 'google') -> str`



**Description**: Generate markdown style document from ast
You can modify this function to generate markdown style that enjoys you

**Arguments**:
> - parser:   
> - lang: language  
> - frontmatter:   
> - style: style of docs  

**Return**: markdown style document


<details>
<summary> <b>Source code</b> </summary>

```python
def generate(parser: AstParser, lang: str, frontmatter: Optional[dict]=None, style: str='google') -> str:
    """
    Generate markdown style document from ast
    You can modify this function to generate markdown style that enjoys you
    Args:
        parser:
        lang: language
        frontmatter:
        style: style of docs
    Returns:
        markdown style document
    """
    if frontmatter is not None:
        md = '---\n'
        for k, v in frontmatter.items():
            md += f'{k}: {v}\n'
        md += '---\n'
    else:
        md = ''
    '遍历函数'
    for func in parser.functions:
        if func.name.startswith('_'):
            continue
        if func.docs is not None and litedoc_hide in func.docs.reduction():
            continue
        md += func.markdown(lang)
    '遍历类'
    for cls in parser.classes:
        md += cls.markdown(lang)
    '遍历变量'
    for var in parser.variables:
        if var.docs is not None and litedoc_hide not in var.docs:
            md += f'### ***var*** `{var.name} = {var.value}`\n\n'
            if var.type != TypeHint.NO_TYPEHINT:
                md += f"- **{get_text(lang, 'type')}**: `{var.type}`\n\n"
            md += f"- **{get_text(lang, 'desc')}**: {var.docs}\n\n"
    return md
```
</details>

