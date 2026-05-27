import re


class IngredientParser:

    @staticmethod
    def parse(
        raw_ingredients:str
    ):

        if not raw_ingredients:

            return []

        cleaned=re.sub(

            r"\([^)]*\)",

            "",

            raw_ingredients

        )

        ingredients=[

            item.strip()

            for item in cleaned.split(",")

            if item.strip()

        ]

        normalized=[]

        for ingredient in ingredients:

            value=ingredient.lower()

            value=value.replace(
                ".",
                ""
            )

            value=value.strip()

            normalized.append(
                value
            )

        return normalized