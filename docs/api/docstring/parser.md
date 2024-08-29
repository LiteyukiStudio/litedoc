---
title: litedoc.docstring.parser
---
### ***func*** `parse(docstring: str = 'google', parser: str = 4) -> Docstring`


<details>
<summary> <b>Source code</b> </summary>

```python
def parse(docstring: str, parser: str='google', indent: int=4) -> Docstring:
    if parser == 'google':
        return GoogleDocstringParser(docstring, indent).parse()
    else:
        raise ValueError(f'Unknown parser: {parser}')
```
</details>

### **class** `Parser`
### **class** `GoogleDocstringParser(Parser)`
### ***method*** `__init__(self, docstring: str, indent: int = 4)`


<details>
<summary> <b>Source code</b> </summary>

```python
def __init__(self, docstring: str, indent: int=4):
    self.lines = docstring.splitlines()
    self.indent = indent
    self.lineno = 0
    self.char = 0
    self.docstring = Docstring()
```
</details>

### ***method*** `read_line(self, move: bool = True) -> str`



**Description**: 每次读取一行

**Arguments**:
> - move: 是否移动指针  


<details>
<summary> <b>Source code</b> </summary>

```python
def read_line(self, move: bool=True) -> str:
    """
        每次读取一行
        Args:
            move: 是否移动指针
        Returns:
        """
    if self.lineno >= len(self.lines):
        return ''
    line = self.lines[self.lineno]
    if move:
        self.lineno += 1
    return line
```
</details>

### ***method*** `match_token(self) -> Optional[str]`



**Description**: 解析下一行的token


<details>
<summary> <b>Source code</b> </summary>

```python
def match_token(self) -> Optional[str]:
    """
        解析下一行的token
        Returns:

        """
    for token in self._tokens:
        line = self.read_line(move=False)
        if line.strip().startswith(token):
            self.lineno += 1
            return self._tokens[token]
    return None
```
</details>

### ***method*** `parse_args(self)`



**Description**: 依次解析后面的参数行，直到缩进小于等于当前行的缩进


<details>
<summary> <b>Source code</b> </summary>

```python
def parse_args(self):
    """
        依次解析后面的参数行，直到缩进小于等于当前行的缩进
        """
    while (line := self.match_next_line()):
        if ':' in line:
            name, desc = line.split(':', 1)
            self.docstring.add_arg(name.strip(), desc.strip())
        else:
            self.docstring.add_arg(line.strip())
```
</details>

### ***method*** `parse_return(self)`



**Description**: 解析返回值行


<details>
<summary> <b>Source code</b> </summary>

```python
def parse_return(self):
    """
        解析返回值行
        """
    if (line := self.match_next_line()):
        self.docstring.add_return(line.strip())
```
</details>

### ***method*** `parse_raises(self)`



**Description**: 解析异常行


<details>
<summary> <b>Source code</b> </summary>

```python
def parse_raises(self):
    """
        解析异常行
        """
    while (line := self.match_next_line()):
        if ':' in line:
            name, desc = line.split(':', 1)
            self.docstring.add_raise(name.strip(), desc.strip())
        else:
            self.docstring.add_raise(line.strip())
```
</details>

### ***method*** `parse_example(self)`



**Description**: 解析示例行


<details>
<summary> <b>Source code</b> </summary>

```python
def parse_example(self):
    """
        解析示例行
        """
    while (line := self.match_next_line()):
        if ':' in line:
            name, desc = line.split(':', 1)
            self.docstring.add_example(name.strip(), desc.strip())
        else:
            self.docstring.add_example(line.strip())
```
</details>

### ***method*** `parse_attrs(self)`



**Description**: 解析属性行


<details>
<summary> <b>Source code</b> </summary>

```python
def parse_attrs(self):
    """
        解析属性行
        """
    while (line := self.match_next_line()):
        if ':' in line:
            name, desc = line.split(':', 1)
            self.docstring.add_attrs(name.strip(), desc.strip())
        else:
            self.docstring.add_attrs(line.strip())
```
</details>

### ***method*** `match_next_line(self) -> Optional[str]`



**Description**: 在一个子解析器中，解析下一行，直到缩进小于等于当前行的缩进


<details>
<summary> <b>Source code</b> </summary>

```python
def match_next_line(self) -> Optional[str]:
    """
        在一个子解析器中，解析下一行，直到缩进小于等于当前行的缩进
        Returns:
        """
    line = self.read_line(move=False)
    if line.startswith(' ' * self.indent):
        self.lineno += 1
        return line[self.indent:]
    else:
        return None
```
</details>

### ***method*** `parse(self) -> Docstring`



**Description**: 逐行解析，直到遇到EOS

最开始未解析到的内容全部加入desc



<details>
<summary> <b>Source code</b> </summary>

```python
def parse(self) -> Docstring:
    """
        逐行解析，直到遇到EOS

        最开始未解析到的内容全部加入desc

        Returns:

        """
    add_desc = True
    while self.lineno < len(self.lines):
        token = self.match_token()
        if token is None and add_desc:
            self.docstring.add_desc(self.lines[self.lineno].strip())
        if token is not None:
            add_desc = False
        match token:
            case 'args':
                self.parse_args()
            case 'return':
                self.parse_return()
            case 'attribute':
                self.parse_attrs()
            case 'raises':
                self.parse_raises()
            case 'example':
                self.parse_example()
            case _:
                self.lineno += 1
    return self.docstring
```
</details>

### **class** `NumpyDocstringParser(Parser)`
### **class** `ReStructuredParser(Parser)`