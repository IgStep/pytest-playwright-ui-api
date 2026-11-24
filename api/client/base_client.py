import json
import logging
import time
from dataclasses import dataclass
from typing import Any

from playwright.sync_api import APIRequestContext

logger = logging.getLogger(__name__)

_BODY_PREVIEW_CHARS = 500


@dataclass(frozen=True)
class ApiResponse:
    """Snapshot of an HTTP exchange, detached from the Playwright response object.

    automationexercise.com reports most outcomes as HTTP 200 and puts the real
    status into the body as ``responseCode``, so both are exposed separately.
    """

    method: str
    url: str
    http_status: int
    text: str
    body: Any
    elapsed_ms: float

    @property
    def response_code(self) -> int | None:
        return self.body.get("responseCode") if isinstance(self.body, dict) else None

    @property
    def message(self) -> str | None:
        return self.body.get("message") if isinstance(self.body, dict) else None

    def __str__(self) -> str:
        preview = self.text[:_BODY_PREVIEW_CHARS]
        if len(self.text) > _BODY_PREVIEW_CHARS:
            preview += "..."
        return (
            f"{self.method} {self.url} -> HTTP {self.http_status} "
            f"({self.elapsed_ms:.0f} ms)\nBody: {preview}"
        )


class BaseApiClient:
    def __init__(self, request_context: APIRequestContext):
        self._request_context = request_context

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        form: dict[str, str] | None = None,
    ) -> ApiResponse:
        """Send a raw request. Public so negative tests can use any method/payload."""
        start = time.perf_counter()
        response = self._request_context.fetch(
            path, method=method, params=params, form=form
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        text = response.text()
        try:
            body = json.loads(text)
        except ValueError:
            body = None

        api_response = ApiResponse(
            method=method,
            url=response.url,
            http_status=response.status,
            text=text,
            body=body,
            elapsed_ms=elapsed_ms,
        )
        logger.info(
            "%s %s -> HTTP %s, responseCode=%s (%.0f ms)",
            method,
            response.url,
            api_response.http_status,
            api_response.response_code,
            elapsed_ms,
        )
        return api_response
