FSSAI_RULES = {

    "NO_PRESERVATIVES": {

        "type": "ingredient_absence",

        "ontology_key":
        "preservatives",

        "claim":
        "no preservatives"

    },

    "NO_ARTIFICIAL_COLORS": {

        "type": "ingredient_absence",

        "ontology_key":
        "artificial_colors",

        "claim":
        "no artificial colors"

    },

    "VEGAN": {

        "type": "ingredient_absence",

        "ontology_key":
        "non_vegan",

        "claim":
        "vegan"

    },

    "GLUTEN_FREE": {

        "type": "ingredient_absence",

        "ontology_key":
        "gluten_sources",

        "claim":
        "gluten free"

    },

    "LOW_SUGAR": {

        "type": "threshold",

        "claim":
        "low sugar",

        "threshold_key":
        "low sugar"

    },

    "LOW_FAT": {

        "type": "threshold",

        "claim":
        "low fat",

        "threshold_key":
        "low fat"

    },

    "HIGH_PROTEIN": {

        "type": "threshold",

        "claim":
        "high protein",

        "threshold_key":
        "high protein"

    }

}