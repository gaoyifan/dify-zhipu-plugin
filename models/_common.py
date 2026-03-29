import json
from urllib import error, request

from dify_plugin.errors.model import (
    InvokeAuthorizationError,
    InvokeBadRequestError,
    InvokeConnectionError,
    InvokeError,
    InvokeRateLimitError,
    InvokeServerUnavailableError,
)
from zai import ZhipuAiClient


class _CommonZhipuaiAI:
    def _normalize_base_url(self, base_url: str | None) -> str | None:
        if not base_url:
            return base_url
        return base_url.strip().rstrip("/")

    def _to_credential_kwargs(self, credentials: dict) -> dict:
        """
        Transform credentials to kwargs for model instance

        :param credentials:
        :return:
        """
        credentials_kwargs = {
            "api_key": credentials["api_key"]
            if "api_key" in credentials
            else credentials.get("zhipuai_api_key"),
        }

        if "base_url" in credentials:
            credentials_kwargs["base_url"] = self._normalize_base_url(
                credentials["base_url"]
            )
        elif "zhipuai_base_url" in credentials:
            credentials_kwargs["base_url"] = self._normalize_base_url(
                credentials["zhipuai_base_url"]
            )

        return credentials_kwargs

    def _build_client(self, credentials_kwargs: dict) -> ZhipuAiClient:
        return ZhipuAiClient(
            api_key=credentials_kwargs["api_key"],
            base_url=credentials_kwargs.get("base_url"),
        )

    def _list_available_models(
        self,
        credentials: dict | None = None,
        credentials_kwargs: dict | None = None,
    ) -> list[str]:
        if credentials_kwargs is None:
            if credentials is None:
                raise ValueError("credentials or credentials_kwargs is required")
            credentials_kwargs = self._to_credential_kwargs(credentials)

        client = self._build_client(credentials_kwargs)
        base_url = self._normalize_base_url(client.base_url or client.default_base_url)
        models_url = f"{base_url}/models"

        req = request.Request(models_url, headers=client.auth_headers)

        try:
            with request.urlopen(req, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as ex:
            detail = ex.read().decode("utf-8", errors="replace")
            raise ValueError(
                f"/models request failed with HTTP {ex.code}: {detail}"
            ) from ex
        except error.URLError as ex:
            raise ValueError(f"/models request failed: {ex.reason}") from ex

        data = payload.get("data")
        if not isinstance(data, list):
            raise ValueError("Unexpected /models response payload")

        model_ids: list[str] = []
        for item in data:
            if isinstance(item, dict):
                model_id = item.get("id")
                if isinstance(model_id, str):
                    model_ids.append(model_id)

        return model_ids

    @property
    def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
        """
        Map model invoke error to unified error
        The key is the error type thrown to the caller
        The value is the error type thrown by the model,
        which needs to be converted into a unified error type for the caller.

        :return: Invoke error mapping
        """
        return {
            InvokeConnectionError: [],
            InvokeServerUnavailableError: [],
            InvokeRateLimitError: [],
            InvokeAuthorizationError: [],
            InvokeBadRequestError: [],
        }
