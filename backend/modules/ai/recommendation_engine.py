class RecommendationEngine:

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
    def _daily_verdict(

        score

    ):

        if score >= 85:

            return "RECOMMENDED"

        if score >= 70:

            return "GENERALLY_ACCEPTABLE"

        if score >= 50:

            return "LIMITED_CONSUMPTION"

        if score >= 30:

            return "OCCASIONAL_ONLY"

        return "AVOID"

    @staticmethod
    def generate(

        goal_result,
        risk_result,
        ingredients_result,
        nutrition_result,
        trust_result,
        user_profile=None

    ):

        user_profile = (

            user_profile

            or

            {}

        )

        overall_goal_score = (

            goal_result.get(
                "overall_score",
                50
            )

        )

        overall_risk = (

            risk_result.get(
                "overall_risk",
                50
            )

        )

        ingredient_score = (

            RecommendationEngine._safe_get(

                ingredients_result,

                "score",

                "score",

                default=50

            )

        )

        nutrition_score = (

            RecommendationEngine._safe_get(

                nutrition_result,

                "nutrition_score",

                "nutrition_score",

                default=50

            )

        )

        trust_score = (

            RecommendationEngine._safe_get(

                trust_result,

                "trust_score",

                "trust_score",

                default=50

            )

        )

        recommendations = []

        warnings = []

        strengths = []

        alternatives = []

        action_plan = []

        # ==================================
        # Strength Analysis
        # ==================================

        if trust_score >= 80:

            strengths.append(

                "Strong trust and compliance profile"

            )

        if nutrition_score >= 80:

            strengths.append(

                "Good nutrition quality"

            )

        if ingredient_score >= 80:

            strengths.append(

                "High ingredient quality"

            )

        # ==================================
        # Risk Analysis
        # ==================================

        if overall_risk >= 70:

            warnings.append(

                "Frequent consumption is not advised"

            )

            action_plan.append(

                "Reserve for occasional use"

            )

        elif overall_risk >= 50:

            warnings.append(

                "Consume in moderation"

            )

            action_plan.append(

                "Limit serving frequency"

            )

        else:

            action_plan.append(

                "Can fit into a balanced diet"

            )

        # ==================================
        # Goal Analysis
        # ==================================

        weight_loss = (

            goal_result.get(
                "scores",
                {}
            )

            .get(
                "weight_loss",
                50
            )

        )

        muscle_gain = (

            goal_result.get(
                "scores",
                {}
            )

            .get(
                "muscle_gain",
                50
            )

        )

        diabetes = (

            goal_result.get(
                "scores",
                {}
            )

            .get(
                "diabetes_friendly",
                50
            )

        )

        heart = (

            goal_result.get(
                "scores",
                {}
            )

            .get(
                "heart_friendly",
                50
            )

        )

        if weight_loss < 40:

            recommendations.append(

                "Not ideal for fat loss goals"

            )

            alternatives.extend([

                "Greek Yogurt",

                "Roasted Chickpeas",

                "High Protein Snacks"

            ])

        if muscle_gain >= 70:

            recommendations.append(

                "Reasonably compatible with muscle gain"

            )

        if diabetes < 40:

            warnings.append(

                "Poor suitability for blood sugar management"

            )

            alternatives.extend([

                "Unsweetened Nuts",

                "High Fibre Snacks"

            ])

        if heart < 40:

            warnings.append(

                "Not ideal for cardiovascular health"

            )

        # ==================================
        # User Context
        # ==================================

        goal = (

            user_profile.get(
                "goal"
            )
        )

        if goal:

            recommendations.append(

                f"User goal detected: {goal}"

            )

        # ==================================
        # Daily Consumption Score
        # ==================================

        daily_score = round(

            (

                overall_goal_score

                +

                (100 - overall_risk)

            )

            / 2,

            1

        )

        daily_verdict = (

            RecommendationEngine
            ._daily_verdict(

                daily_score

            )

        )

        confidence = round(

            (

                ingredient_score

                +

                nutrition_score

                +

                trust_score

            )

            / 3,

            1

        )

        return {

            "daily_consumption_score":

            daily_score,

            "daily_consumption_verdict":

            daily_verdict,

            "strengths":

            strengths,

            "warnings":

            warnings,

            "recommendations":

            recommendations,

            "better_alternatives":

            list(

                set(
                    alternatives
                )

            ),

            "action_plan":

            action_plan,

            "confidence":

            confidence

        }