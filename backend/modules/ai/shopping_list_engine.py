from collections import defaultdict

from modules.ai.food_catalog import (
    FoodCatalog
)


class ShoppingListEngine:

    CATEGORY_MAP = {

        "protein": "Proteins",
        "carb": "Carbohydrates",
        "vegetable": "Vegetables",
        "fruit": "Fruits",
        "snack": "Snacks",
        "healthy_fat": "Healthy Fats",
        "drink": "Beverages",
        "breakfast": "Breakfast Items",
        "lunch": "Meal Items",
        "dinner": "Meal Items"

    }

    BUDGET_MULTIPLIER = {

        "student": 1.0,
        "medium": 1.4,
        "premium": 2.2

    }

    # =====================================
    # Budget Substitutions
    # =====================================

    BUDGET_SUBSTITUTIONS = {

        "student": {

            "Salmon": "Eggs",
            "Grilled Fish": "Boiled Eggs",
            "Chicken Breast": "Soy Chunks",
            "Greek Yogurt": "Curd",
            "Quinoa Bowl": "Brown Rice",
            "Protein Smoothie": "Low Fat Milk",
            "Almonds": "Peanuts",
            "Walnuts": "Peanuts",
            "Fish Curry": "Chicken Curry"

        },

        "medium": {

            "Salmon": "Chicken Breast",
            "Greek Yogurt": "Curd",
            "Quinoa Bowl": "Brown Rice",
            "Grilled Fish": "Chicken Curry"

        },

        "premium": {}

    }

    # =====================================
    # Real Grocery Quantities & Prices
    # =====================================

    QUANTITY_MAP = {

        "Chicken Breast": 3,
        "Chicken Curry": 2,
        "Tandoori Chicken": 2,
        "Chicken Rice Bowl": 7,

        "Fish Curry": 2,
        "Grilled Fish": 2,
        "Salmon": 2.5,

        "Eggs": 42,
        "Boiled Eggs": 42,
        "Egg Whites": 30,

        "Milk": 7,
        "Low Fat Milk": 7,

        "Greek Yogurt": 2,
        "Cottage Cheese": 2,
        "Curd": 2,

        "Oats": 1.5,
        "Brown Rice": 3,
        "Quinoa Bowl": 7,

        "Banana": 21,
        "Apple": 14,
        "Orange": 14,

        "Almonds": 0.5,
        "Walnuts": 0.5,
        "Peanut Butter": 1,
        "Peanuts": 1,

        "Broccoli": 2,
        "Spinach": 2,
        "Carrot": 2,

        "Rajma": 1.5,
        "Chole": 1.5,
        "Moong Dal": 1.5,
        "Masoor Dal": 1.5,

        "Tofu": 2,
        "Paneer Curry": 2,
        "Palak Paneer": 2,
        "Soy Chunks": 1.5,

        "Protein Smoothie": 7,
        "Whey Protein": 1

    }

    PRICE_MAP = {

        "Chicken Breast": 600,
        "Chicken Curry": 400,
        "Tandoori Chicken": 500,
        "Chicken Rice Bowl": 600,

        "Fish Curry": 400,
        "Grilled Fish": 600,
        "Salmon": 1200,

        "Eggs": 200,
        "Boiled Eggs": 200,
        "Egg Whites": 180,

        "Low Fat Milk": 350,
        "Greek Yogurt": 300,
        "Curd": 120,

        "Oats": 200,
        "Brown Rice": 200,
        "Quinoa Bowl": 1000,

        "Banana": 120,
        "Apple": 200,
        "Orange": 200,

        "Almonds": 400,
        "Walnuts": 450,
        "Peanut Butter": 300,
        "Peanuts": 120,

        "Broccoli": 200,
        "Spinach": 150,
        "Carrot": 120,

        "Rajma": 180,
        "Chole": 180,
        "Moong Dal": 150,
        "Masoor Dal": 150,

        "Tofu": 300,
        "Paneer Curry": 500,
        "Palak Paneer": 450,
        "Soy Chunks": 120,

        "Protein Smoothie": 400,
        "Whey Protein": 1800

    }

    DEFAULT_QUANTITY = {

        "protein": 2,
        "fruit": 14,
        "vegetable": 2,
        "snack": 7,
        "drink": 7,
        "breakfast": 14,
        "lunch": 7,
        "dinner": 7

    }

    DEFAULT_PRICE = {

        "protein": 500,
        "fruit": 150,
        "vegetable": 150,
        "snack": 200,
        "drink": 250,
        "breakfast": 200,
        "lunch": 350,
        "dinner": 350

    }

    @classmethod
    def apply_budget_substitutions(

        cls,

        foods,

        budget

    ):

        subs = cls.BUDGET_SUBSTITUTIONS.get(

            budget,

            {}

        )

        if not subs:

            return foods

        all_foods = {

            f.name: f

            for f in FoodCatalog.get_all()

        }

        final_foods = []

        for f in foods:

            if f.name in subs:

                sub_name = subs[f.name]

                if sub_name in all_foods:

                    final_foods.append(

                        all_foods[sub_name]

                    )

                else:

                    final_foods.append(f)

            else:

                final_foods.append(f)

        unique_foods = {

            x.name: x

            for x in final_foods

        }

        return list(

            unique_foods.values()

        )

    @classmethod
    def categorize(

        cls,

        foods

    ):

        categorized = defaultdict(list)

        for food in foods:

            category = cls.CATEGORY_MAP.get(

                food.meal_type,

                "Other"

            )

            categorized[category].append(

                food.name

            )

        return dict(categorized)

    @classmethod
    def estimate_quantity(

        cls,

        food,

        calories=2200

    ):

        multiplier = (

            cls.calorie_multiplier(

                calories

            )

        )

        base_val = cls.QUANTITY_MAP.get(

            food.name

        )

        if not base_val:

            base_val = cls.DEFAULT_QUANTITY.get(

                food.meal_type,

                3

            )

        try:
            base_val = float(base_val)
        except (ValueError, TypeError):
            try:
                base_val = float(str(base_val).split(" ")[0])
            except Exception:
                base_val = 3.0

        unit = "kg"

        name_lower = food.name.lower()

        if "egg" in name_lower:
            unit = "eggs"

        elif "milk" in name_lower:
            unit = "litres"

        elif "smoothie" in name_lower or "snack" in food.meal_type.lower():
            unit = "servings"

        elif "bowl" in name_lower or "lunch" in food.meal_type.lower() or "dinner" in food.meal_type.lower():
            unit = "meals"

        elif "fruit" in food.meal_type.lower() or "banana" in name_lower or "apple" in name_lower or "orange" in name_lower:
            unit = "pieces"

        scaled = round(base_val * multiplier, 1)

        if scaled.is_integer():
            scaled = int(scaled)

        final_quantity = f"{scaled} {unit}"

        return {

            "item":

            food.name,

            "weekly_quantity":

            final_quantity

        }

    @classmethod
    def build_quantities(

        cls,

        foods,

        calories

    ):

        return [

            cls.estimate_quantity(

                food,

                calories

            )

            for food in foods

        ]

    @classmethod
    def estimate_cost(

        cls,

        foods,

        budget

    ):

        total = 0

        for food in foods:

            total += cls.PRICE_MAP.get(

                food.name,

                cls.DEFAULT_PRICE.get(

                    food.meal_type,

                    200

                )

            )

        budget_factor = {

            "student": 0.75,
            "medium": 0.90,
            "premium": 1.25

        }

        total *= budget_factor.get(

            budget,

            1.0

        )

        return round(total)

    @staticmethod
    def pantry_staples():

        return [

            "Salt",
            "Turmeric",
            "Black Pepper",
            "Cooking Oil",
            "Garlic",
            "Ginger"

        ]

    @classmethod
    def weekly_list(

        cls,

        goal=None,

        diet_type=None,

        budget="medium",

        calories=2200

    ):

        try:
            foods = FoodCatalog.get_all()
        except NameError:
            foods = []

        foods = cls.goal_filter(

            foods,

            goal

        )

        if diet_type:

            foods = [

                f

                for f in foods

                if f.diet_type == diet_type

            ]

        foods = cls.apply_budget_substitutions(

            foods,

            budget

        )

        categorized = (

            cls.categorize(

                foods

            )

        )

        quantities = (

            cls.build_quantities(

                foods,

                calories

            )

        )

        cost = (

            cls.estimate_cost(

                foods,

                budget

            )

        )

        return {

            "budget":

            budget,

            "estimated_weekly_cost":

            cost,

            "estimated_monthly_cost":

            cost * 4,

            "categories":

            categorized,

            "pantry_items":

            cls.pantry_staples(),

            "quantities":

            quantities

        }

    @classmethod
    def monthly_list(

        cls,

        goal=None,

        diet_type=None,

        budget="medium"

    ):

        weekly = cls.weekly_list(

            goal,

            diet_type,

            budget

        )

        weekly[

            "estimated_monthly_cost"

        ] = (

            weekly[
                "estimated_weekly_cost"
            ]

            * 4

        )

        return weekly
    

    @classmethod
    def goal_filter(

        cls,

        foods,

        goal

    ):

        if not goal:

            return foods

        if goal == "muscle_gain":

            return [

                f for f in foods

                if f.muscle_gain

            ]

        if goal in [

            "weight_loss",

            "fat_loss"

        ]:

            return [

                f for f in foods

                if f.weight_loss

            ]

        if goal == "diabetic":

            return [

                f for f in foods

                if f.diabetic_safe

            ]

        if goal == "heart_friendly":

            return [

                f for f in foods

                if f.heart_friendly

            ]

        return foods
    

    @staticmethod
    def calorie_multiplier(

        calories

    ):

        if calories <= 1800:

            return 1.0

        if calories <= 2400:

            return 1.1

        if calories <= 3000:

            return 1.2

        return 1.3