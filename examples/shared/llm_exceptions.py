"""Exceptions for LLM provider integrations.

Provides a hierarchy of exceptions for different failure modes
when calling LLM APIs. Based on production patterns from
app/integrations/llm/exceptions.py.

Related: Chapter 4 (Infrastructure) — Error Handling
"""


class LLMException(Exception):
    """Base exception for LLM provider errors."""

    def __init__(
        self,
        message: str,
        provider: str | None = None,
        model: str | None = None,
        status_code: int | None = None,
        raw_response: dict | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.model = model
        self.status_code = status_code
        self.raw_response = raw_response

    def __str__(self) -> str:
        parts = [self.message]
        if self.provider:
            parts.append(f'provider={self.provider}')
        if self.model:
            parts.append(f'model={self.model}')
        if self.status_code:
            parts.append(f'status={self.status_code}')
        return ' '.join(parts)


class LLMAuthException(LLMException):
    """Raised when authentication fails (401)."""

    pass


class LLMInsufficientCreditsException(LLMException):
    """Raised when account has insufficient credits (402)."""

    pass


class LLMRateLimitException(LLMException):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        retry_after: int | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class LLMInvalidRequestException(LLMException):
    """Raised for invalid requests (400)."""

    pass


class LLMModelNotFoundError(LLMException):
    """Raised when the requested model is not found (404)."""

    pass


class LLMContextLengthException(LLMException):
    """Raised when context length is exceeded."""

    pass


class LLMContentFilterException(LLMException):
    """Raised when content is filtered by safety systems."""

    pass


class LLMServerException(LLMException):
    """Raised for server errors (5xx)."""

    pass


class LLMTimeoutException(LLMException):
    """Raised when request times out."""

    pass


def raise_for_status(
    status_code: int,
    message: str,
    provider: str | None = None,
    model: str | None = None,
    raw_response: dict | None = None,
    retry_after: int | None = None,
) -> None:
    """Raise appropriate exception based on HTTP status code.

    Maps HTTP status codes to specific exception types so callers
    can handle different failure modes appropriately.
    """
    kwargs = {
        'message': message,
        'provider': provider,
        'model': model,
        'status_code': status_code,
        'raw_response': raw_response,
    }

    if status_code == 401:
        raise LLMAuthException(**kwargs)
    elif status_code == 402:
        raise LLMInsufficientCreditsException(**kwargs)
    elif status_code == 429:
        raise LLMRateLimitException(retry_after=retry_after, **kwargs)
    elif status_code == 400:
        if raw_response:
            error_msg = str(raw_response).lower()
            if 'context' in error_msg or 'token' in error_msg:
                raise LLMContextLengthException(**kwargs)
            if 'content' in error_msg and (
                'filter' in error_msg or 'policy' in error_msg
            ):
                raise LLMContentFilterException(**kwargs)
        raise LLMInvalidRequestException(**kwargs)
    elif status_code == 404:
        raise LLMModelNotFoundError(**kwargs)
    elif 500 <= status_code < 600:
        raise LLMServerException(**kwargs)
    else:
        raise LLMException(**kwargs)
