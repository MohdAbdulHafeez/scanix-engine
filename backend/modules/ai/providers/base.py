from abc import (
    ABC,
    abstractmethod
)

from typing import (
    Dict,
    Any,
    Optional
)


class BaseLLMProvider(
    ABC
):

    def __init__(

        self,
        model: str

    ):

        self.model = model

    @property
    def provider_name(

        self

    ) -> str:

        return self.__class__.__name__

    @abstractmethod
    def generate(

        self,
        prompt: str,
        temperature: float = 0.3

    ) -> str:

        pass

    @abstractmethod
    def health_check(

        self

    ) -> bool:

        pass

    def generate_json(

        self,
        prompt: str,
        temperature: float = 0.3

    ):

        return self.generate(

            prompt=prompt,

            temperature=temperature

        )

    def metadata(

        self

    ) -> Dict[str, Any]:

        return {

            "provider":
            self.provider_name,

            "model":
            self.model

        }