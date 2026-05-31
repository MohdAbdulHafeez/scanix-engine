class GoalEngine:

    @staticmethod
    def _safe_get(
        data,
        *keys,
        default=None
    ):

        current = data

        for key in keys:

            if not isinstance(
                current,
                dict
            ):
                return default

            current = current.get(
                key
            )

            if current is None:
                return default

        return current

    @staticmethod
    def _clamp(
        value
    ):

        return max(
            0,
            min(
                100,
                round(value)
            )
        )

    @staticmethod
    def evaluate(

        ingredients_result,
        nutrition_result,
        trust_result

    ):

        ingredient_score = (
            GoalEngine._safe_get(
                ingredients_result,
                "score",
                "score",
                default=50
            )
        )

        nutrition_score = (
            GoalEngine._safe_get(
                nutrition_result,
                "nutrition_score",
                "nutrition_score",
                default=50
            )
        )

        trust_score = (
            GoalEngine._safe_get(
                trust_result,
                "trust_score",
                "trust_score",
                default=50
            )
        )

        glycemic_risk = (
            GoalEngine._safe_get(
                nutrition_result,
                "glycemic",
                "risk",
                default="UNKNOWN"
            )
        )

        heart_status = (
            GoalEngine._safe_get(
                nutrition_result,
                "heart_health",
                "status",
                default="UNKNOWN"
            )
        )

        additives = (
            ingredients_result.get(
                "additives",
                []
            )
        )

        additive_count = len(
            additives
        )

        # ====================================
        # Data Extraction for Upgrades
        # ====================================

        ingredients_list = (
            ingredients_result.get(
                "ingredients",
                []
            )
        )

        nutrients = (

            nutrition_result.get(
                "nutrients",
                {}
            )

        )

        protein = float(

            nutrients.get(
                "protein",

                nutrition_result.get(
                    "protein",
                    0
                )

            ) or 0

        )

        fiber = float(

            nutrients.get(
                "fiber",

                nutrition_result.get(
                    "fiber",
                    0
                )

            ) or 0

        )

        sodium = float(

            nutrients.get(
                "sodium",

                nutrition_result.get(
                    "sodium",
                    0
                )

            ) or 0

        )

        sugar = float(

            nutrients.get(
                "sugar",

                nutrition_result.get(
                    "sugar",
                    0
                )

            ) or 0

        )

        calories = float(

            nutrients.get(
                "calories",

                nutrition_result.get(
                    "calories",
                    0
                )

            ) or 0

        )

        evidence_strength = (
            GoalEngine._safe_get(
                trust_result,
                "evidence_strength",
                default="MODERATE"
            )
        )

        base_score = (

            ingredient_score * 0.35

            +

            nutrition_score * 0.45

            +

            trust_score * 0.20

        )

        scores = {

            "weight_loss":
            base_score,

            "muscle_gain":
            base_score,

            "diabetes_friendly":
            base_score,

            "heart_friendly":
            base_score,

            "daily_consumption":
            base_score

        }

        reasons = {

            "weight_loss": [],
            "muscle_gain": [],
            "diabetes_friendly": [],
            "heart_friendly": [],
            "daily_consumption": []

        }

        # ====================================
        # Upgrade 3: Goal-Specific Logic
        # ====================================

        if protein >= 25:

            scores["muscle_gain"] += 25

            reasons[
                "muscle_gain"
            ].append(
                "Very high protein"
            )

        elif protein >= 15:

            scores["muscle_gain"] += 15

            reasons[
                "muscle_gain"
            ].append(
                "High protein"
            )

        elif protein >= 8:

            scores["muscle_gain"] += 8

            reasons[
                "muscle_gain"
            ].append(
                "Moderate protein"
            )

        if protein >= 15:

            scores["weight_loss"] += 5

            reasons[
                "weight_loss"
            ].append(
                "Supports satiety"
            )

        if fiber >= 5:

            scores["weight_loss"] += 8

            scores["diabetes_friendly"] += 8

            scores["heart_friendly"] += 5

            reasons[
                "weight_loss"
            ].append(
                "High fibre content"
            )

            reasons[
                "diabetes_friendly"
            ].append(
                "High fibre content"
            )

        if sodium >= 400:

            scores["heart_friendly"] -= 15

            reasons[
                "heart_friendly"
            ].append(
                "High sodium content"
            )

        if sugar >= 10:

            scores["diabetes_friendly"] -= 15

            reasons[
                "diabetes_friendly"
            ].append(
                "High sugar content"
            )

        # =====================================
        # Calorie Density Intelligence
        # =====================================

        if calories >= 400:

            scores["muscle_gain"] += 20

            reasons[
                "muscle_gain"
            ].append(
                "Very high calorie density"
            )

        elif calories >= 250:

            scores["muscle_gain"] += 12

            reasons[
                "muscle_gain"
            ].append(
                "Good calorie density"
            )

        elif calories >= 180:

            scores["muscle_gain"] += 6

            reasons[
                "muscle_gain"
            ].append(
                "Moderate calorie density"
            )

        if calories <= 120:

            scores["weight_loss"] += 15

            reasons[
                "weight_loss"
            ].append(
                "Low calorie density"
            )

        elif calories <= 180:

            scores["weight_loss"] += 8

            reasons[
                "weight_loss"
            ].append(
                "Moderately low calorie density"
            )

        if fiber >= 5 and sugar <= 5:

            scores["daily_consumption"] += 10

            reasons[
                "daily_consumption"
            ].append(
                "Suitable for daily use"
            )

        # ====================================
        # Upgrade 1: Ingredient Order Awareness
        # ====================================

        for ing in ingredients_list:

            if isinstance(
                ing,
                dict
            ):

                ing_name = str(
                    ing.get(
                        "name",
                        ""
                    )
                ).lower()

                pos = ing.get(
                    "position",
                    99
                )

            else:

                ing_name = str(
                    ing
                ).lower()

                pos = 99

            if "sugar" in ing_name and pos <= 3:

                scores["weight_loss"] -= 10
                scores["diabetes_friendly"] -= 20
                scores["daily_consumption"] -= 10

                reasons[
                    "diabetes_friendly"
                ].append(
                    "Sugar in top 3 ingredients"
                )

            if "palm oil" in ing_name and pos <= 5:

                scores["heart_friendly"] -= 15

                reasons[
                    "heart_friendly"
                ].append(
                    "Palm oil in top 5 ingredients"
                )

            if "hfcs" in ing_name or "high fructose" in ing_name:

                if pos <= 5:

                    scores["diabetes_friendly"] -= 20
                    scores["weight_loss"] -= 15

                    reasons[
                        "diabetes_friendly"
                    ].append(
                        "HFCS in top 5 ingredients"
                    )

        # ====================================
        # Upgrade 2: Additive Severity
        # ====================================

        high_risk_additives = 0

        moderate_risk_additives = 0

        for add in additives:

            if isinstance(
                add,
                dict
            ):

                risk = str(
                    add.get(
                        "risk",
                        "UNKNOWN"
                    )
                ).upper()

                if risk == "HIGH":

                    high_risk_additives += 1

                elif risk == "MODERATE":

                    moderate_risk_additives += 1

        if high_risk_additives >= 2:

            scores["daily_consumption"] -= 20
            scores["heart_friendly"] -= 15
            scores["weight_loss"] -= 10

            reasons[
                "daily_consumption"
            ].append(
                "Multiple high-risk additives"
            )

        elif high_risk_additives == 1 or moderate_risk_additives >= 3:

            scores["daily_consumption"] -= 10

        elif additive_count >= 5:

            scores["daily_consumption"] -= 15
            scores["heart_friendly"] -= 10

        elif additive_count >= 3:

            scores["daily_consumption"] -= 5

        # ====================================
        # Existing Risk Logic
        # ====================================

        if glycemic_risk == "HIGH":

            scores["weight_loss"] -= 20
            scores["diabetes_friendly"] -= 35
            scores["daily_consumption"] -= 15

            reasons[
                "weight_loss"
            ].append(
                "High glycemic impact"
            )

            reasons[
                "diabetes_friendly"
            ].append(
                "High blood sugar risk"
            )

        elif glycemic_risk == "MODERATE":

            scores["weight_loss"] -= 10
            scores["diabetes_friendly"] -= 15

        if heart_status == "HIGH":

            scores["heart_friendly"] -= 35
            scores["daily_consumption"] -= 10

        elif heart_status == "MODERATE":

            scores["heart_friendly"] -= 15

        # ====================================
        # Upgrade 4: Scientific Evidence Integration
        # ====================================

        if evidence_strength == "HIGH":

            for goal in scores:

                scores[goal] += 3

        elif evidence_strength == "LOW":

            for goal in scores:

                scores[goal] -= 5

        # ====================================
        # Final Adjustments & Verdicts
        # ====================================

        if trust_score >= 90:

            for goal in scores:

                scores[goal] += 2

        elif trust_score <= 50:

            for goal in scores:

                scores[goal] -= 5

        for goal in scores:

            if scores[goal] > 95:

                scores[goal] = 95

        for goal in scores:

            scores[goal] = (

                GoalEngine._clamp(

                    scores[goal]

                )

            )

        verdicts = {}

        for goal, score in scores.items():

            if score >= 85:

                verdict = "EXCELLENT"

            elif score >= 70:

                verdict = "GOOD"

            elif score >= 50:

                verdict = "AVERAGE"

            elif score >= 30:

                verdict = "POOR"

            else:

                verdict = "AVOID"

            verdicts[
                goal
            ] = verdict

        return {

            "scores":
            scores,

            "verdicts":
            verdicts,

            "reasons":
            reasons,

            "overall_score":

            round(

                sum(
                    scores.values()
                )

                /

                len(scores),

                1

            )

        }