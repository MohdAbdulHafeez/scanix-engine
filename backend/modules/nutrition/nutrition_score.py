from modules.nutrition.nutrition_registry import (
    NUTRITION_THRESHOLDS
)


class NutritionScore:

    @staticmethod
    def compute(

        nutrition,
        macros,
        micros,
        glycemic,
        heart,
        bmi_analysis

    ):

        score = 100

        protein = nutrition.get(
            "protein",
            0
        )

        fiber = nutrition.get(
            "fiber",
            0
        )

        sugar = nutrition.get(
            "sugar",
            0
        )

        sodium = nutrition.get(
            "sodium",
            0
        )

        saturated_fat = nutrition.get(
            "saturated_fat",
            0
        )

        calories = nutrition.get(
            "calories",
            0
        )

        # --------------------------------
        # POSITIVE FACTORS
        # --------------------------------

        if protein >= 20:
            score += 8

        elif protein >= 10:
            score += 4

        if fiber >= 8:
            score += 10

        elif fiber >= 4:
            score += 5

        micronutrient_bonus = (

            micros[
                "micronutrient_richness"
            ]

            * 2

        )

        score += micronutrient_bonus

        # --------------------------------
        # SUGAR PENALTIES
        # --------------------------------

        if sugar >= 25:
            score -= 18

        elif sugar >= 12:
            score -= 10

        # --------------------------------
        # SODIUM PENALTIES
        # --------------------------------

        if sodium >= 700:
            score -= 15

        elif sodium >= 350:
            score -= 8

        # --------------------------------
        # SATURATED FAT
        # --------------------------------

        if saturated_fat >= 10:
            score -= 15

        elif saturated_fat >= 5:
            score -= 8

        # --------------------------------
        # CALORIE PENALTIES
        # --------------------------------

        if calories >= 500:
            score -= 10

        elif calories <= 120:
            score -= 6

        # --------------------------------
        # GLYCEMIC RISK
        # --------------------------------

        if glycemic["risk"] == "HIGH":
            score -= 12

        elif glycemic["risk"] == "MODERATE":
            score -= 6

        # --------------------------------
        # HEART HEALTH
        # --------------------------------

        if heart["status"] == "HIGH":
            score -= 15

        elif heart["status"] == "MODERATE":
            score -= 8

        # --------------------------------
        # BMI-AWARE PENALTIES
        # --------------------------------

        bmi_category = bmi_analysis[
            "category"
        ]

        if bmi_category == "OVERWEIGHT":

            if sugar >= 12:
                score -= 5

            if calories >= 300:
                score -= 4

        elif bmi_category == "OBESE":

            if sugar >= 10:
                score -= 8

            if calories >= 250:
                score -= 8

            if saturated_fat >= 5:
                score -= 6

        # --------------------------------
        # NORMALIZATION
        # --------------------------------

        score = max(
            0,
            min(
                100,
                round(score)
            )
        )

        # --------------------------------
        # GRADING
        # --------------------------------

        if score >= 90:

            grade = "A+"

        elif score >= 80:

            grade = "A"

        elif score >= 70:

            grade = "B"

        elif score >= 55:

            grade = "C"

        elif score >= 40:

            grade = "D"

        else:

            grade = "F"

        ratings = {

            "A+":
            "Excellent",

            "A":
            "Healthy",

            "B":
            "Balanced",

            "C":
            "Moderate",

            "D":
            "Poor",

            "F":
            "Harmful"

        }

        return {

            "nutrition_score":
            score,

            "grade":
            grade,

            "rating":
            ratings[grade]

        }