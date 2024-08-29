---
title: litedoc.docstring.docstring
---
### **class** `Attr(BaseModel)`
### **class** `Args(BaseModel)`
### **class** `Return(BaseModel)`
### **class** `Exception_(BaseModel)`
### **class** `Raise(BaseModel)`
### **class** `Example(BaseModel)`
### **class** `Docstring(BaseModel)`
### ***method*** `add_desc(self, desc: str)`


<details>
<summary> <b>Source code</b> </summary>

```python
def add_desc(self, desc: str):
    if self.desc == '':
        self.desc = desc
    else:
        self.desc += '\n' + desc
```
</details>

### ***method*** `add_arg(self, name: str, type_: str = '', desc: str = '')`


<details>
<summary> <b>Source code</b> </summary>

```python
def add_arg(self, name: str, type_: str='', desc: str=''):
    self.args.append(Args(name=name, type=type_, desc=desc))
```
</details>

### ***method*** `add_attrs(self, name: str, type_: str = '', desc: str = '')`


<details>
<summary> <b>Source code</b> </summary>

```python
def add_attrs(self, name: str, type_: str='', desc: str=''):
    self.attrs.append(Attr(name=name, type=type_, desc=desc))
```
</details>

### ***method*** `add_return(self, desc: str = '')`


<details>
<summary> <b>Source code</b> </summary>

```python
def add_return(self, desc: str=''):
    self.return_ = Return(desc=desc)
```
</details>

### ***method*** `add_raise(self, name: str, desc: str = '')`


<details>
<summary> <b>Source code</b> </summary>

```python
def add_raise(self, name: str, desc: str=''):
    self.raise_.append(Exception_(name=name, desc=desc))
```
</details>

### ***method*** `add_example(self, desc: str = '', input_: str = '', output: str = '')`


<details>
<summary> <b>Source code</b> </summary>

```python
def add_example(self, desc: str='', input_: str='', output: str=''):
    self.example.append(Example(desc=desc, input=input_, output=output))
```
</details>

### ***method*** `reduction(self, style: str = 'google') -> str`



**Description**: 通过解析结果还原docstring

**Arguments**:
> - style: docstring风格  


<details>
<summary> <b>Source code</b> </summary>

```python
def reduction(self, style: str='google') -> str:
    """
        通过解析结果还原docstring
        Args:
            style: docstring风格
        Returns:

        """
    ret = ''
    if style == 'google':
        ret += self.desc + '\n'
        if self.args:
            ret += 'Args:\n'
            for arg in self.args:
                ret += f'    {arg.name}: {arg.type}\n        {arg.desc}\n'
        if self.attrs:
            ret += 'Attributes:\n'
            for attr in self.attrs:
                ret += f'    {attr.name}: {attr.type}\n        {attr.desc}\n'
        if self.return_:
            ret += 'Returns:\n'
            ret += f'    {self.return_.desc}\n'
        if self.raise_:
            ret += 'Raises:\n'
            for exception in self.raise_:
                ret += f'    {exception.name}\n        {exception.desc}\n'
        if self.example:
            ret += 'Examples:\n'
            for example in self.example:
                ret += f'    {example.desc}\n        Input: {example.input}\n        Output: {example.output}\n'
    return ret
```
</details>

### ***method*** `markdown(self, lang: str, indent: int = 4, is_classmethod: bool = False) -> str`



**Description**: 生成markdown文档

**Arguments**:
> - is_classmethod:   
> - lang:   
> - indent:   


<details>
<summary> <b>Source code</b> </summary>

```python
def markdown(self, lang: str, indent: int=4, is_classmethod: bool=False) -> str:
    """
        生成markdown文档
        Args:
            is_classmethod:
            lang:
            indent:

        Returns:

        """
    PREFIX = '' * indent
    ret = ''
    if self.desc:
        ret += PREFIX + f"\n**{get_text(lang, 'desc')}**: {self.desc}\n"
    if self.args:
        ret += PREFIX + f"\n**{get_text(lang, 'docstring.args')}**:\n"
        for arg in self.args:
            ret += PREFIX + f'> - {arg.name}: {arg.type}  {arg.desc}\n'
    if self.attrs:
        ret += PREFIX + f"\n**{get_text(lang, 'docstring.attrs')}**:\n"
        for attr in self.attrs:
            ret += PREFIX + f'> - {attr.name}: {attr.type}  {attr.desc}\n'
    if self.return_ is not None:
        ret += PREFIX + f"\n**{get_text(lang, 'docstring.return')}**: {self.return_.desc}\n"
    if self.raise_:
        ret += PREFIX + f"\n**{get_text(lang, 'docstring.raises')}**:\n"
        for exception in self.raise_:
            ret += PREFIX + f'> - {exception.name}  {exception.desc}\n'
    if self.example:
        ret += PREFIX + f"\n**{get_text(lang, 'docstring.example')}**:\n"
        for example in self.example:
            ret += PREFIX + f"  - {example.desc}\n>        **{get_text(lang, 'docs.input')}**: {example.input}\n>        **{get_text(lang, 'docs.output')}**: {example.output}\n"
    return ret
```
</details>

