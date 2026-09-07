import time

from openai import OpenAI

from app.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from app.ai.result import AIResult
from app.ai.schemas import TriageDecision
from app.ai.usage import calculate_cost
from app.core.config import settings


class AIEngine:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )
        self.model = settings.openai_model
        self.max_retries = 2

    def triage(self, message: str) -> AIResult:
        if not message or not message.strip():
            raise ValueError("Customer message cannot be empty.")

        start_time = time.perf_counter()

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.responses.parse(
                    model=self.model,
                    instructions=SYSTEM_PROMPT,
                    input=build_user_prompt(message),
                    text_format=TriageDecision,
                )

                if response.output_parsed is None:
                    raise ValueError(
                        "The AI did not return a valid triage decision."
                    )

                latency_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                usage = getattr(response, "usage", None)

                input_tokens = getattr(
                    usage,
                    "input_tokens",
                    None,
                )

                output_tokens = getattr(
                    usage,
                    "output_tokens",
                    None,
                )

                total_tokens = getattr(
                    usage,
                    "total_tokens",
                    None,
                )

                estimated_cost = calculate_cost(
                    input_tokens,
                    output_tokens,
                )

                return AIResult(
                    decision=response.output_parsed,
                    latency_ms=latency_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=total_tokens,
                    estimated_cost_usd=estimated_cost,
                )

            except Exception as exc:
                last_error = exc

                if attempt < self.max_retries:
                    time.sleep(1)

        raise RuntimeError(
            f"AI service request failed after "
            f"{self.max_retries + 1} attempts: {last_error}"
        ) from last_error