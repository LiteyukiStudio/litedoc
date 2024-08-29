---
title: litedoc.version
---
### ***func*** `format_date_number() -> str`



**Description**: 将日期转换为20240212114514

**Arguments**:
> - date: 日期  

**Return**: 日期字符串


<details>
<summary> <b>Source code</b> </summary>

```python
def format_date_number() -> str:
    """
    将日期转换为20240212114514
    Args:
        date: 日期
    Returns:
        日期字符串
    """
    import datetime
    date = datetime.datetime.now()
    return date.strftime('%Y%m%d%H%M%S')
```
</details>

### ***func*** `get_version() -> str`


<details>
<summary> <b>Source code</b> </summary>

```python
def get_version() -> str:
    return f'0.1.0.dev{format_date_number()}'
```
</details>

