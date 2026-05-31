class AdditiveMapper:

    @staticmethod
    def resolve(

        additive

    ):

        return (

            ADDITIVE_MAP.get(

                additive,

                additive

            )

        )
    
ADDITIVE_MAP = {

    "INS 100":
    "Curcumin",

    "INS 102":
    "Tartrazine",

    "INS 110":
    "Sunset Yellow",

    "INS 211":
    "Sodium Benzoate",

    "INS 250":
    "Sodium Nitrite",

    "INS 322":
    "Lecithin",

    "INS 330":
    "Citric Acid",

    "INS 500":
    "Sodium Bicarbonate",

    "INS 500(ii)":
    "Sodium Bicarbonate",

    "INS 621":
    "Monosodium Glutamate",

    "MSG":
    "Monosodium Glutamate"
}
