import os

from modules.ai.providers.gemini_provider import (
    GeminiProvider
)

from modules.ai.conversation_memory import (
    ConversationMemory
)

from modules.ai.multimodal_context import (
    MultimodalContext
)

from modules.ai.goal_engine import (
    GoalEngine
)

from modules.ai.risk_forecast import (
    RiskForecast
)

from modules.ai.recommendation_engine import (
    RecommendationEngine
)


class NutritionAgent:

    def __init__(

        self,

        memory=None

    ):

        self.llm = (
            GeminiProvider()
        )

        self.memory = (

            memory

            or

            ConversationMemory()

        )

    # ====================================
    # Main Agent Entry
    # ====================================

    def ask(

        self,

        question,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None,

        image_analysis=None

    ):

        self.memory.add_message(

            role="user",

            content=question

        )

        goal_result = (

            GoalEngine.evaluate(

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result

            )

        )

        risk_result = (

            RiskForecast.forecast(

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result

            )

        )

        recommendation_result = (

            RecommendationEngine.generate(

                goal_result=
                goal_result,

                risk_result=
                risk_result,

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result,

                user_profile=

                self.memory.get_profile()

            )

        )

        # ====================================
        # Upgrade 1: Food Explainer Priority
        # ====================================

        if not food_explainer:

            food_explainer = {}

        food_explainer["agent_priority"] = True

        context = (

            MultimodalContext.build(

                question=
                question,

                image_analysis=
                image_analysis,

                memory=
                self.memory,

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result,

                food_explainer=
                food_explainer,

                goal_result=
                goal_result,

                risk_result=
                risk_result,

                recommendation_result=
                recommendation_result

            )

        )

        prompt = (

            MultimodalContext.build_prompt(

                context

            )

        )

        response = (

            self.llm.generate(

                prompt

            )

        )

        self.memory.add_message(

            role="assistant",

            content=response

        )

        self.memory.update_state(

            last_recommendation=

            recommendation_result.get(

                "daily_consumption_verdict"

            ),

            last_risk_level=

            risk_result.get(

                "overall_label"

            )

        )

        confidence = self._confidence(

            goal_result,

            risk_result,

            trust_result,

            food_explainer

        )

        return {

            "answer":
            response,

            "confidence":
            confidence,

            "goal_analysis":
            goal_result,

            "risk_forecast":
            risk_result,

            "recommendation":
            recommendation_result,

            "memory_session":

            self.memory
            .get_session_id(),

            # ====================================
            # Upgrade 3: Agent Metadata
            # ====================================

            "agent_version":
            "1.0",

            "reasoning_sources": [

                "goal_engine",

                "risk_forecast",

                "recommendation_engine",

                "memory",

                "food_explainer"

            ]

        }

    # ====================================
    # Voice Nutritionist
    # ====================================

    def ask_voice(

        self,

        transcript,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None,

        image_analysis=None

    ):

        if (

            not ingredients_result and

            not nutrition_result and

            not trust_result and

            not image_analysis

        ):

            return {

                "answer":

                (
                    "I need the food product information "
                    "or an image before I can analyze it."
                ),

                "confidence": 100

            }

        return self.ask(

            question=transcript,

            ingredients_result=
            ingredients_result,

            nutrition_result=
            nutrition_result,

            trust_result=
            trust_result,

            food_explainer=
            food_explainer,

            image_analysis=
            image_analysis

        )

    # ====================================
    # Image Nutritionist
    # ====================================

    def ask_image(

        self,

        image_analysis,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None

    ):

        question = """

Analyze this food product
and provide nutrition guidance.

"""

        return self.ask(

            question=
            question,

            image_analysis=
            image_analysis,

            ingredients_result=
            ingredients_result,

            nutrition_result=
            nutrition_result,

            trust_result=
            trust_result,

            food_explainer=
            food_explainer

        )

    # ====================================
    # Multimodal
    # ====================================

    def ask_multimodal(

        self,

        question,

        transcript,

        image_analysis,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None

    ):

        merged = f"""

Question:
{question}

Voice:
{transcript}

"""

        return self.ask(

            question=
            merged,

            image_analysis=
            image_analysis,

            ingredients_result=
            ingredients_result,

            nutrition_result=
            nutrition_result,

            trust_result=
            trust_result,

            food_explainer=
            food_explainer

        )

    # ====================================
    # Confidence Engine
    # ====================================

    def _confidence(

        self,

        goal_result,

        risk_result,

        trust_result,

        food_explainer=None

    ):

        goal_score = (

            goal_result.get(

                "overall_score",

                50

            )

        )

        trust_score = (

            trust_result

            .get(
                "trust_score",
                {}
            )

            .get(
                "trust_score",
                50
            )

        )

        risk_score = (

            100

            -

            risk_result.get(

                "overall_risk",

                50

            )

        )

        # ====================================
        # Upgrade 2: RAG Confidence Fusion
        # ====================================

        rag_confidence = 75

        if food_explainer:

            rag_confidence = (

                food_explainer.get(
                    "evidence_strength_score",
                    75
                )

            )

        return round(

            (

                goal_score

                +

                trust_score

                +

                risk_score

                +

                rag_confidence

            )

            / 4,

            1

        )

