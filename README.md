# Dify Zhipu Plugin

This repository packages a Dify model provider plugin for ZHIPU AI, based on the official `langgenius/dify-official-plugins` `models/zhipuai` implementation and extended with `glm-5` and `glm-5.1`.

## Included models

- All predefined models from the current official ZHIPU AI Dify plugin base
- `glm-5`
- `glm-5.1`

## Notes

- `glm-5` metadata is aligned with Zhipu's public GLM-5 model card.
- `glm-5.1` is exposed as an additional predefined model entry. Zhipu has not published a standalone public model card for it at the time this repository was prepared, so its context and output limits are aligned with the public GLM-5 family documentation.

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
