# Dify Zhipu Plugin

This repository packages a Dify model provider plugin for ZHIPU AI, aligned to the current `@z_ai/coding-helper` Coding Plan model set and extended with `glm-5` and `glm-5.1`.

## Included models

- `glm-5.1`
- `glm-5`
- `glm-4.7`
- `glm-4.6`
- `glm-4.5-air`
- `glm-4-plus`
- `embedding-2`
- `embedding-3`
- `text_embedding`

## Defaults

- Default endpoint: `https://open.bigmodel.cn/api/coding/paas/v4`
- Supported model types: `llm`, `text-embedding`
- `glm-5` metadata is aligned with Zhipu's public GLM-5 model card.
- `glm-5.1` is exposed as an additional predefined model entry. Zhipu has not published a standalone public model card for it yet, so its limits are aligned with the public GLM-5 family documentation.
- `embedding-2`, `embedding-3`, and `text_embedding` were verified to work on both standard PAAS and Coding Plan endpoints, even though they are not returned by the `/models` list API.

## Endpoint overrides

- China Coding Plan default: `https://open.bigmodel.cn/api/coding/paas/v4`
- Global Coding Plan override: `https://api.z.ai/api/coding/paas/v4`
- Standard PAAS override: `https://open.bigmodel.cn/api/paas/v4`

## Technical docs

Maintainer-oriented technical documentation is available in `docs/`.

## Local development

```bash
uv sync
python -m main
```

## Package plugin

Use the Dify CLI:

```bash
dify plugin package . -o zhipuai-0.1.2.difypkg
```

Or use the `dify-plugin` binary from `langgenius/dify-plugin-daemon` releases:

```bash
./dify-plugin plugin package . -o zhipuai-0.1.2.difypkg
```

## Publish for Dify GitHub installation

Dify installs GitHub plugins from release assets, not directly from source code. This repository includes `.github/workflows/release.yml`, which:

1. Triggers on tags matching `v*`
2. Packages the plugin into a `.difypkg`
3. Creates a GitHub Release and uploads the package asset

Example:

```bash
git tag v0.1.2
git push origin v0.1.2
```

After the workflow succeeds, Dify can install the plugin from this repository by selecting the release tag and the generated `.difypkg` asset.

## Configure in Dify

After installation, get an API key from ZHIPU AI and configure it in `Settings -> Model Provider`.

API key page:

- https://open.bigmodel.cn/usercenter/apikeys
