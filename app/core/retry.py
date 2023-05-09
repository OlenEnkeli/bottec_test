import logging

from tenacity import (
    retry,
    wait_exponential_jitter,
    RetryCallState,
    stop_after_attempt,
)


def _retry_logging(retry_state: RetryCallState) -> None:
    if (not retry_state.outcome) or (not retry_state.fn):
        return

    exception = retry_state.outcome.exception()

    logging.error(
        f'Function {retry_state.fn.__name__} failed, '
        f'{repr(exception)}. '
        f'Retrying attempt: {retry_state.attempt_number},'
        f'time_spend: {retry_state.idle_for}'
    )


api_retry = retry(
    wait=wait_exponential_jitter(1, 20),
    stop=stop_after_attempt(2),
    after=_retry_logging,
)
