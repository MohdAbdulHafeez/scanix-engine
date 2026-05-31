from typing import Dict


class CalorieEngine:

    ACTIVITY_FACTORS = {

        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9

    }

    GOAL_ADJUSTMENTS = {

        "weight_loss": -500,
        "fat_loss": -400,
        "recomposition": -150,
        "maintenance": 0,
        "muscle_gain": 350,
        "aggressive_muscle_gain": 500

    }

    # =====================================
    # Validation
    # =====================================

    @staticmethod
    def validate_inputs(

        age: int,
        weight: float,
        height: float,
        gender: str,
        activity_level: str

    ):

        if age <= 0:
            raise ValueError("Invalid age")

        if weight <= 0:
            raise ValueError("Invalid weight")

        if height <= 0:
            raise ValueError("Invalid height")

        if gender.lower() not in {

            "male",
            "female"

        }:
            raise ValueError("Invalid gender")

        if activity_level not in (

            CalorieEngine.ACTIVITY_FACTORS

        ):
            raise ValueError(

                "Invalid activity level"

            )

    # =====================================
    # BMR
    # Mifflin-St Jeor
    # =====================================

    @staticmethod
    def calculate_bmr(

        age: int,
        weight: float,
        height: float,
        gender: str

    ) -> float:

        if gender.lower() == "male":

            return (

                10 * weight
                + 6.25 * height
                - 5 * age
                + 5

            )

        return (

            10 * weight
            + 6.25 * height
            - 5 * age
            - 161

        )

    # =====================================
    # TDEE
    # =====================================

    @classmethod
    def calculate_tdee(

        cls,
        bmr: float,
        activity_level: str

    ) -> float:

        factor = cls.ACTIVITY_FACTORS.get(

            activity_level,

            1.55

        )

        return round(

            bmr * factor,

            0

        )

    # =====================================
    # Goal Calories
    # =====================================

    @classmethod
    def calculate_goal_calories(

        cls,
        tdee: float,
        goal: str

    ) -> int:

        adjustment = (

            cls.GOAL_ADJUSTMENTS.get(

                goal,

                0

            )

        )

        return int(

            tdee + adjustment

        )

    # =====================================
    # Water Target
    # =====================================

    @staticmethod
    def calculate_water_target(

        weight: float

    ) -> float:

        return round(

            weight * 0.04,

            1

        )

    # =====================================
    # Macros
    # =====================================

    @staticmethod
    def calculate_macros(

        calories: int,
        goal: str

    ) -> Dict:

        if goal in {

            "muscle_gain",
            "aggressive_muscle_gain"

        }:

            protein_pct = 0.30
            carbs_pct = 0.45
            fats_pct = 0.25

        elif goal in {

            "weight_loss",
            "fat_loss"

        }:

            protein_pct = 0.35
            carbs_pct = 0.35
            fats_pct = 0.30

        else:

            protein_pct = 0.30
            carbs_pct = 0.40
            fats_pct = 0.30

        protein = (

            calories
            * protein_pct

        ) / 4

        carbs = (

            calories
            * carbs_pct

        ) / 4

        fats = (

            calories
            * fats_pct

        ) / 9

        return {

            "protein_g":

            round(protein),

            "carbs_g":

            round(carbs),

            "fat_g":

            round(fats)

        }

    # =====================================
    # Meal Timing
    # =====================================

    @staticmethod
    def meal_timing():

        return {

            "breakfast":

            "07:00 - 09:00",

            "mid_morning":

            "10:30 - 11:30",

            "lunch":

            "13:00 - 14:30",

            "evening_snack":

            "16:30 - 18:00",

            "dinner":

            "19:30 - 21:00"

        }

    @classmethod
    def calculate(

        cls,

        age: int,
        gender: str,
        weight: float,
        height: float,
        activity_level: str,
        goal: str

    ) -> int:

        cls.validate_inputs(

            age,
            weight,
            height,
            gender,
            activity_level

        )

        bmr = cls.calculate_bmr(

            age,
            weight,
            height,
            gender

        )

        tdee = cls.calculate_tdee(

            bmr,
            activity_level

        )

        calories = cls.calculate_goal_calories(

            tdee,
            goal

        )

        return calories

    # =====================================
    # Master Planner
    # =====================================

    @classmethod
    def build_targets(

        cls,

        age: int,
        weight: float,
        height: float,
        gender: str,

        activity_level: str,
        goal: str

    ):

        cls.validate_inputs(

            age,
            weight,
            height,
            gender,
            activity_level

        )

        bmr = cls.calculate_bmr(

            age,
            weight,
            height,
            gender

        )

        tdee = cls.calculate_tdee(

            bmr,
            activity_level

        )

        calories = (

            cls.calculate_goal_calories(

                tdee,
                goal

            )

        )

        macros = (

            cls.calculate_macros(

                calories,
                goal

            )

        )

        return {

            "bmr":

            round(bmr),

            "tdee":

            round(tdee),

            "target_calories":

            calories,

            "water_target_liters":

            cls.calculate_water_target(

                weight

            ),

            "meal_timing":

            cls.meal_timing(),

            **macros

        }