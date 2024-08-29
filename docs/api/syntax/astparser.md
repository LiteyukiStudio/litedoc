---
title: litedoc.syntax.astparser
---
### **class** `AstParser`
### ***method*** `__init__(self, code: str, style: str = 'google')`



**Description**: 从代码解析AST

**Arguments**:
> - code: 代码  
> - style: 注释风格  


<details>
<summary> <b>Source code</b> </summary>

```python
def __init__(self, code: str, style: str='google'):
    """
        从代码解析AST
        Args:
            code: 代码
            style: 注释风格
        """
    self.style = style
    self.code = code
    self.tree = ast.parse(code)
    self.classes: list[ClassNode] = []
    self.functions: list[FunctionNode] = []
    self.variables: list[AssignNode] = []
    self.parse()
```
</details>

### `@staticmethod`
### ***method*** `clear_quotes(s: str) -> str`



**Description**: 去除类型注解中的引号

**Arguments**:
> - s:   


<details>
<summary> <b>Source code</b> </summary>

```python
@staticmethod
def clear_quotes(s: str) -> str:
    """
        去除类型注解中的引号
        Args:
            s:
        Returns:
        """
    return s.replace("'", '').replace('"', '')
```
</details>

### ***method*** `get_line_content(self, lineno: int, ignore_index_out: bool = True) -> str`



**Description**: 获取代码行内容

**Arguments**:
> - lineno: 行号  
> - ignore_index_out: 是否忽略索引越界  

**Return**: 代码行内容


<details>
<summary> <b>Source code</b> </summary>

```python
def get_line_content(self, lineno: int, ignore_index_out: bool=True) -> str:
    """获取代码行内容
        Args:
            lineno: 行号
            ignore_index_out: 是否忽略索引越界
        Returns:
            代码行内容
        """
    if ignore_index_out:
        if lineno < 1 or lineno > len(self.code.split('\n')):
            return ''
    return self.code.split('\n')[lineno - 1]
```
</details>

### `@staticmethod`
### ***method*** `match_line_docs(linecontent: str) -> str`



**Description**: 匹配行内注释

**Arguments**:
> - linecontent: 行内容  

**Return**: 文档字符串


<details>
<summary> <b>Source code</b> </summary>

```python
@staticmethod
def match_line_docs(linecontent: str) -> str:
    """匹配行内注释
        Args:
            linecontent: 行内容
        Returns:
            文档字符串
        """
    in_string = False
    string_char = ''
    for i, char in enumerate(linecontent):
        if char in ('"', "'"):
            if in_string:
                if char == string_char:
                    in_string = False
            else:
                in_string = True
                string_char = char
        elif char == '#' and (not in_string):
            return linecontent[i + 1:].strip()
    return ''
```
</details>

### ***method*** `parse(self)`


<details>
<summary> <b>Source code</b> </summary>

