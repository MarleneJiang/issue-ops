"""内部使用的实用工具。"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests


def set_action_outputs(output_pairs: dict[str, str]) -> None:
    """设置 GitHub Action outputs。"""
    if "GITHUB_OUTPUT" in os.environ:
        with Path(os.environ["GITHUB_OUTPUT"]).open(mode="a") as f:
            for key, value in output_pairs.items():
                f.write(f"{key}={value}\n")
    else:
        for key, value in output_pairs.items():
            print(f"::set-output name={key}::{value}")


class PyPi:
    """PyPi 工具类。"""

    PYPI_BASE_URL = "https://pypi.org/pypi"

    def __init__(self, name: str) -> None:
        """初始化。"""
        self.name: str = name

        target_url = f"{self.PYPI_BASE_URL}/{self.name}/json"
        response = requests.get(target_url, timeout=5)
        if response.status_code != requests.codes.ok:
            msg = "pypi_name 检查出错"
            raise ValueError(msg)
        res = response.json()
        if not isinstance(res, dict) or "info" not in res or not res["info"]:
            msg = "请求插件 PyPi 信息失败"
            raise ValueError(msg)
        self.data: dict[str, Any] = response.json()["info"]

    def check_pypi(self) -> None:
        """检查 pypi_name。"""
        msg = "输入的 pypi_name 存在问题"
        if self.name == "null":
            raise ValueError(msg)
        package_url = self.data.get("package_url")
        if package_url is None:
            raise ValueError(msg)
        module_name = package_url.split("/")[-2]
        if self.name.lower() != module_name.lower():
            raise ValueError(msg)

    def get_info(self) -> dict[str, str]:
        """获取 PyPi 包信息"""
        name = self.data.get("name")
        if (name is None) or (name == ""):
            msg = "模块名称获取失败"
            raise ValueError(msg)
        description = self.data.get("summary")
        if (description is None) or (description == ""):
            msg = "模块描述获取失败"
            raise ValueError(msg)
        author = self.data.get("author")
        if (author is None) or (author == ""):
            email = self.data.get("author_email")
            if email is not None and "<" in email:  # PDM发包问题
                author = email.split("<")[0].strip()
            else:
                msg = "作者信息获取失败"
                raise ValueError(msg)
        license_info = self.data.get("license")
        if license_info is None:
            license_info = ""
        homepage = self.data.get("home_page")
        if homepage is None:
            homepage = ""
        tags = self.data.get("keywords")
        if (tags is None) or (tags == ""):
            msg = "标签信息获取失败"
            raise ValueError(msg)
        return {
            "name": name,
            "description": description,
            "author": author,
            "license": license_info,
            "homepage": homepage,
            "tags": tags,
        }
