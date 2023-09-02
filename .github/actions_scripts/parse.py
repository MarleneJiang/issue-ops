"""信息解析。

1. 解析标题的 type，如果不符合就报错。
2. 提取 name、module_name、pypi_name，如果不符合就报错。
3. pypi_name 在 pip 网站中检查，不存在则报错。
"""
from __future__ import annotations

import os
import re
from typing import Any

from utils import PyPi, set_action_outputs


def parse_title(title: str) -> dict[str, Any]:
    """解析标题。"""
    pattern = r"\[(plugin|adapter|bot)\]:\s*(.+)"
    match = re.match(pattern, title)
    if match:
        return {"type": match.group(1), "name": match.group(2)}
    msg = "标题格式错误"
    raise ValueError(msg)


if __name__ == "__main__":
    title = os.environ["TITLE"]
    pypi_name = os.environ["PYPI_NAME"]
    try:
        PyPi(pypi_name).check_pypi()
        parsed = parse_title(title)
        set_action_outputs(
            {
                "result": "success",
                "output": "",
                "type": parsed.get("type", ""),
                "name": parsed.get("name", ""),
            }
        )
    except ValueError as e:
        set_action_outputs({"result": "error", "output": str(e)})
