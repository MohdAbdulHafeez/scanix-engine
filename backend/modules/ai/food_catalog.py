from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class FoodItem:

    name: str

    calories: int

    protein: float

    carbs: float

    fats: float

    fiber: float

    sugar: float

    sodium: float

    glycemic_index: int

    meal_type: str

    diet_type: str

    region: str

    budget: str

    diabetic_safe: bool

    heart_friendly: bool

    muscle_gain: bool

    weight_loss: bool

    tags: List[str]


class FoodCatalog:

    FOODS = [

        # =====================================
        # SOUTH INDIAN
        # =====================================

        FoodItem(
            "Idli",70,2,15,0,1,0,120,55,
            "breakfast","vegetarian","south_indian",
            "student",True,True,False,True,
            ["traditional"]
        ),

        FoodItem(
            "Dosa",130,3,22,3,1,1,180,65,
            "breakfast","vegetarian","south_indian",
            "student",False,True,False,False,
            ["traditional"]
        ),

        FoodItem(
            "Ragi Dosa",120,4,20,2,4,1,150,45,
            "breakfast","vegetarian","south_indian",
            "student",True,True,False,True,
            ["high_fiber"]
        ),

        FoodItem(
            "Upma",220,6,35,5,3,2,220,60,
            "breakfast","vegetarian","south_indian",
            "student",True,True,False,False,
            ["breakfast"]
        ),

        FoodItem(
            "Sambar",120,6,18,2,4,1,180,40,
            "side","vegetarian","south_indian",
            "student",True,True,False,True,
            ["high_fiber"]
        ),

        # =====================================
        # NORTH INDIAN
        # =====================================

        FoodItem(
            "Rajma",220,15,35,1,11,2,90,35,
            "lunch","vegetarian","north_indian",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Chole",260,14,40,4,10,3,120,40,
            "lunch","vegetarian","north_indian",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Paneer Curry",320,20,8,22,2,3,420,25,
            "dinner","vegetarian","north_indian",
            "medium",False,True,True,False,
            ["muscle_gain"]
        ),

        FoodItem(
            "Dal Tadka",180,10,25,5,6,2,250,35,
            "lunch","vegetarian","north_indian",
            "student",True,True,False,True,
            ["protein"]
        ),

        # =====================================
        # NON VEG
        # =====================================

        FoodItem(
            "Chicken Breast",165,31,0,4,0,0,70,0,
            "protein","non_vegetarian","global",
            "medium",True,True,True,True,
            ["lean_protein"]
        ),

        FoodItem(
            "Eggs",140,12,1,10,0,0,140,0,
            "breakfast","non_vegetarian","global",
            "student",True,True,True,False,
            ["protein"]
        ),

        FoodItem(
            "Fish Curry",260,28,6,12,0,1,280,15,
            "dinner","non_vegetarian","coastal",
            "medium",True,True,True,False,
            ["omega3"]
        ),

        FoodItem(
            "Chicken Curry",290,26,8,15,1,2,350,20,
            "dinner","non_vegetarian","north_indian",
            "medium",True,False,True,False,
            ["muscle_gain"]
        ),

        # =====================================
        # GYM FOODS
        # =====================================

        FoodItem(
            "Oats",150,5,27,3,4,1,5,40,
            "breakfast","vegetarian","global",
            "student",True,True,False,True,
            ["fitness"]
        ),

        FoodItem(
            "Greek Yogurt",120,15,5,3,0,3,60,20,
            "snack","vegetarian","global",
            "premium",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Banana",105,1,27,0,3,14,1,52,
            "snack","vegetarian","global",
            "student",True,True,True,False,
            ["preworkout"]
        ),

        FoodItem(
            "Whey Protein",130,25,3,2,0,1,90,5,
            "supplement","vegetarian","global",
            "premium",True,True,True,False,
            ["protein"]
        ),

        FoodItem(
            "Peanut Butter",190,8,7,16,2,3,90,15,
            "snack","vegetarian","global",
            "medium",True,True,True,False,
            ["healthy_fat"]
        ),

        # =====================================
        # HEART FRIENDLY
        # =====================================

        FoodItem(
            "Apple",95,0,25,0,4,19,1,36,
            "snack","vegan","global",
            "student",True,True,False,True,
            ["fruit"]
        ),

        FoodItem(
            "Almonds",170,6,6,15,4,1,1,10,
            "snack","vegan","global",
            "medium",True,True,True,False,
            ["healthy_fat"]
        ),

        FoodItem(
            "Tofu",140,16,4,8,2,1,10,10,
            "protein","vegan","global",
            "medium",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Brown Rice",216,5,45,2,4,0,5,50,
            "carb","vegan","global",
            "student",True,True,False,True,
            ["complex_carb"]
        ),

        # =====================================
        # SOUTH INDIAN EXTENDED
        # =====================================

        FoodItem(
            "Rava Dosa",170,4,28,4,2,1,180,55,
            "breakfast","vegetarian","south_indian",
            "student",True,True,False,False,
            ["traditional"]
        ),

        FoodItem(
            "Pesarattu",180,9,24,4,5,1,150,40,
            "breakfast","vegetarian","south_indian",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Pongal",250,8,35,8,2,1,220,58,
            "breakfast","vegetarian","south_indian",
            "student",False,True,False,False,
            ["traditional"]
        ),

        FoodItem(
            "Curd Rice",220,6,32,7,1,2,250,60,
            "lunch","vegetarian","south_indian",
            "student",False,True,False,False,
            ["comfort_food"]
        ),

        FoodItem(
            "Lemon Rice",240,5,38,7,2,1,200,62,
            "lunch","vegetarian","south_indian",
            "student",False,True,False,False,
            ["traditional"]
        ),

        FoodItem(
            "Vegetable Upma",210,7,32,6,4,2,180,52,
            "breakfast","vegetarian","south_indian",
            "student",True,True,False,True,
            ["high_fiber"]
        ),

        # =====================================
        # NORTH INDIAN EXTENDED
        # =====================================

        FoodItem(
            "Palak Paneer",280,18,10,18,4,2,320,25,
            "dinner","vegetarian","north_indian",
            "medium",True,True,True,True,
            ["iron"]
        ),

        FoodItem(
            "Dal Makhani",290,14,28,14,8,2,350,38,
            "lunch","vegetarian","north_indian",
            "medium",False,False,True,False,
            ["protein"]
        ),

        FoodItem(
            "Aloo Gobi",180,5,22,7,5,3,180,40,
            "lunch","vegetarian","north_indian",
            "student",True,True,False,True,
            ["vegetable"]
        ),

        FoodItem(
            "Mixed Dal",210,15,28,4,8,1,220,35,
            "lunch","vegetarian","north_indian",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Roti",110,4,22,1,3,0,120,45,
            "carb","vegetarian","north_indian",
            "student",True,True,False,True,
            ["whole_wheat"]
        ),

        # =====================================
        # NON VEG EXPANDED
        # =====================================

        FoodItem(
            "Egg Whites",70,15,1,0,0,0,80,0,
            "protein","non_vegetarian","global",
            "student",True,True,True,True,
            ["lean_protein"]
        ),

        FoodItem(
            "Tandoori Chicken",220,32,2,8,0,0,250,5,
            "dinner","non_vegetarian","north_indian",
            "medium",True,True,True,True,
            ["lean_protein"]
        ),

        FoodItem(
            "Grilled Fish",210,30,0,8,0,0,120,0,
            "protein","non_vegetarian","coastal",
            "medium",True,True,True,True,
            ["omega3"]
        ),

        FoodItem(
            "Boiled Eggs",140,12,1,10,0,0,140,0,
            "snack","non_vegetarian","global",
            "student",True,True,True,False,
            ["protein"]
        ),

        # =====================================
        # FRUITS
        # =====================================

        FoodItem(
            "Apple",95,0,25,0,4,19,1,36,
            "snack","vegan","global",
            "student",True,True,False,True,
            ["fruit"]
        ),

        FoodItem(
            "Orange",62,1,15,0,3,12,0,40,
            "snack","vegan","global",
            "student",True,True,False,True,
            ["fruit"]
        ),

        FoodItem(
            "Guava",68,3,14,1,5,8,2,24,
            "snack","vegan","global",
            "student",True,True,False,True,
            ["high_fiber"]
        ),

        FoodItem(
            "Papaya",55,1,14,0,3,8,2,35,
            "snack","vegan","global",
            "student",True,True,False,True,
            ["fruit"]
        ),

        # =====================================
        # VEGETABLES
        # =====================================

        FoodItem(
            "Broccoli",55,4,11,1,5,2,30,15,
            "vegetable","vegan","global",
            "medium",True,True,True,True,
            ["superfood"]
        ),

        FoodItem(
            "Spinach",35,4,4,0,3,0,40,10,
            "vegetable","vegan","global",
            "student",True,True,True,True,
            ["iron"]
        ),

        FoodItem(
            "Carrot",50,1,12,0,4,5,40,35,
            "vegetable","vegan","global",
            "student",True,True,False,True,
            ["vitamin_a"]
        ),

        FoodItem(
            "Cucumber",16,1,4,0,1,2,2,15,
            "vegetable","vegan","global",
            "student",True,True,False,True,
            ["hydration"]
        ),

        # =====================================
        # GYM FOODS
        # =====================================

        FoodItem(
            "Low Fat Milk",110,8,12,3,0,12,90,30,
            "drink","vegetarian","global",
            "student",True,True,True,False,
            ["protein"]
        ),

        FoodItem(
            "Cottage Cheese",210,24,6,10,0,2,300,20,
            "protein","vegetarian","global",
            "medium",True,True,True,False,
            ["protein"]
        ),

        FoodItem(
            "Soy Chunks",170,26,12,1,5,1,30,20,
            "protein","vegetarian","global",
            "student",True,True,True,True,
            ["high_protein"]
        ),

        FoodItem(
            "Black Chana",210,13,32,3,10,2,40,30,
            "protein","vegan","india",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Moong Dal",180,14,26,2,7,1,30,28,
            "protein","vegan","india",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Masoor Dal",190,15,28,2,8,1,35,30,
            "protein","vegan","india",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Kidney Beans",220,15,35,1,11,2,20,32,
            "protein","vegan","india",
            "student",True,True,True,True,
            ["protein"]
        ),

        FoodItem(
            "Walnuts",185,4,4,18,2,1,2,15,
            "snack","vegan","global",
            "premium",True,True,True,False,
            ["healthy_fat"]
        ),

        FoodItem(
            "Cashews",170,5,9,14,1,2,5,22,
            "snack","vegan","india",
            "medium",True,True,True,False,
            ["healthy_fat"]
        ),

        FoodItem(
            "Flax Seeds",150,5,8,12,8,1,5,5,
            "snack","vegan","global",
            "medium",True,True,True,True,
            ["omega3"]
        ),

        FoodItem(
            "Vegetable Salad",80,3,12,1,5,3,20,15,
            "lunch","vegan","global",
            "student",True,True,False,True,
            ["weight_loss"]
        ),

        FoodItem(
            "Sprouts Salad",120,9,18,2,6,2,40,20,
            "snack","vegan","india",
            "student",True,True,True,True,
            ["weight_loss"]
        ),

        FoodItem(
            "Clear Vegetable Soup",70,3,10,1,3,2,150,15,
            "dinner","vegan","global",
            "student",True,True,False,True,
            ["weight_loss"]
        ),

        FoodItem(
            "Chicken Rice Bowl",450,35,45,10,3,2,250,35,
            "lunch","non_vegetarian","global",
            "medium",True,True,True,False,
            ["muscle_gain"]
        ),

        FoodItem(
            "Paneer Rice Bowl",430,24,48,14,4,2,300,38,
            "lunch","vegetarian","india",
            "medium",True,True,True,False,
            ["muscle_gain"]
        ),

        FoodItem(
            "Protein Smoothie",350,30,25,10,4,8,120,25,
            "snack","vegetarian","global",
            "premium",True,True,True,False,
            ["muscle_gain"]
        ),

        FoodItem(
            "Millet Khichdi",220,8,34,5,7,2,150,38,
            "lunch","vegetarian","india",
            "student",True,True,False,True,
            ["diabetic"]
        ),

        FoodItem(
            "Foxtail Millet Upma",210,7,32,4,6,2,140,35,
            "breakfast","vegetarian","south_indian",
            "student",True,True,False,True,
            ["diabetic"]
        ),

        FoodItem(
            "Besan Chilla",180,10,20,5,4,1,120,32,
            "breakfast","vegetarian","north_indian",
            "student",True,True,True,True,
            ["diabetic"]
        ),

        FoodItem(
            "Salmon",280,32,0,16,0,0,90,0,
            "protein","non_vegetarian","global",
            "premium",True,True,True,False,
            ["omega3"]
        ),

        FoodItem(
            "Avocado",240,3,12,22,10,1,10,10,
            "healthy_fat","vegan","global",
            "premium",True,True,False,True,
            ["heart"]
        ),

        FoodItem(
            "Quinoa Bowl",320,12,50,8,7,2,40,40,
            "lunch","vegan","global",
            "premium",True,True,True,True,
            ["superfood"]
        )

    ]

    @classmethod
    def get_all(cls):

        return cls.FOODS

    @classmethod
    def by_goal(cls, goal: str):

        if goal == "muscle_gain":

            return [f for f in cls.FOODS if f.muscle_gain]

        if goal in {
            "weight_loss",
            "fat_loss"
        }:

            return [f for f in cls.FOODS if f.weight_loss]

        return cls.FOODS

    @classmethod
    def by_diet(cls, diet_type: str):

        return [

            f for f in cls.FOODS

            if f.diet_type == diet_type

        ]

    @classmethod
    def diabetic_safe(cls):

        return [

            f for f in cls.FOODS

            if f.diabetic_safe

        ]

    @classmethod
    def heart_friendly(cls):

        return [

            f for f in cls.FOODS

            if f.heart_friendly

        ]