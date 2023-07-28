<div align="center">
<h1>IssueOps</h1></div>

<p align="center">
<img src="https://wakatime.com/badge/user/5bfd81bc-9515-462b-a942-069791b283b7/project/af5f20a2-48c4-4ffb-81b8-7c330a9ee330.svg?style=flat-square"  alt="Develop time"/>

</p>
<p align="center">通过issue触发自动化校验，然后提交pr</p>

## ✨ 使用说明

1. 按照模板新建issue，输入插件仓库的工程Toml文件地址，例如:[https://raw.githubusercontent.com/AliceBotProject/alicebot/master/pyproject.toml](https://raw.githubusercontent.com/AliceBotProject/alicebot/master/pyproject.toml),勾选条款

2. 等待自动化校验完成，如果校验失败，会在issue中回复失败原因

3. 若插件更新，只需在原先issue中输入`/validate`，则可再次触发自动化校验

4. 校验成功后，会自动提交pr，等待管理员审核

5. 审核通过后，会自动合并pr，关闭issue

## 🍜 参考文档

1. [issue comment](https://github.com/marketplace/actions/create-or-update-comment)
2. [managing-issues-and-pull-requests](https://docs.github.com/zh/actions/managing-issues-and-pull-requests)
3. [extensions-submissions](https://github.com/docker/extensions-submissions)
4. [creating-a-file-branch-pull-request-from-github-actions-by-issue-event](https://dev.classmethod.jp/articles/creating-a-file-branch-pull-request-from-github-actions-by-issue-event/)

## 📄 作者

(C) 2023 Marlene
