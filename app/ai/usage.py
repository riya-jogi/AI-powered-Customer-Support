from typing import Final


# Price per 1 million tokens.
INPUT_PRICE_PER_MILLION: Final[float] = 0.20
OUTPUT_PRICE_PER_MILLION: Final[float] = 1.20


def calculate_cost(
    input_tokens: int | None,
    output_tokens: int | None,
) -> float | None:
    if input_tokens is None or output_tokens is None:
        return None

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_PRICE_PER_MILLION

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_PRICE_PER_MILLION

    return input_cost + output_cost