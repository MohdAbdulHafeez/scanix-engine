from modules.ai.nutrition_agent import (
    NutritionAgent
)

from modules.ai.image_analyzer import (
    ImageAnalyzer
)

from modules.ai.voice_engine import (
    VoiceEngine
)


class AgentService:

    agent = NutritionAgent()

    image_analyzer = (
        ImageAnalyzer()
    )

    voice_engine = (
        VoiceEngine()
    )

    # =====================================
    # Chat
    # =====================================

    @classmethod
    def chat(

        cls,

        question,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None

    ):

        return cls.agent.ask(

            question=
            question,

            ingredients_result=
            ingredients_result,

            nutrition_result=
            nutrition_result,

            trust_result=
            trust_result,

            food_explainer=
            food_explainer

        )

    # =====================================
    # Image
    # =====================================

    @classmethod
    def image_chat(

        cls,

        image_path,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None

    ):

        image_analysis = (

            cls.image_analyzer
            .scan_product(

                image_path

            )

        )

        auto_ingredients,\
        auto_nutrition,\
        auto_trust = (

            cls
            ._build_intelligence_from_image(

                image_analysis

            )

        )

        return cls.agent.ask_image(

            image_analysis=
            image_analysis,

            ingredients_result=

            auto_ingredients,

            nutrition_result=

            auto_nutrition,

            trust_result=

            auto_trust,

            food_explainer=
            food_explainer

        )

    # =====================================
    # Voice
    # =====================================

    @classmethod
    def voice_chat(

        cls,

        audio_path,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None

    ):

        return (

            cls.voice_engine
            .voice_chat(

                audio_path=
                audio_path,

                nutrition_agent=
                cls.agent,

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result,

                food_explainer=
                food_explainer

            )

        )

    # =====================================
    # Multimodal
    # =====================================

    @classmethod
    def multimodal_chat(

        cls,

        question,

        image_path,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None

    ):

        image_analysis = (

            cls.image_analyzer
            .scan_product(

                image_path

            )

        )

        auto_ingredients,\
        auto_nutrition,\
        auto_trust = (

            cls
            ._build_intelligence_from_image(

                image_analysis

            )

        )

        return cls.agent.ask_multimodal(

            question=
            question,

            transcript=
            "",

            image_analysis=
            image_analysis,

            ingredients_result=

            auto_ingredients,

            nutrition_result=

            auto_nutrition,

            trust_result=

            auto_trust,

            food_explainer=
            food_explainer

        )

    # =====================================
    # Intelligence Builder
    # =====================================

    @classmethod
    def _build_intelligence_from_image(

        cls,

        image_analysis

    ):

        nutrition = image_analysis.get(
            "nutrition",
            {}
        )

        ingredients = image_analysis.get(
            "ingredients",
            []
        )

        additives = image_analysis.get(
            "additives",
            []
        )

        protein = float(
            nutrition.get(
                "protein",
                0
            ) or 0
        )

        fiber = float(
            nutrition.get(
                "fiber",
                0
            ) or 0
        )

        added_sugar = float(
            nutrition.get(
                "added_sugars",
                0
            ) or 0
        )

        nutrition_score = 60

        nutrition_score += protein * 2

        nutrition_score += fiber * 3

        nutrition_score -= added_sugar * 2

        nutrition_score = max(
            0,
            min(
                100,
                round(
                    nutrition_score
                )
            )
        )

        glycemic = "LOW"

        if added_sugar >= 10:

            glycemic = "HIGH"

        elif added_sugar >= 5:

            glycemic = "MODERATE"

        ingredients_result = {

            "score": {

                "score":

                max(
                    50,
                    100 - (
                        len(additives) * 5
                    )
                )

            },

            "additives":

            additives

        }

        nutrition_result = {

            "nutrition_score": {

                "nutrition_score":

                nutrition_score

            },

            "glycemic": {

                "risk":

                glycemic

            },

            "heart_health": {

                "status":

                "LOW"

            }

        }

        trust_result = {

            "trust_score": {

                "trust_score":

                image_analysis.get(
                    "confidence",
                    80
                )

            }

        }

        return (

            ingredients_result,

            nutrition_result,

            trust_result

        )