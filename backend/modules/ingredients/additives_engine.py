from modules.ingredients.data.additives_registry import (
ADDITIVES
)


class AdditivesEngine:

    @staticmethod
    def detect(
        ingredients
    ):

        detected=[]

        for ingredient in ingredients:

            value=ingredient.lower()

            for additive in ADDITIVES:

                code=additive.get(
                    "number",
                    ""
                ).lower()

                name=additive.get(
                    "name",
                    ""
                ).lower()

                if (

                    code in value

                    or

                    name in value

                ):

                    detected.append({

                        "number":
                        additive.get(
                            "number"
                        ),

                        "name":
                        additive.get(
                            "name"
                        ),

                        "risk":
                        additive.get(
                            "risk"
                        ),

                        "description":
                        additive.get(
                            "description"
                        ),

                        "use":
                        additive.get(
                            "use"
                        )

                    })

        unique=[]

        seen=set()

        for additive in detected:

            key=additive["number"]

            if key not in seen:

                unique.append(
                    additive
                )

                seen.add(key)

        return unique