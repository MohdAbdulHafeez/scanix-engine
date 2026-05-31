import random
from typing import Dict, List

from modules.ai.food_catalog import (
    FoodCatalog,
    FoodItem
)


class GoalProfileEngine:

    GOALS = {

        "weight_loss": {

            "protein_ratio": 0.35,
            "carb_ratio": 0.35,
            "fat_ratio": 0.30,

            "preferred_tags": [

                "weight_loss",
                "high_fiber"

            ]

        },

        "muscle_gain": {

            "protein_ratio": 0.35,
            "carb_ratio": 0.45,
            "fat_ratio": 0.20,

            "preferred_tags": [

                "muscle_gain",
                "protein"

            ]

        },

        "fat_loss": {

            "protein_ratio": 0.40,
            "carb_ratio": 0.30,
            "fat_ratio": 0.30,

            "preferred_tags": [

                "weight_loss",
                "lean_protein"

            ]

        },

        "recomposition": {

            "protein_ratio": 0.40,
            "carb_ratio": 0.35,
            "fat_ratio": 0.25,

            "preferred_tags": [

                "protein"

            ]

        }

    }

    @classmethod
    def get(

        cls,

        goal

    ):

        return cls.GOALS.get(

            goal,

            cls.GOALS[
                "muscle_gain"
            ]

        )
    
    
class MacroMatcher:

    @staticmethod
    def calculate_macros(

        calories,

        goal

    ):

        profile = (

            GoalProfileEngine.get(

                goal

            )

        )

        protein = (

            calories

            * profile[
                "protein_ratio"
            ]

        ) / 4

        carbs = (

            calories

            * profile[
                "carb_ratio"
            ]

        ) / 4

        fats = (

            calories

            * profile[
                "fat_ratio"
            ]

        ) / 9

        return {

            "calories":

            calories,

            "protein":

            round(protein),

            "carbs":

            round(carbs),

            "fats":

            round(fats)

        }
    

class WorkoutNutritionEngine:

    @staticmethod
    def build(

        goal

    ):

        if goal == "muscle_gain":

            return {

                "pre_workout":

                [

                    "Banana",

                    "Black Coffee"

                ],

                "post_workout":

                [

                    "Whey Protein",

                    "Chicken Breast"

                ]

            }

        return {

            "pre_workout":

            [

                "Apple"

            ],

            "post_workout":

            [

                "Greek Yogurt"

            ]

        }
    

class HydrationEngine:

    @staticmethod
    def calculate(

        weight

    ):

        return round(

            weight * 35 / 1000,

            1

        )


class MacroBalancer:

    @staticmethod
    def protein_foods(foods):

        return [

            f

            for f in foods

            if f.protein >= 15

        ]

    @staticmethod
    def carb_foods(foods):

        return [

            f

            for f in foods

            if f.carbs >= 20

        ]

    @staticmethod
    def fat_foods(foods):

        return [

            f

            for f in foods

            if f.fats >= 10

        ]

    @staticmethod
    def veg_foods(foods):

        return [

            f

            for f in foods

            if f.meal_type == "vegetable"

        ]


class MealBuilder:

    MEAL_RULES = {

        "breakfast": [
            "breakfast",
            "snack",
            "drink",
            "protein"
        ],

        "lunch": [
            "lunch",
            "protein",
            "carb",
            "vegetable"
        ],

        "snack": [
            "snack",
            "fruit",
            "drink"
        ],

        "dinner": [
            "dinner",
            "protein",
            "vegetable"
        ]

    }

    BREAKFAST_ONLY = {

        "Eggs",
        "Boiled Eggs",
        "Egg Whites",

        "Greek Yogurt",

        "Banana",
        "Apple",
        "Orange",
        "Guava",
        "Papaya",

        "Low Fat Milk",
        "Milk",

        "Protein Smoothie",

        "Idli",
        "Dosa",
        "Rava Dosa",

        "Pesarattu",
        "Besan Chilla",

        "Vegetable Upma",
        "Foxtail Millet Upma"

    }

    @staticmethod
    def _pick_best_foods(

        foods,

        target_calories,

        limit=3

    ):

        ranked = sorted(

            foods,

            key=lambda x: abs(

                x.calories -

                (target_calories / limit)

            )

        )

        return ranked[:limit]

    @classmethod
    def calorie_fill(

        cls,

        selected,

        candidates,

        target

    ):

        current = sum(

            x.calories

            for x in selected

        )

        remaining = [

            f

            for f in candidates

            if f not in selected

        ]

        remaining = sorted(

            remaining,

            key=lambda x: x.calories,

            reverse=True

        )

        for food in remaining:

            if current >= target * 0.95:

                break

            selected.append(food)

            current += food.calories

        return selected

    @classmethod
    def build_meal(

        cls,

        foods,

        target_calories,

        meal_type

    ):

        allowed = cls.MEAL_RULES.get(

            meal_type,

            []

        )

        if meal_type == "breakfast":

            candidates = [

                f

                for f in foods

                if f.name in cls.BREAKFAST_ONLY

            ]

            if not candidates:

                candidates = foods

        else:

            candidates = [

                f

                for f in foods

                if f.meal_type in allowed

            ]

            if not candidates:

                candidates = foods

        selected = []

        proteins = MacroBalancer.protein_foods(candidates)
        carbs = MacroBalancer.carb_foods(candidates)
        vegs = MacroBalancer.veg_foods(candidates)

        if meal_type == "breakfast":

            if proteins:
                selected.append(random.choice(proteins))
            if carbs:
                selected.append(random.choice(carbs))

        elif meal_type == "lunch":

            if proteins:
                selected.append(random.choice(proteins))
            if carbs:
                selected.append(random.choice(carbs))

        elif meal_type == "dinner":

            if proteins:
                selected.append(random.choice(proteins))
            if vegs:
                selected.append(random.choice(vegs))

        elif meal_type == "snack":

            snack_cands = [f for f in candidates if f.meal_type in ["snack", "fruit"]]
            if snack_cands:
                selected.append(random.choice(snack_cands))

        if not selected:

            selected = cls._pick_best_foods(

                candidates,

                target_calories

            )

        selected = cls.calorie_fill(

            selected,

            candidates,

            target_calories

        )

        selected = list(

            {

                x.name: x

                for x in selected

            }.values()

        )

        total_calories = sum(

            x.calories

            for x in selected

        )

        total_protein = round(

            sum(

                x.protein

                for x in selected

            ),

            1

        )

        return {

            "foods":

            [

                x.name

                for x in selected

            ],

            "calories":

            total_calories,

            "protein":

            total_protein

        }
    

