"""验证脚本能否正常运行。"""
from __future__ import annotations

import importlib
import os
import subprocess

from utils import PyPi, set_action_outputs

PYPI_NAME = os.environ["PYPI_NAME"]
MODULE_NAME = os.environ["MODULE_NAME"]
TYPE = os.environ["TYPE"]


def check_module(module_name: str) -> bool:
    """检查 module name。"""
    if module_name == "null":
        return False
    if "-" in module_name:
        return False
    try:
        importlib.invalidate_caches()
        module = importlib.import_module(module_name)
        importlib.reload(module)
    except BaseException:  # noqa: BLE001
        return False
    else:
        return True


def alicebot_test() -> None:
    """验证插件是否能在 AliceBot 中正常运行。"""
    try:
        # 要执行的 Python 脚本路径
        python_script_path = ".github/actions_scripts/plugin_test.py"
        result = subprocess.run(
            f"python {python_script_path} {MODULE_NAME} {TYPE}",
            timeout=10,
            check=True,
            shell=True,  # noqa: S602
            capture_output=True,
        )
        if result.returncode != 0:
            msg = f"脚本执行失败: {result.stdout}"
            raise ValueError(msg)
    except subprocess.TimeoutExpired as e:
        msg = f"脚本执行超时: {e.stdout}"
        raise ValueError(msg) from e
    except subprocess.CalledProcessError as e:
        msg = f"脚本执行错误: {e.stdout}"
        raise ValueError(msg) from e


def get_meta_info() -> None:
    """获取模块的元信息."""
    try:
        pypi = PyPi(PYPI_NAME)
        data = pypi.get_info()
        data["result"] = "success"
        data["output"] = "获取 module 元信息成功"
        set_action_outputs(data)
    except ValueError as e:
        set_action_outputs({"result": "error", "output": str(e)})


if __name__ == "__main__":
    if TYPE != "bot" and (check_module(MODULE_NAME) is False):
        set_action_outputs({"result": "error", "output": "输入的 module_name 存在问题"})
    else:
        try:
            if TYPE != "bot":
                alicebot_test()
        except ValueError as e:
            set_action_outputs({"result": "error", "output": str(e)})
        else:
            get_meta_info()
