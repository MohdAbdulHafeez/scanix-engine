from modules.ai.calorie_engine import (
    CalorieEngine
)

from modules.ai.meal_generator import (
    MealGenerator
)

from modules.ai.shopping_list_engine import (
    ShoppingListEngine
)


class DietPlanner:

    # =====================================
    # User Profile
    # =====================================

    @staticmethod
    def build_profile(

        age,

        gender,

        weight,

        height,

        activity_level,

        goal,

        diet_type,

        budget

    ):

        return {

            "age": age,

            "gender": gender,

            "weight": weight,

            "height": height,

            "activity_level": activity_level,

            "goal": goal,

            "diet_type": diet_type,

            "budget": budget

        }

    # =====================================
    # Calories
    # =====================================

    @staticmethod
    def calculate_targets(

        profile

    ):

        calories = (

            CalorieEngine.calculate(

                age=profile["age"],

                gender=profile["gender"],

                weight=profile["weight"],

                height=profile["height"],

                activity_level=profile[
                    "activity_level"
                ],

                goal=profile["goal"]

            )

        )

        return calories

    # =====================================
    # Daily Plan
    # =====================================

    @staticmethod
    def daily_plan(

        profile,

        calories

    ):

        return (

            MealGenerator.generate_daily_plan(

                goal=profile["goal"],

                diet_type=profile[
                    "diet_type"
                ],

                calories=calories,

                budget=profile[
                    "budget"
                ]

            )

        )

    # =====================================
    # Weekly Plan
    # =====================================

    @staticmethod
    def weekly_plan(

        profile,

        calories

    ):

        return (

            MealGenerator.generate_weekly_plan(

                goal=profile["goal"],

                diet_type=profile[
                    "diet_type"
                ],

                calories=calories,

                budget=profile[
                    "budget"
                ]

            )

        )

    # =====================================
    # Shopping
    # =====================================

    @staticmethod
    def shopping_plan(

        profile,

        calories

    ):

        return (

            ShoppingListEngine.weekly_list(

                goal=profile["goal"],

                diet_type=profile[
                    "diet_type"
                ],

                budget=profile[
                    "budget"
                ],

                calories=calories

            )

        )

    # =====================================
    # Master Planner
    # =====================================

    @classmethod
    def build(

        cls,

        age,

        gender,

        weight,

        height,

        activity_level,

        goal,

        diet_type,

        budget="medium"

    ):

        profile = (

            cls.build_profile(

                age=age,

                gender=gender,

                weight=weight,

                height=height,

                activity_level=activity_level,

                goal=goal,

                diet_type=diet_type,

                budget=budget

            )

        )

        calories = (

            cls.calculate_targets(

                profile

            )

        )

        meal_plan = (

            MealGenerator.build(

                goal=goal,

                diet_type=diet_type,

                calories=calories,

                weight=weight

            )

        )

        shopping = (

            cls.shopping_plan(

                profile,

                calories

            )

        )

        return {

            "profile":

            profile,

            "daily_calorie_target":

            calories,

            "meal_plan":

            meal_plan,

            "shopping_plan":

            shopping

        }