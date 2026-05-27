class BMIEngine:

    @staticmethod
    def analyze(

        bmi

    ):

        if bmi < 18.5:

            category = "UNDERWEIGHT"

        elif bmi < 25:

            category = "NORMAL"

        elif bmi < 30:

            category = "OVERWEIGHT"

        else:

            category = "OBESE"

        return {

            "bmi":
            bmi,

            "category":
            category

        }