class WeeklyPlanner:

    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    @classmethod
    def generate(

        cls,

        foods,

        calories,

        goal,

        diet_type

    ):

        used_foods = set()

        weekly = {}

        for day in cls.DAYS:

            day_foods = [

                f for f in foods

                if f.name not in used_foods

            ]

            b_foods = [

                f for f in day_foods

                if f.name in MealBuilder.BREAKFAST_ONLY

            ]

            if len(day_foods) < 5 or not b_foods:

                used_foods.clear()

                day_foods = foods

            random.shuffle(
                day_foods
            )

            daily = MealGenerator.generate_daily_plan(

                goal=goal,
                diet_type=diet_type,
                calories=calories,
                foods=day_foods

            )

            meals = []

            for meal in [

                "breakfast",
                "lunch",
                "snack",
                "dinner"
            ]:

                meals.extend(

                    daily[meal]["foods"]

                )

            used_foods.update(meals)

            weekly[day] = daily

        return weekly
    

class MealGenerator:

    @classmethod
    def generate_daily_plan(

        cls,

        goal,

        diet_type,

        calories,

        budget=None,

        foods=None

    ):

        if foods is None:
            try:
                foods = (

                    FoodCatalog.by_goal(

                        goal

                    )

                )
            except NameError:
                foods = []

            foods = (
                BudgetOptimizer.filter(
                    foods,
                    budget
                )
            )

            if goal == "diabetic":
                foods = (
                    HealthFilter.diabetic(
                        foods
                    )
                )

            if goal == "heart_friendly":
                foods = (
                    HealthFilter.heart(
                        foods
                    )
                )

            foods = [

                f

                for f in foods

                if (

                    f.diet_type ==

                    diet_type

                    or

                    diet_type is None

                )

            ]

        breakfast_target = (

            calories * 0.25

        )

        lunch_target = (

            calories * 0.30

        )

        snack_target = (

            calories * 0.15

        )

        dinner_target = (

            calories * 0.30

        )

        return {

            "breakfast":

            MealBuilder.build_meal(

                foods,

                breakfast_target,

                "breakfast"

            ),

            "lunch":

            MealBuilder.build_meal(

                foods,

                lunch_target,

                "lunch"

            ),

            "snack":

            MealBuilder.build_meal(

                foods,

                snack_target,

                "snack"

            ),

            "dinner":

            MealBuilder.build_meal(

                foods,

                dinner_target,

                "dinner"

            ),

            "workout":

            WorkoutNutritionEngine.build(

                goal

            )

        }

    @classmethod
    def generate_weekly_plan(

        cls,

        goal,

        diet_type,

        calories,

        budget=None

    ):
        
        try:
            foods = (

                FoodCatalog.by_goal(

                    goal

                )

            )
        except NameError:
            foods = []

        foods = (
            BudgetOptimizer.filter(
                foods,
                budget
            )
        )

        return (
            WeeklyPlanner.generate(
                foods=foods,
                calories=calories,
                goal=goal,
                diet_type=diet_type
            )
        )

    @classmethod
    def build(

        cls,

        goal,

        diet_type,

        calories,

        weight

    ):

        macros = (

            MacroMatcher.calculate_macros(

                calories,

                goal

            )

        )

        hydration = (

            HydrationEngine.calculate(

                weight

            )

        )

        daily = (

            cls.generate_daily_plan(

                goal,

                diet_type,

                calories

            )

        )

        weekly = (

            cls.generate_weekly_plan(

                goal,

                diet_type,

                calories

            )

        )

        return {

            "goal":

            goal,

            "diet_type":

            diet_type,

            "macros":

            macros,

            "water_target_liters":

            hydration,

            "daily_plan":

            daily,

            "weekly_plan":

            weekly

        }
    

class HealthFilter:

    @staticmethod
    def diabetic(

        foods

    ):

        return [

            f

            for f in foods

            if f.diabetic_safe

        ]

    @staticmethod
    def heart(

        foods

    ):

        return [

            f

            for f in foods

            if f.heart_friendly

        ]
    

class BudgetOptimizer:

    @staticmethod
    def filter(

        foods,

        budget

    ):

        if budget is None:

            return foods

        return [

            f

            for f in foods

            if f.budget == budget

        ]