"""验证脚本能否正常运行."""
from __future__ import annotations

import os
import subprocess

from utils import set_action_outputs

PYPI_NAME = os.environ["PYPI_NAME"]
MODULE_NAME = os.environ["MODULE_NAME"]
TYPE = os.environ["TYPE"]
print("MODULE_NAME",MODULE_NAME)

def check_module(module_name: str) -> bool:
    """Check module name."""
    import importlib
    print("module_name",module_name)
    if module_name == "null":
        print("null")
        return False
    if "-" in module_name:
        print("-")
        return False
    try:
        print("try")
        importlib.invalidate_caches()
        module = importlib.import_module(module_name)
        importlib.reload(module)
    except BaseException as e:  # noqa: BLE001
        print("except",e)
        return False
    else:
        print("else")
        return True


def alicebot_test() -> None:
    """验证插件是否能在 alicebot 中正常运行."""
    try:
        # 要执行的 Python 脚本路径
        python_script_path = ".github/actions_scripts/plugin_test.py"
        # 整个命令
        command = f"python {python_script_path} {MODULE_NAME} {TYPE}"
        result = subprocess.run(
            command, timeout=10, check=True, shell=True, capture_output=True)  # noqa: S602
        if result.returncode != 0:
            msg = f"脚本执行失败: {result.stdout}"
            raise ValueError(msg) from None
    except subprocess.TimeoutExpired as e:
        msg = f"脚本执行超时: {e.stdout}"
        raise ValueError(msg) from e
    except subprocess.CalledProcessError as e:
        msg = f"脚本执行错误: {e.stdout}"
        raise ValueError(msg) from e


def get_meta_info() -> None:
    """获取模块的元信息."""
    from importlib.metadata import metadata

    metadata = metadata(PYPI_NAME)
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
        email = metadata.get_all("Author-email")
        if email is not None and "<" in email[0]:  # PDM发包问题
            author = [email[0].split("<")[0].strip()]
        else:
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
    print("MODULE_NAME",MODULE_NAME)
    if check_module(MODULE_NAME) is False:
        set_action_outputs({"result": "error", "output": "输入的module_name存在问题"})
    else:
        try:
            alicebot_test()
        except Exception:  # noqa: BLE001
            set_action_outputs({"result": "error", "output": "无法在alicebot中正常运行"})
        else:
            get_meta_info()
