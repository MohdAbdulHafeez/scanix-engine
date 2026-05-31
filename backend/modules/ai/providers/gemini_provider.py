import os
import time

from google import genai

from modules.ai.providers.base import (
    BaseLLMProvider
)


class GeminiProvider(
    BaseLLMProvider
):

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY missing"
            )

        model = os.getenv(

            "AI_PRIMARY_MODEL",

            "gemini-2.5-flash"

        )

        super().__init__(
            model=model
        )

        self.client = (
            genai.Client(
                api_key=api_key
            )
        )

        self.max_retries = int(

            os.getenv(

                "AI_MAX_RETRIES",

                3

            )

        )

    def generate(

        self,
        prompt: str,
        temperature: float = 0.3

    ) -> str:

        MODELS = [

            self.model,

            "gemini-2.5-flash",

            "gemini-2.0-flash"

        ]

        last_error = None

        for current_model in MODELS:

            try:

                response = (

                    self.client.models.generate_content(

                        model=current_model,

                        contents=prompt

                    )

                )

                return (
                    response.text
                )

            except Exception as e:

                last_error = e

                error_msg = str(e).lower()

                if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:

                    continue

                time.sleep(1)

        raise last_error

    def generate_json(

        self,
        prompt: str,
        temperature: float = 0.3

    ):

        return self.generate(

            prompt=prompt,

            temperature=temperature

        )

    def health_check(

        self

    ) -> bool:

        MODELS = [

            self.model,

            "gemini-2.5-flash",

            "gemini-2.0-flash"

        ]

        for current_model in MODELS:

            try:

                response = (

                    self.client.models.generate_content(

                        model=current_model,

                        contents="ping"

                    )

                )

                return bool(
                    response.text
                )

            except Exception as e:

                error_msg = str(e).lower()

                if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:

                    continue

                return False

        return False