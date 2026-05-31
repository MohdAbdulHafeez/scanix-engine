class IngredientRanker:

    @staticmethod
    def rank(

        ingredients

    ):

        ranked = []

        for index, ingredient in enumerate(

            ingredients,

            start=1

        ):

            ranked.append({

                "name":
                ingredient,

                "position":
                index

            })

        return ranked