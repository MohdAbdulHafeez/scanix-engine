from modules.ai.food_explainer import (
    FoodExplainer
)


class AIService:

    @staticmethod
    def explain_product(

        ingredients_result,
        nutrition_result,
        trust_result

    ):

        explainer = (
            FoodExplainer()
        )

        explanation = (

            explainer.explain(

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result

            )

        )

        return {

            "success":
            True,

            "system":

            "SCANIX_AI_V1",

            "ingredients_score":

            ingredients_result
            .get(
                "score",
                {}
            )
            .get(
                "score"
            ),

            "nutrition_score":

            nutrition_result
            .get(
                "nutrition_score",
                {}
            )
            .get(
                "nutrition_score"
            ),

            "trust_score":

            trust_result
            .get(
                "trust_score",
                {}
            )
            .get(
                "trust_score"
            ),

            "food_explainer":

            explanation

        }