"""验证脚本能否正常运行."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from utils import set_action_outputs

pypi_name = os.environ["PYPI_NAME"]
module_name = os.environ["MODULE_NAME"]



current_directory = Path(__file__).parent
print("当前文件所在目录:", current_directory)  # noqa: T201

def check_module(module_name: str) -> bool:
    """Check module name."""
    import importlib
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
    """验证插件是否能在 alicebot 中正常运行."""
    try:

        # 要执行的 Python 脚本路径
        python_script_path = ".github/actions_scripts/plugin_test.py"
        # 整个命令
        command = f"python {python_script_path} {module_name}"
        print(f"command: {command}")# noqa: T201
        result = subprocess.run(command, timeout=10, check=True, shell=True)  # noqa: S602
        print(f"result: {result}")# noqa: T201
        if result.returncode != 0:
            msg = f"脚本执行失败: {result.stdout}"
            print(f"msg: {msg}")# noqa: T201
            raise ValueError(msg) from None
    except subprocess.TimeoutExpired:
        print("Script execution timed out!")# noqa: T201
        raise
    except subprocess.CalledProcessError as e:
        msg = f"Script execution failed with error code {e.returncode}"
        print(f"msg: {msg}")# noqa: T201
        raise ValueError(msg) from e


def get_meta_info() -> None:
    """获取模块的元信息."""
    from importlib.metadata import metadata

    metadata = metadata(pypi_name)
    name = metadata.get_all("Name")
    if name is None:
        set_action_outputs({"result": "error", "output": "模块名称获取失败"})
        return
    description = metadata.get_all("Summary")
    if description is None:
        set_action_outputs({"result": "error", "output": "模块描述获取失败"})
        return
    author = metadata.get_all("Author")
    if author is None:
        set_action_outputs({"result": "error", "output": "作者信息获取失败"})
        return
    license_info = metadata.get_all("License")
    if license_info is None:
        license_info = [""]
    homepage = metadata.get_all("Home-page")
    if homepage is None:
        homepage = [""]
    tags = metadata.get_all("Keywords")
    if tags is None:
        set_action_outputs({"result": "error", "output": "标签信息获取失败"})
        return
    tags = metadata.get_all("Keywords")
    if tags is None:
        set_action_outputs({"result": "error", "output": "标签信息获取失败"})
        return
    set_action_outputs(
        {
            "result": "success",
            "output": "模块元信息获取成功",
            "name": name[0],
            "description": description[0],
            "author": author[0],
            "license": license_info[0],
            "homepage": homepage[0],
            "tags": str(tags),
        }
    )


if __name__ == "__main__":
    if check_module(module_name) is False:
        set_action_outputs({"result": "error", "output": "输入的module_name存在问题"})
    else:
        try:
            print("alicebot_test")# noqa: T201
            alicebot_test()
        except Exception as e:  # noqa: BLE001
            print(f"Exception: {e}")# noqa: T201
            set_action_outputs({"result": "error", "output": "无法在alicebot中正常运行"})
        else:
            print("get_meta_info")# noqa: T201
            get_meta_info()
