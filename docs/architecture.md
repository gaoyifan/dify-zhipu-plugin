# 架构说明

## 1. 目录结构

```text
.
├── manifest.yaml
├── main.py
├── provider/
│   ├── zhipuai.py
│   └── zhipuai.yaml
├── models/
│   ├── _common.py
│   ├── llm/
│   │   ├── _position.yaml
│   │   ├── llm.py
│   │   └── *.yaml
│   └── text_embedding/
│       ├── text_embedding.py
│       └── *.yaml
├── _assets/
├── requirements.txt
├── pyproject.toml
└── .difyignore
```

## 2. 运行入口

### `main.py`

`main.py` 是 Dify 插件运行入口：

```python
from dify_plugin import Plugin, DifyPluginEnv

plugin = Plugin(DifyPluginEnv())

if __name__ == '__main__':
    plugin.run()
```

插件被 Dify 加载后，`Plugin(DifyPluginEnv())` 会根据 `manifest.yaml` 和 provider 声明文件注册模型能力。

## 3. `manifest.yaml`

`manifest.yaml` 定义插件级元数据，关键字段如下：

- `type: plugin`
  - 声明这是一个 Dify 插件
- `version`
  - 插件版本，对应 GitHub Release 的实际插件版本
- `author`
  - 插件作者，决定插件唯一标识中的作者部分
- `name`
  - 插件名，当前保持为 `zhipuai`
- `meta.runner`
  - 定义运行语言、Python 版本和入口模块
- `plugins.models`
  - 指向模型 provider 声明文件 `provider/zhipuai.yaml`

## 4. Provider 层

### `provider/zhipuai.yaml`

该文件负责声明：

- provider 名称
- 支持的模型类型
- 凭证表单
- Python 源码入口
- 帮助链接与图标

这里最关键的配置是：

- `extra.python.provider_source: provider/zhipuai.py`
- `extra.python.model_sources`
  - `models/llm/llm.py`
  - `models/text_embedding/text_embedding.py`

### `provider/zhipuai.py`

该文件实现 provider 凭证校验逻辑。当前实现沿用官方插件方案，通过获取一个 LLM 实例并调用 `validate_credentials()` 验证配置是否可用。

## 5. 模型实现层

### `models/_common.py`

公共逻辑主要负责：

- 兼容不同字段名的凭证读取
- 标准化 `api_key` / `base_url`
- 提供统一错误映射入口

### `models/llm/llm.py`

LLM 实现是插件核心，负责：

- 将 Dify 的消息格式转换为智谱 `chat.completions` 请求格式
- 处理流式与非流式响应
- 处理 tool calling
- 处理推理内容 `reasoning_content`
- 处理视觉输入模型的图像/视频内容格式
- 将 `thinking`、`response_format`、`web_search` 等参数翻译成智谱 SDK 调用参数

当前使用的 SDK 是 `zai-sdk`，核心调用对象为：

```python
client = ZhipuAiClient(api_key=..., base_url=...)
client.chat.completions.create(...)
```

### `models/text_embedding/text_embedding.py`

该文件负责智谱 embedding 模型的调用，结构与官方插件保持一致。

## 6. 模型声明文件

### LLM 模型清单

`models/llm/*.yaml` 是每个预定义模型的能力声明。Dify 会读取这些 YAML，将其展示为 provider 可选模型。

典型字段包括：

- `model`
  - 实际请求使用的 model id
- `model_type: llm`
- `features`
  - 如 `multi-tool-call`、`agent-thought`、`stream-tool-call`
- `model_properties.context_size`
- `parameter_rules`
  - 如 `temperature`、`top_p`、`max_tokens`、`thinking`

### 模型排序

`models/llm/_position.yaml` 控制模型在 Dify 中的展示顺序。新增模型后，需要同步把 model id 写入该文件。

## 7. 新增的 `glm-5` 与 `glm-5.1`

本仓库新增了两个模型声明文件：

- `models/llm/glm-5.yaml`
- `models/llm/glm-5.1.yaml`

实现策略如下：

- `glm-5`
  - 直接作为新的预定义模型接入
- `glm-5.1`
  - 作为额外预定义模型接入

其中 `glm-5.1` 当前没有找到独立公开模型卡，因此本仓库将其上下文长度、输出上限和参数边界与公开的 `GLM-5` 家族能力保持一致。这是一个显式推断，不是来自公开模型页的逐项逐字映射。

## 8. 打包边界控制

### `.difyignore`

`dify-plugin-daemon` 打包时优先读取 `.difyignore`。本仓库通过该文件排除了不应进入 `.difypkg` 的内容，例如：

- `.git/`
- `.github/`
- `.tools/`
- `.venv/`
- 本地产物与缓存

如果不配置 `.difyignore`，打包产物可能夹带本地调试或仓库元数据，导致包变大且不够干净。
