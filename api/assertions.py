from typing import overload

import pytest
from pydantic import BaseModel, ValidationError

from api.client.base_client import ApiResponse


@overload
def assert_api_response(
    response: ApiResponse,
    *,
    code: int | None = 200,
    message: str | None = None,
    http_status: int = 200,
    model: None = None,
) -> None: ...


@overload
def assert_api_response[M: BaseModel](
    response: ApiResponse,
    *,
    code: int | None = 200,
    message: str | None = None,
    http_status: int = 200,
    model: type[M],
) -> M: ...


def assert_api_response[M: BaseModel](
    response: ApiResponse,
    *,
    code: int | None = 200,
    message: str | None = None,
    http_status: int = 200,
    model: type[M] | None = None,
) -> M | None:
    """Single place that knows how this API reports outcomes.

    ``http_status`` is the transport status, ``code`` is the body's
    ``responseCode`` (pass ``None`` for responses without one). When ``model``
    is given, the body is validated against it and the parsed model returned.
    """
    __tracebackhide__ = True

    assert response.http_status == http_status, (
        f"Expected HTTP {http_status}, got {response.http_status}\n{response}"
    )
    if code is not None:
        assert response.response_code == code, (
            f"Expected responseCode {code}, got {response.response_code}\n{response}"
        )
    if message is not None:
        assert response.message == message, (
            f"Expected message {message!r}, got {response.message!r}\n{response}"
        )
    if model is None:
        return None
    try:
        return model.model_validate(response.body)
    except ValidationError as error:
        validation_error = error
    # Failing outside the except block avoids printing the error twice.
    pytest.fail(
        f"Response does not match {model.__name__} contract:\n"
        f"{validation_error}\n{response}"
    )


def assert_response_time(response: ApiResponse, max_ms: float) -> None:
    __tracebackhide__ = True
    assert response.elapsed_ms <= max_ms, (
        f"Response took {response.elapsed_ms:.0f} ms, SLA is {max_ms} ms\n{response}"
    )
