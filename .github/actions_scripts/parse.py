"""信息解析:1. 标题的type解析,如果不符合就报错 2. 提取name、module_name、pypi_name,如果不符合就报错 3. pypi_name在pip网站中检查,不存在则报错."""
from __future__ import annotations

import os
import re
from typing import Any

import requests
from utils import set_action_outputs

BASE_URL = "https://pypi.org/pypi"
CODE = 404


def get_response(name: str) -> dict[str, Any] | None:
    """Request response from PyPi API."""
    target_url = f"{BASE_URL}/{name}/json"
    response = requests.get(target_url, timeout=5)
    if response.status_code == CODE:
        return None
    return response.json()


def check_pypi(name: str) -> bool:
    """Check module filename for conflict."""
    if name == "null":
        return False
    response = get_response(name)

    if response:
        module_name = response.get("info", {}).get("package_url", "").split("/")[-2]
        return name.lower() == module_name.lower()

    return False

def check_module(module_name: str) -> bool:
    """Check module name."""
    import importlib
    if module_name == "null":
        print("module_name is null")# noqa: T201
        return False
    if "-" in module_name:
        print("module_name contains '-'")# noqa: T201
        return False
    try:
        importlib.invalidate_caches()
        module = importlib.import_module(module_name)
        importlib.reload(module)
        print(f"module_name: {module_name}")# noqa: T201
    except BaseException as e:  # noqa: BLE001
        print(f"module_name is invalid ${e}")# noqa: T201
        return False
    else:
        print("module_name is valid")# noqa: T201
        return True

def parse_title(title: str) -> dict[str, Any]:
    """Prase Title."""
    pattern = r"\[(plugin|adapter|bot)\]:\s*(.+)"
    match = re.match(pattern, title)
    if match:
        return {"type": match.group(1), "name": match.group(2)}
    msg = "标题格式错误"
    raise ValueError(msg)


def main() -> None:
    """信息解析:1. 标题的type解析,如果不符合就报错 2. 提取name、module_name、pypi_name,如果不符合就报错 3. pypi_name在pip网站中检查,不存在则报错."""
    title = os.environ["TITLE"]
    pypi_name = os.environ["PYPI_NAME"]
    module_name = os.environ["MODULE_NAME"]
    try:
        print(f"module_name: {module_name}")# noqa: T201
        if check_module(module_name) is False:
            set_action_outputs({"result": "error", "output": "输入的module_name存在问题"})
            return
        if check_pypi(pypi_name) is False:
            set_action_outputs({"result": "error", "output": "输入的pypi_name存在问题"})
            return
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
