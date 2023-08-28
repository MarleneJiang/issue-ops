"""Utility functions for GitHub Actions."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests


def set_action_outputs(output_pairs: dict[str, str]) -> None:
    """Sets the GitHub Action outputs, with backwards compatibility for self-hosted runners without a GITHUB_OUTPUT environment file. Keyword arguments: output_pairs - Dictionary of outputs with values."""
    if "GITHUB_OUTPUT" in os.environ:
        with Path(os.environ["GITHUB_OUTPUT"]).open(mode="a") as f:
            for key, value in output_pairs.items():
                f.write(f"{key}={value}\n")
    else:
        for key, value in output_pairs.items():
            print(f"::set-output name={key}::{value}")  # noqa: T201


class Pypi:
    """获取pypi info."""

    BASE_URL = "https://pypi.org/pypi"
    CODE = 404
    name = None

    def __init__(self, name: str) -> None:
        """Init."""
        self.name = name
        self.data = self.get_response(name).get("info", {})

    def get_response(self, name: str) -> dict[str, Any]:
        """Request response from PyPi API."""
        target_url = f"{self.BASE_URL}/{name}/json"
        response = requests.get(target_url, timeout=5)
        if response.status_code == self.CODE:
            msg = "pypi_name检查出错"
            raise ValueError(msg)
        return response.json()

    def get(self, key: str) -> str | None:
        """."""
        if self.data == {}:
            msg = "module pypi info为空"
            raise ValueError(msg)
        return self.data.get(key, None)

    def check_pypi(self, name: str) -> bool:
        """Check module filename for conflict."""
        if name == "null":
            return False
        package_url = self.get("package_url")
        if package_url is not None:
            module_name = package_url.split("/")[-2]
            return name.lower() == module_name.lower()
        return False

    def get_info(self) -> dict[str, str]:
        """."""
        name = self.get("name")
        if (name is None) or (name == ""):
            msg = "模块名称获取失败"
            raise ValueError(msg)
        description = self.get("summary")
        if (description is None) or (description == ""):
            msg = "模块描述获取失败"
            raise ValueError(msg)
        author = self.get("author")
        if (author is None) or (author == ""):
            email = self.get("author_email")
            if email is not None and "<" in email:  # PDM发包问题
                author = email.split("<")[0].strip()
            else:
                msg = "作者信息获取失败"
                raise ValueError(msg)
        license_info = self.get("license")
        if license_info is None:
            license_info = ""
        homepage = self.get("home_page")
        if homepage is None:
            homepage = ""
        tags = self.get("keywords")
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
