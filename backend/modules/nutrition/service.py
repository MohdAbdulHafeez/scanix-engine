from modules.nutrition.macros import (
    MacroAnalyzer
)

from modules.nutrition.micros import (
    MicroAnalyzer
)

from modules.nutrition.daily_rdi_engine import (
    DailyRDIEngine
)

from modules.nutrition.glycemic_engine import (
    GlycemicEngine
)

from modules.nutrition.heart_health_engine import (
    HeartHealthEngine
)

from modules.nutrition.body_goal_engine import (
    BodyGoalEngine
)

from modules.nutrition.nutrition_ai_reasoner import (
    NutritionAIReasoner
)

from modules.nutrition.nutrition_score import (
    NutritionScore
)

from modules.nutrition.density import (
    HealthDensity
)

from modules.nutrition.simulation import (
    NutritionSimulation
)

from modules.nutrition.bmi_engine import (
    BMIEngine
)


class NutritionService:

    @staticmethod
    def analyze(

        nutrition,
        bmi=22

    ):

        macros = MacroAnalyzer.analyze(
            nutrition
        )

        micros = MicroAnalyzer.analyze(
            nutrition
        )

        rdi = DailyRDIEngine.analyze(
            nutrition
        )

        glycemic = (
            GlycemicEngine.analyze(
                nutrition
            )
        )

        heart = (
            HeartHealthEngine.analyze(
                nutrition
            )
        )

        goals = (
            BodyGoalEngine.analyze(
                nutrition
            )
        )

        density = (
            HealthDensity.analyze(
                nutrition
            )
        )

        simulation = (
            NutritionSimulation.simulate(
                nutrition
            )
        )

        bmi_analysis = (
            BMIEngine.analyze(
                bmi
            )
        )

        nutrition_score = (
    NutritionScore.compute(

        nutrition=
        nutrition,

        macros=
        macros,

        micros=
        micros,

        glycemic=
        glycemic,

        heart=
        heart,

        bmi_analysis=
        bmi_analysis

        )
)

        ai_reasoning = (
            NutritionAIReasoner.explain(

                score=
                nutrition_score[
                    "nutrition_score"
                ],

                glycemic=
                glycemic,

                heart=
                heart,

                goals=
                goals

            )
        )

        return {

            "macros":
            macros,

            "micros":
            micros,

            "daily_rdi":
            rdi,

            "glycemic":
            glycemic,

            "heart_health":
            heart,

            "body_goals":
            goals,

            "bmi":
            bmi_analysis,

            "nutrition_score":
            nutrition_score,

            "health_density":
            density,

            "simulation":
            simulation,

            "ai_reasoning":
            ai_reasoning

        }