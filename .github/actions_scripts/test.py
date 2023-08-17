"""验证脚本能否正常运行."""
from __future__ import annotations

import os

from utils import set_action_outputs

pypi_name = os.environ["PYPI_NAME"]


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
    get_meta_info()
