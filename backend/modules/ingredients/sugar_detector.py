HIGH_SUGAR_TERMS=[

"sugar",
"glucose",
"fructose",
"syrup",
"corn syrup",
"dextrose",
"maltose",
"caramel",
"sucrose",
"cane sugar",
"brown sugar",
"invert sugar",
"molasses",
"honey"

]


class SugarDetector:

    @staticmethod
    def detect(
        ingredients
    ):

        found=[]

        for ingredient in ingredients:

            value=ingredient.lower()

            for sugar in HIGH_SUGAR_TERMS:

                if sugar in value:

                    found.append(
                        ingredient
                    )

        score=min(
            len(found)*15,
            100
        )

        return {

            "detected":
            found,

            "count":
            len(found),

            "sugar_score":
            score,

            "risk":
            (
                "HIGH"
                if score>=50
                else "LOW"
            )

        }