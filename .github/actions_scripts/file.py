"""添加信息:1. 获取对应json文件并解析 2. 查询是否有同名插件,若存在则覆盖,并更新时间 3. 否则添加至最后一行,并附上更新时间 4. 保存至文件."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

type_info = os.environ["TYPE"]
module_name = os.environ["MODULE_NAME"]
pypi_name = os.environ["PYPI_NAME"]
name = os.environ["NAME"]
description = os.environ["DESCRIPTION"]
author = os.environ["AUTHOR"]
license_info = os.environ["LICENSE"]
homepage = os.environ["HOMEPAGE"]
tags = os.environ["TAGS"]

def set_action_outputs(output_pairs: dict[str, str]) -> None:
  """Sets the GitHub Action outputs, with backwards compatibility for self-hosted runners without a GITHUB_OUTPUT environment file. Keyword arguments: output_pairs - Dictionary of outputs with values."""
  if "GITHUB_OUTPUT" in os.environ :
    with Path(os.environ["GITHUB_OUTPUT"]).open(mode="a") as f :
      for key, value in output_pairs.items() :
        f.write(f"{key}={value}\n")
  else :
    for key, value in output_pairs.items() :
      print(f"::set-output name={key}::{value}")  # noqa: T201



def get_json() -> dict[str, Any]:
  """获取对应json文件并解析."""
  with Path(type_info+"s.json").open(encoding="utf-8") as f:
    return json.load(f)

def add_info(json_data: list[dict[str, str]],infos:dict[str, Any]) -> bool:
  """查询是否有同名插件,若存在则覆盖,并更新时间."""
  for i in json_data:
    if i["name"] == name:
      i["module_name"] = infos["module_name"]
      i["pypi_name"] = infos["pypi_name"]
      i["description"] = infos["description"]
      i["author"] = infos["author"]
      i["license"] = infos["license"]
      i["homepage"] = infos["homepage"]
      i["tags"] = infos["tags"]
      return True
  json_data.append(infos)
  return False

def save_json(json_data: dict[str, Any]) -> None:
  """保存至文件."""
  with Path(type_info+"s.json").open(mode="w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

def main() -> None:
  """添加信息:1. 获取对应json文件并解析 2. 查询是否有同名插件,若存在则覆盖,并更新时间 3. 否则添加至最后一行,并附上更新时间 4. 保存至文件."""
  json_data = get_json()
  data_list = json_data.get(type_info+"s", [])
  info = {"module_name": module_name, "pypi_name": pypi_name, "name": name, "description": description, "author": author, "license": license_info, "homepage": homepage, "tags": tags,"is_official": False}
  if add_info(data_list,info):
    set_action_outputs({"result": "success", "output": "插件信息更新成功","file_json":json.dumps(info)})
  else:
    set_action_outputs({"result": "success", "output": "插件信息添加成功","file_json":json.dumps(info)})
  json_data[type_info+"s"] = data_list
  save_json(json_data)

if __name__ == "__main__":
  main()
