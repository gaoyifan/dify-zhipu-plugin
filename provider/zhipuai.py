import logging
from dify_plugin.errors.model import CredentialsValidateFailedError
from dify_plugin import ModelProvider

from models._common import _CommonZhipuaiAI

logger = logging.getLogger(__name__)


class ZhipuaiProvider(_CommonZhipuaiAI, ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        Validate provider credentials

        if validate failed, raise exception

        :param credentials: provider credentials, credentials form defined in `provider_credential_schema`.
        """
        try:
            credentials_kwargs = self._to_credential_kwargs(credentials)
            self._list_available_models(credentials_kwargs=credentials_kwargs)
        except Exception as ex:
            logger.exception(
                f"{self.get_provider_schema().provider} credentials validate failed"
            )
            raise CredentialsValidateFailedError(str(ex)) from ex
