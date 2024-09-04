# -*- coding: utf-8 -*-
"""
Internationalization module.
"""
from typing import Optional, TypeAlias

NestedDict: TypeAlias = dict[str, 'str | NestedDict']

"""@litedoc-hide"""
i18n_dict: dict[str, NestedDict] = {  # @litedoc-hide
        "en"     : {
                "docstring"     : {
                        "args"     : "Arguments",
                        "return"   : "Return",
                        "attribute": "Attribute",
                        "raises"   : "Raises",
                        "example"  : "Examples",
                        "yields"   : "Yields",
                },
                "module"        : "Module",
                "src"           : "Source code",
                "desc"          : "Description",
                "type"          : "Type",
                "or"            : "or",
                "view_on_github": "View on GitHub",
                "default_value" : "Default",
        },
        "zh-Hans": {
                "docstring"     : {
                        "args"     : "参数",
                        "return"   : "返回",
                        "attribute": "属性",
                        "raises"   : "引发",
                        "example"  : "示例",
                        "yields"   : "产出",
                },
                "module"        : "模块",
                "src"           : "源代码",
                "desc"          : "说明",
                "type"          : "类型",
                "or"            : "或",
                "view_on_github": "在GitHub上查看",
                "default_value" : "默认值",
        },
        "zh-Hant": {
                "docstring"     : {
                        "args"     : "變數説明",
                        "return"   : "返回",
                        "attribute": "屬性",
                        "raises"   : "抛出",
                        "example"  : "範例",
                        "yields"   : "產出",
                },
                "module"        : "模組",
                "src"           : "源碼",
                "desc"          : "説明",
                "type"          : "類型",
                "or"            : "或",
                "view_on_github": "於GitHub上查看",
                "default_value" : "默認值",
        },
        "ja"     : {
                "docstring"     : {
                        "args"     : "引数",
                        "return"   : "戻り値",
                        "attribute": "属性",
                        "raises"   : "例外",
                        "example"  : "例",
                        "yields"   : "生成",
                },
                "module"        : "モジュール",
                "src"           : "ソースコード",
                "desc"          : "説明",
                "type"          : "タイプ",
                "or"            : "または",
                "view_on_github": "GitHubで表示",
                "default_value" : "デフォルト",
        },
}  # @litedoc-hide


def flat_i18n_dict(data: dict[str, NestedDict]) -> dict[str, dict[str, str]]:
    """
    Flatten i18n_dict.
    Args:
        data: i18n_dict
    Returns:
        dict: flatten dict
    """
    ret: dict[str, dict[str, str]] = {}

    def _flat(_lang_data: NestedDict) -> dict[str, str]:
        res = {}
        for k, v in _lang_data.items():
            if isinstance(v, dict):
                for kk, vv in _flat(v).items():
                    res[f"{k}.{kk}"] = vv
            else:
                res[k] = v
        return res

    for lang, lang_data in data.items():
        ret[lang] = _flat(lang_data)

    return ret


i18n_flat_dict = flat_i18n_dict(i18n_dict)


def get_text(lang: str, key: str, default: Optional[str] = None, fallback: Optional[str] = "en") -> str:
    """
    Get text from i18n_dict.
    Args:
        lang: language name
        key: text key
        default: default text, if None return fallback language or key
        fallback: fallback language, priority is higher than default
    Returns:
        str: text
    """
    if lang in i18n_flat_dict:
        if key in i18n_flat_dict[lang]:
            return i18n_flat_dict[lang][key]

    if fallback is not None:
        return i18n_flat_dict.get(fallback, {}).get(key, default or key)
    else:
        return default or key


litedoc_hide = "@litedoc-hide"
