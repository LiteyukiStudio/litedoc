---
title: litedoc.syntax.node
---
### **class** `TypeHint`
### **class** `AssignNode(BaseModel)`
### **class** `ArgNode(BaseModel)`
### **class** `AttrNode(BaseModel)`
### **class** `ImportNode(BaseModel)`
### **class** `ConstantNode(BaseModel)`
### **class** `FunctionNode(BaseModel)`
### ***method*** `is_private(self)`



**Description**: Check if the function or method is private.

**Return**: bool: True if the function or method is private, False otherwise.


<details>
<summary> <b>Source code</b> </summary>

```python
def is_private(self):
    """
        Check if the function or method is private.
        Returns:
            bool: True if the function or method is private, False otherwise.
        """
    return self.name.startswith('_')
```
</details>

### ***method*** `is_builtin(self)`



**Description**: Check if the function or method is a builtin function or method.

**Return**: bool: True if the function or method is a builtin function or method, False otherwise.


<details>
<summary> <b>Source code</b> </summary>

```python
def is_builtin(self):
    """
        Check if the function or method is a builtin function or method.
        Returns:
            bool: True if the function or method is a builtin function or method, False otherwise.
        """
    return self.name.startswith('__') and self.name.endswith('__')
```
</details>

### ***method*** `markdown(self, lang: str, indent: int = 0) -> str`



**Arguments**:
> - indent: int  
> - The number of spaces to indent the markdown.:   
> - lang: str  
> - The language of the:   

**Return**: markdown style document


<details>
<summary> <b>Source code</b> </summary>

```python
def markdown(self, lang: str, indent: int=0) -> str:
    """
        Args:
            indent: int
                The number of spaces to indent the markdown.
            lang: str
                The language of the
        Returns:
            markdown style document
        """
    self.complete_default_args()
    PREFIX = '' * indent
    func_type = 'func' if not self.is_classmethod else 'method'
    md = ''
    if len(self.decorators) > 0:
        for decorator in self.decorators:
            md += PREFIX + f'### `@{decorator}`\n'
    if self.is_async:
        md += PREFIX + f'### ***async {func_type}*** '
    else:
        md += PREFIX + f'### ***{func_type}*** '
    args: list[str] = []
    arg_i = 0
    if len(self.posonlyargs) > 0:
        for arg in self.posonlyargs:
            arg_text = f'{arg.name}'
            if arg.type != TypeHint.NO_TYPEHINT:
                arg_text += f': {arg.type}'
            arg_default = self.defaults[arg_i].value
            if arg_default != TypeHint.NO_DEFAULT:
                arg_text += f' = {arg_default}'
            args.append(arg_text)
            arg_i += 1
        args.append('/')
    for arg in self.args:
        arg_text = f'{arg.name}'
        if arg.type != TypeHint.NO_TYPEHINT:
            arg_text += f': {arg.type}'
        arg_default = self.defaults[arg_i].value
        if arg_default != TypeHint.NO_DEFAULT:
            arg_text += f' = {arg_default}'
        args.append(arg_text)
        arg_i += 1
    if len(self.kwonlyargs) > 0:
        args.append('*')
        for arg, kw_default in zip(self.kwonlyargs, self.kw_defaults):
            arg_text = f'{arg.name}'
            if arg.type != TypeHint.NO_TYPEHINT:
                arg_text += f': {arg.type}'
            if kw_default.value != TypeHint.NO_DEFAULT:
                arg_text += f' = {kw_default.value}'
            args.append(arg_text)
    '魔法方法'
    if self.name in self.magic_methods:
        if len(args) == 2:
            md += f'`{args[0]} {self.magic_methods[self.name]} {args[1]}'
        elif len(args) == 1:
            md += f'`{self.magic_methods[self.name]} {args[0]}'
        if self.return_ != TypeHint.NO_RETURN:
            md += f' => {self.return_}'
    else:
        md += f'`{self.name}('
        md += ', '.join(args) + ')'
        if self.return_ != TypeHint.NO_RETURN:
            md += f' -> {self.return_}'
    md += '`\n\n'
    '此处预留docstring'
    if self.docs is not None:
        md += f'\n{self.docs.markdown(lang, indent)}\n'
    else:
        pass
    md += PREFIX + f"\n<details>\n<summary> <b>{get_text(lang, 'src')}</b> </summary>\n\n```python\n{self.src}\n```\n</details>\n\n"
    return md
```
</details>

### ***method*** `complete_default_args(self)`



**Description**: 补全位置参数默认值，用无默认值插入


<details>
<summary> <b>Source code</b> </summary>

```python
def complete_default_args(self):
    """
        补全位置参数默认值，用无默认值插入
        Returns:

        """
    num = len(self.args) + len(self.posonlyargs) - len(self.defaults)
    self.defaults = [ConstantNode(value=TypeHint.NO_DEFAULT) for _ in range(num)] + self.defaults
```
</details>

### **class** `ClassNode(BaseModel)`
### ***method*** `markdown(self, lang: str) -> str`



**Arguments**:
> - lang: str  
> - The language of the:   

**Return**: markdown style document


<details>
<summary> <b>Source code</b> </summary>

```python
def markdown(self, lang: str) -> str:
    """
        返回类的markdown文档
        Args:
            lang: str
                The language of the
        Returns:
            markdown style document
        """
    hidden_methods = ['__str__', '__repr__']
    md = ''
    md += f'### **class** `{self.name}'
    if len(self.inherits) > 0:
        md += f"({', '.join([cls for cls in self.inherits])})"
    md += '`\n'
    for method in self.methods:
        if method.name in hidden_methods:
            continue
        md += method.markdown(lang, 2)
    for attr in self.attrs:
        if attr.type == TypeHint.NO_TYPEHINT:
            md += f'#### ***attr*** `{attr.name} = {attr.value}`\n\n'
        else:
            md += f'#### ***attr*** `{attr.name}: {attr.type} = {attr.value}`\n\n'
    return md
```
</details>

