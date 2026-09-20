import logging
from collections.abc import Iterable

from atlas.config import settings


class RedactSecrets(logging.Filter):
    """Replace known secret values in log records with a placeholder.

    Attached to handlers rather than to a logger: filters on a logger are
    not applied to records propagated up from child loggers, so a filter
    on root would never see httpx's records.

    :param secrets: candidate secret values; falsy entries are ignored.
    """

    PLACEHOLDER = "***REDACTED***"

    def __init__(self, secrets: Iterable[str | None]) -> None:
        super().__init__()
        self._secrets = [s for s in secrets if s]

    def filter(self, record: logging.LogRecord) -> bool:
        """Redact in place and always allow the record through.

        :param record: the record about to be emitted.
        :return: always True; this filter rewrites, it never drops.
        """
        if not self._secrets:
            return True

        for secret in self._secrets:
            if isinstance(record.msg, str) and secret in record.msg:
                record.msg = record.msg.replace(secret, self.PLACEHOLDER)

            if isinstance(record.args, tuple):
                record.args = tuple(
                    str(arg).replace(secret, self.PLACEHOLDER) if secret in str(arg) else arg
                    for arg in record.args
                )

        return True


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    redactor = RedactSecrets([settings.news_api_key])

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(redactor)

    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler("atlas.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(redactor)

    logger.addHandler(file_handler)
