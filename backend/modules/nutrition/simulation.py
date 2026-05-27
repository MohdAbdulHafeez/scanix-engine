class NutritionSimulation:

    @staticmethod
    def simulate(

        nutrition

    ):

        calories = nutrition.get(
            "calories",
            0
        )

        protein = nutrition.get(
            "protein",
            0
        )

        sugar = nutrition.get(
            "sugar",
            0
        )

        fat = nutrition.get(
            "fat",
            0
        )

        monthly_calories = (
            calories * 30
        )

        yearly_calories = (
            calories * 365
        )

        # --------------------------------
        # WEIGHT PROJECTION
        # --------------------------------

        maintenance_calories = (
            2200 * 365
        )

        calorie_surplus = (
            yearly_calories -
            maintenance_calories
        )

        projected_weight_gain = round(

            calorie_surplus / 7700,

            1

        )

        projected_weight_gain = max(

            -25,

            min(
                25,
                projected_weight_gain
            )

        )

        # --------------------------------
        # OBESITY RISK
        # --------------------------------

        obesity_score = 0

        if calories >= 500:
            obesity_score += 1

        if sugar >= 25:
             obesity_score += 1

        if fat >= 20:
            obesity_score += 1

        if yearly_calories >= 220000:
             obesity_score += 1

        if obesity_score >= 4:

            obesity_risk = "HIGH"

        elif obesity_score >= 2:

            obesity_risk = "MODERATE"

        else:

            obesity_risk = "LOW"
        # --------------------------------
        # MUSCLE SUPPORT
        # --------------------------------

        muscle_support = (

            protein >= 20

            and

            calories >= 250

        )

        # --------------------------------
        # DIABETES RISK
        # --------------------------------

        diabetes_risk = (

            "HIGH"

            if sugar >= 25

            else

            "MODERATE"

            if sugar >= 12

            else

            "LOW"

        )

        # --------------------------------
        # FATIGUE RISK
        # --------------------------------

        fatigue_risk = (

            "HIGH"

            if calories < 120

            else

            "MODERATE"

            if calories < 180

            else

            "LOW"

        )

        return {

            "monthly_calories":
            monthly_calories,

            "yearly_calories":
            yearly_calories,

            "projected_weight_change_kg":
            projected_weight_gain,

            "obesity_risk":
            obesity_risk,

            "diabetes_risk":
            diabetes_risk,

            "fatigue_risk":
            fatigue_risk,

            "muscle_support":
            muscle_support

        }