```python
def parse(self):
    for node in ast.walk(self.tree):
        if isinstance(node, ast.ClassDef):
            if not self._is_module_level_class(node):
                continue
            class_node = ClassNode(name=node.name, docs=parse(ast.get_docstring(node), parser=self.style) if ast.get_docstring(node) else None, inherits=[ast.unparse(base) for base in node.bases])
            self.classes.append(class_node)
            for sub_node in node.body:
                if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    class_node.methods.append(FunctionNode(name=sub_node.name, docs=parse(ast.get_docstring(sub_node), parser=self.style) if ast.get_docstring(sub_node) else None, posonlyargs=[ArgNode(name=arg.arg, type=self.clear_quotes(ast.unparse(arg.annotation).strip()) if arg.annotation else TypeHint.NO_TYPEHINT) for arg in sub_node.args.posonlyargs], args=[ArgNode(name=arg.arg, type=self.clear_quotes(ast.unparse(arg.annotation).strip()) if arg.annotation else TypeHint.NO_TYPEHINT) for arg in sub_node.args.args], kwonlyargs=[ArgNode(name=arg.arg, type=self.clear_quotes(ast.unparse(arg.annotation).strip()) if arg.annotation else TypeHint.NO_TYPEHINT) for arg in sub_node.args.kwonlyargs], kw_defaults=[ConstantNode(value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT) for default in sub_node.args.kw_defaults], defaults=[ConstantNode(value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT) for default in sub_node.args.defaults], return_=self.clear_quotes(ast.unparse(sub_node.returns).strip()) if sub_node.returns else TypeHint.NO_RETURN, decorators=[ast.unparse(decorator).strip() for decorator in sub_node.decorator_list], is_async=isinstance(sub_node, ast.AsyncFunctionDef), src=ast.unparse(sub_node).strip(), is_classmethod=True))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not self._is_module_level_function(node):
                continue
            self.functions.append(FunctionNode(name=node.name, docs=parse(ast.get_docstring(node), parser=self.style) if ast.get_docstring(node) else None, posonlyargs=[ArgNode(name=arg.arg, type=self.clear_quotes(ast.unparse(arg.annotation).strip()) if arg.annotation else TypeHint.NO_TYPEHINT) for arg in node.args.posonlyargs], args=[ArgNode(name=arg.arg, type=self.clear_quotes(ast.unparse(arg.annotation).strip()) if arg.annotation else TypeHint.NO_TYPEHINT) for arg, default in zip(node.args.args, node.args.defaults)], kwonlyargs=[ArgNode(name=arg.arg, type=self.clear_quotes(ast.unparse(arg.annotation).strip()) if arg.annotation else TypeHint.NO_TYPEHINT) for arg in node.args.kwonlyargs], kw_defaults=[ConstantNode(value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT) for default in node.args.kw_defaults], defaults=[ConstantNode(value=ast.unparse(default).strip() if default else TypeHint.NO_DEFAULT) for default in node.args.defaults], return_=self.clear_quotes(ast.unparse(node.returns).strip()) if node.returns else TypeHint.NO_RETURN, decorators=[ast.unparse(decorator).strip() for decorator in node.decorator_list], is_async=isinstance(node, ast.AsyncFunctionDef), src=ast.unparse(node).strip()))
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            if not self._is_module_level_variable2(node):
                continue
            else:
                pass
            lineno = node.lineno
            prev_line = self.get_line_content(lineno - 1).strip()
            curr_line = self.get_line_content(lineno).strip()
            next_line = self.get_line_content(lineno + 1).strip()
            if next_line.startswith('"""'):
                docs = next_line[3:-3]
            elif prev_line.startswith('"""'):
                docs = prev_line[3:-3]
            else:
                curr_docs = self.match_line_docs(curr_line)
                if curr_docs:
                    docs = curr_docs
                else:
                    docs = None
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.variables.append(AssignNode(name=target.id, value=ast.unparse(node.value).strip(), type=ast.unparse(node.annotation).strip() if isinstance(node, ast.AnnAssign) else TypeHint.NO_TYPEHINT, docs=docs))
            if isinstance(node, ast.AnnAssign):
                self.variables.append(AssignNode(name=node.target.id, value=ast.unparse(node.value).strip() if node.value else TypeHint.NO_DEFAULT, type=ast.unparse(node.annotation).strip(), docs=docs))
```
</details>

### ***method*** `_is_module_level_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef)`


<details>
<summary> <b>Source code</b> </summary>

```python
def _is_module_level_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
    for parent in ast.walk(self.tree):
        if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node in parent.body:
                return False
    return True
```
</details>

### ***method*** `_is_module_level_class(self, node: ast.ClassDef)`


<details>
<summary> <b>Source code</b> </summary>

```python
def _is_module_level_class(self, node: ast.ClassDef):
    for parent in ast.walk(self.tree):
        if isinstance(parent, ast.ClassDef):
            if node in parent.body:
                return False
    return True
```
</details>

### ***method*** `_is_module_level_variable(self, node: ast.Assign | ast.AnnAssign)`



**Description**: 在类方法或函数内部的变量不会被记录


<details>
<summary> <b>Source code</b> </summary>

```python
def _is_module_level_variable(self, node: ast.Assign | ast.AnnAssign):
    """在类方法或函数内部的变量不会被记录"""

    def _check(_node, _parent):
        if isinstance(_parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if _node in _parent.body:
                return False
            else:
                for sub_node in _parent.body:
                    if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return _check(_node, sub_node)
        return True
    for parent in ast.walk(self.tree):
        if not _check(node, parent):
            return False
    return True
```
</details>

### ***method*** `_is_module_level_variable2(self, node: ast.Assign | ast.AnnAssign) -> bool`



**Description**: 检查变量是否在模块级别定义。


<details>
<summary> <b>Source code</b> </summary>

```python
def _is_module_level_variable2(self, node: ast.Assign | ast.AnnAssign) -> bool:
    """
        检查变量是否在模块级别定义。
        """
    for parent in ast.walk(self.tree):
        if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node in parent.body:
                return False
    return True
```
</details>
