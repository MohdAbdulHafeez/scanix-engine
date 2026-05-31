class RiskForecast:

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
    def _risk_label(

        score

    ):

        if score >= 80:

            return "VERY_HIGH"

        if score >= 60:

            return "HIGH"

        if score >= 40:

            return "MODERATE"

        if score >= 20:

            return "LOW"

        return "VERY_LOW"

    @staticmethod
    def forecast(

        ingredients_result,
        nutrition_result,
        trust_result

    ):

        ingredient_score = (

            RiskForecast._safe_get(

                ingredients_result,

                "score",

                "score",

                default=50

            )

        )

        nutrition_score = (

            RiskForecast._safe_get(

                nutrition_result,

                "nutrition_score",

                "nutrition_score",

                default=50

            )

        )

        trust_score = (

            RiskForecast._safe_get(

                trust_result,

                "trust_score",

                "trust_score",

                default=50

            )

        )

        glycemic_risk = (

            RiskForecast._safe_get(

                nutrition_result,

                "glycemic",

                "risk",

                default="UNKNOWN"

            )

        )

        heart_risk = (

            RiskForecast._safe_get(

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

        obesity_risk = 20

        diabetes_risk = 20

        cardiovascular_risk = 20

        inflammation_risk = 20

        daily_use_risk = 20

        drivers = []

        # ==========================
        # Glycemic Risk
        # ==========================

        if glycemic_risk == "HIGH":

            obesity_risk += 30

            diabetes_risk += 45

            daily_use_risk += 25

            drivers.append(

                "High glycemic impact"

            )

        elif glycemic_risk == "MODERATE":

            obesity_risk += 15

            diabetes_risk += 20

        # ==========================
        # Heart Risk
        # ==========================

        if heart_risk == "HIGH":

            cardiovascular_risk += 45

            inflammation_risk += 20

            daily_use_risk += 15

            drivers.append(

                "Elevated cardiovascular risk"

            )

        elif heart_risk == "MODERATE":

            cardiovascular_risk += 20

        # ==========================
        # Nutrition Logic
        # ==========================

        if nutrition_score < 40:

            obesity_risk += 15

            diabetes_risk += 15

            cardiovascular_risk += 15

            drivers.append(

                "Poor nutrition profile"

            )

        elif nutrition_score > 80:

            obesity_risk -= 10

            diabetes_risk -= 10

            cardiovascular_risk -= 10

        # ==========================
        # Ingredient Logic
        # ==========================

        if ingredient_score < 40:

            inflammation_risk += 20

            daily_use_risk += 15

            drivers.append(

                "Weak ingredient quality"

            )

        elif ingredient_score > 80:

            inflammation_risk -= 10

        # ==========================
        # Additive Load
        # ==========================

        if additive_count >= 5:

            inflammation_risk += 25

            daily_use_risk += 15

            drivers.append(

                "High additive load"

            )

        elif additive_count >= 3:

            inflammation_risk += 10

        # ==========================
        # Trust Logic
        # ==========================

        if trust_score >= 90:

            obesity_risk -= 5

            diabetes_risk -= 5

            cardiovascular_risk -= 5

            inflammation_risk -= 5

        elif trust_score <= 50:

            obesity_risk += 10

            diabetes_risk += 10

            cardiovascular_risk += 10

            daily_use_risk += 10

        # ==========================
        # Clamp
        # ==========================

        obesity_risk = (

            RiskForecast._clamp(
                obesity_risk
            )

        )

        diabetes_risk = (

            RiskForecast._clamp(
                diabetes_risk
            )

        )

        cardiovascular_risk = (

            RiskForecast._clamp(
                cardiovascular_risk
            )

        )

        inflammation_risk = (

            RiskForecast._clamp(
                inflammation_risk
            )

        )

        daily_use_risk = (

            RiskForecast._clamp(
                daily_use_risk
            )

        )

        overall_risk = round(

            (

                obesity_risk
                +
                diabetes_risk
                +
                cardiovascular_risk
                +
                inflammation_risk
                +
                daily_use_risk

            )

            / 5,

            1

        )

        return {

            "overall_risk":

            overall_risk,

            "overall_label":

            RiskForecast._risk_label(

                overall_risk

            ),

            "risk_dimensions": {

                "obesity": {

                    "score":
                    obesity_risk,

                    "label":

                    RiskForecast
                    ._risk_label(

                        obesity_risk

                    )

                },

                "diabetes": {

                    "score":
                    diabetes_risk,

                    "label":

                    RiskForecast
                    ._risk_label(

                        diabetes_risk

                    )

                },

                "cardiovascular": {

                    "score":
                    cardiovascular_risk,

                    "label":

                    RiskForecast
                    ._risk_label(

                        cardiovascular_risk

                    )

                },

                "inflammation": {

                    "score":
                    inflammation_risk,

                    "label":

                    RiskForecast
                    ._risk_label(

                        inflammation_risk

                    )

                },

                "daily_use": {

                    "score":
                    daily_use_risk,

                    "label":

                    RiskForecast
                    ._risk_label(

                        daily_use_risk

                    )

                }

            },

            "primary_drivers":

            list(

                set(
                    drivers
                )

            )
        }