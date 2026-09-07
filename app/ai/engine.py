from openai import OpenAI

from app.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from app.ai.schemas import TriageDecision
from app.core.config import settings


class AIEngine:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

        self.model = settings.openai_model

    def triage(self, message: str) -> TriageDecision:
        response = self.client.responses.parse(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_user_prompt(message),
            text_format=TriageDecision,
        )

        if response.output_parsed is None:
            raise ValueError("The AI did not return a valid triage decision.")

        return response.output_parsed