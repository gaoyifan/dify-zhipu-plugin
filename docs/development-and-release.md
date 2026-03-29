# 开发与发布

## 1. 本地开发环境

本仓库优先使用 `uv` 管理 Python 环境。

### 安装依赖

```bash
uv sync
```

这会根据 `pyproject.toml` 和 `uv.lock` 创建 `.venv/` 并安装运行依赖。

## 2. 本地验证

建议至少执行以下验证。

### 语法与导入检查

```bash
uv run python -m compileall main.py provider models
```

### 核心模块导入检查

```bash
uv run python - <<'PY'
from provider.zhipuai import ZhipuaiProvider
from models.llm.llm import ZhipuAILargeLanguageModel
print(ZhipuaiProvider.__name__)
print(ZhipuAILargeLanguageModel.__name__)
PY
```

### 打包检查

从 `langgenius/dify-plugin-daemon` release 下载 `dify-plugin` 二进制后执行：

```bash
./dify-plugin plugin package . -o zhipuai-0.1.2.difypkg
```

然后检查包内容：

```bash
unzip -l zhipuai-0.1.2.difypkg
```

重点确认：

- 包内存在 `manifest.yaml`
- 包内存在公开 LLM `models/llm/glm-5.yaml`
- 包内存在公开 LLM `models/llm/glm-5.1.yaml`
- 包内存在 embedding 模型 `models/text_embedding/embedding-2.yaml`
- 包内不包含 `.git/`、`.github/`、`.tools/`、`.venv/`

## 3. 新增模型的维护方式

如果未来需要继续添加智谱新模型，建议按以下顺序操作。

1. 在 `models/llm/` 下新增对应的 YAML 声明文件
2. 如果要公开该模型，同时把模型文件写入 `provider/zhipuai.yaml` 的 `predefined` whitelist
3. 把模型 id 写入 `models/llm/_position.yaml`
4. 如果新模型引入新的调用参数，再修改 `models/llm/llm.py`
5. 重新执行本地验证与打包检查

只有新增 YAML 而不更新 provider whitelist 与 `_position.yaml`，通常会导致模型文件存在但不会在 Dify 中公开。

## 4. 版本管理

发布版本时需要同时维护三个概念：

- `manifest.yaml` 中的 `version`
  - 例如 `0.1.2`
- Git tag
  - 例如 `v0.1.2`
- GitHub Release 中的 `.difypkg` 资产名
  - 例如 `zhipuai-0.1.2.difypkg`

本仓库要求：

- tag 去掉前缀 `v` 后，必须与 `manifest.yaml` 的 `version` 完全一致

GitHub Actions workflow 中已经包含这个校验。

## 5. GitHub 发布流程

本仓库包含自动发布工作流 `.github/workflows/release.yml`。

工作流触发条件：

- 推送 tag，且 tag 匹配 `v*`

工作流执行内容：

1. 下载最新 `dify-plugin` CLI
2. 读取 `manifest.yaml` 中的插件名和版本
3. 校验 tag 与版本是否一致
4. 打包生成 `.difypkg`
5. 创建或更新对应 GitHub Release
6. 上传 `.difypkg` 资产

### 标准发布命令

```bash
git tag v0.1.2
git push origin v0.1.2
```

## 6. Dify 安装方式

Dify 从 GitHub 安装插件时，读取的是 release 资产，而不是仓库源码。安装时通常需要：

- GitHub 仓库地址
- release 版本
- `.difypkg` 包名

对于当前仓库：

- 仓库：`gaoyifan/dify-zhipu-plugin`
- 版本：`v0.1.2`
- 包：`zhipuai-0.1.2.difypkg`

## 7. 当前已验证的发布结果

当前版本已经完成以下动作：

- 提交到 `main`
- 推送到 GitHub
- 创建 tag `v0.1.2`
- 创建 GitHub Release
- 上传 `zhipuai-0.1.2.difypkg`

对应仓库地址：

- `https://github.com/gaoyifan/dify-zhipu-plugin`

对应 release 地址：

- `https://github.com/gaoyifan/dify-zhipu-plugin/releases/tag/v0.1.2`
