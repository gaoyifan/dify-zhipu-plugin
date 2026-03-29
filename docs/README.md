# 技术文档

本文档目录面向插件维护者，说明这个 Dify 智谱模型插件的结构、运行机制、模型扩展方式以及发布流程。

## 文档列表

- `architecture.md`
  - 说明插件目录结构、Dify 运行入口、provider 与模型实现的关系
- `development-and-release.md`
  - 说明本地开发、验证、打包、GitHub Release 发布和 Dify 安装方式

## 插件定位

本仓库基于 Dify 官方 `zhipuai` 模型插件实现，保留官方 provider 结构，并在此基础上补充：

- `glm-5`
- `glm-5.1`

当前仓库是一个可直接发布到独立 GitHub 仓库的 Dify 模型插件仓库。Dify 安装时读取的是 GitHub Release 中的 `.difypkg` 资产，而不是仓库源码本身。

## 当前发布信息

- GitHub 仓库：`https://github.com/gaoyifan/dify-zhipu-plugin`
- 当前版本：`0.1.0`
- 当前标签：`v0.1.0`
- 当前发布包：`zhipuai-0.1.0.difypkg`
