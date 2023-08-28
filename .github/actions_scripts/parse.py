"""信息解析:1. 标题的type解析,如果不符合就报错 2. 提取name、module_name、pypi_name,如果不符合就报错 3. pypi_name在pip网站中检查,不存在则报错."""
from __future__ import annotations

import os
import re
from typing import Any

from utils import Pypi, set_action_outputs


def parse_title(title: str) -> dict[str, Any]:
    """Prase Title."""
    pattern = r"\[(plugin|adapter|bot)\]:\s*(.+)"
    match = re.match(pattern, title)
    if match:
        return {"type": match.group(1), "name": match.group(2)}
    msg = "标题格式错误"
    raise ValueError(msg)


def raise_value_error(msg: str) -> None:
    """Raise ValueError."""
    raise ValueError(msg)


def main() -> None:
    """信息解析:1. 标题的type解析,如果不符合就报错 2. 提取name、module_name、pypi_name,如果不符合就报错 3. pypi_name在pip网站中检查,不存在则报错."""
    title = os.environ["TITLE"]
    pypi_name = os.environ["PYPI_NAME"]
    try:
        pypi = Pypi(pypi_name)
        if pypi.check_pypi(pypi_name) is False:
            msg = "输入的pypi_name存在问题"
            raise_value_error(msg)
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


if __name__ == "__main__":
    main()
