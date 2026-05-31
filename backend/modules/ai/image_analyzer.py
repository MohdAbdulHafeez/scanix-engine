import os

import re

from google import genai

from PIL import Image


class ImageAnalyzer:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY missing"
            )

        self.client = (

            genai.Client(
                api_key=api_key
            )

        )

        self.model = os.getenv(

            "AI_PRIMARY_MODEL",

            "gemini-2.5-flash"

        )

    # =====================================
    # Vision Analysis
    # =====================================

    def analyze(

        self,

        image_path

    ):

        image = Image.open(
            image_path
        )

        # =====================================
        # UPGRADE 1: Exact JSON Prompt
        # UPGRADE 5: Ingredient Order (position inside array)
        # UPGRADE 6: Nutrition Label Extraction (exact fields)
        # =====================================
        prompt = """

Analyze this food product image.

Return VALID JSON ONLY.

Use EXACT keys:

{
  "product_name": "",
  "brand": "",
  "ingredients": [
    {
      "name": "",
      "position": 1
    }
  ],
  "nutrition": {
    "calories": 0,
    "protein": 0,
    "fat": 0,
    "saturated_fat": 0,
    "carbohydrates": 0,
    "sugars": 0,
    "added_sugars": 0,
    "fiber": 0,
    "sodium": 0
  },
  "claims": [],
  "additives": [],
  "allergens": [],
  "food_category": "",
  "confidence": 0
}

Rules:

- Extract nutrition label values exactly as shown.
- Extract ingredients in order with their position.
- Extract additives separately.
- Extract allergens separately.
- Extract all marketing claims.
- If a value is missing use null.
- Return ONLY valid JSON.
- No markdown.
- No explanations.

"""

        MODELS = [

            self.model,

            "gemini-2.5-flash",

            "gemini-2.0-flash",

            "gemini-1.5-flash"

        ]

        text = ""

        for current_model in MODELS:

            try:

                response = (

                    self.client.models.generate_content(

                        model=current_model,

                        contents=[

                            prompt,

                            image

                        ]

                    )

                )

                text = response.text

                break

            except Exception as e:

                error_msg = str(e).lower()

                if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:

                    continue

                break

        parsed = (

            self._extract_json(
                text
            )

        )

        # =====================================
        # UPGRADE 3: Add OCR text output & vision success
        # =====================================
        return {

            "raw_response":
            text,

            "structured":
            parsed,

            "vision_success":
            bool(
                parsed
            )

        }

    # =====================================
    # JSON Extraction
    # =====================================

    def _extract_json(

        self,

        text

    ):

        # =====================================
        # UPGRADE 2: Replace _extract_json (Robust fallback)
        # =====================================
        import json

        text = text.strip()

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        try:

            return json.loads(
                text
            )

        except Exception:

            pass

        try:

            match = re.search(

                r"\{.*\}",

                text,

                re.DOTALL

            )

            if match:

                return json.loads(

                    match.group()

                )

        except Exception:

            pass

        return {}

    # =====================================
    # Product Scan
    # =====================================

    def scan_product(

        self,

        image_path

    ):

        result = self.analyze(
            image_path
        )

        data = result.get(

            "structured",

            {}

        )

        # =====================================
        # UPGRADE 4: Add fallback extraction
        # =====================================
        if not data:

            return {

                "product_name": None,

                "brand": None,

                "ingredients": [],

                "nutrition": {},

                "claims": [],

                "additives": [],

                "allergens": [],

                "food_category": None,

                "confidence": 0,

                "vision_success": False

            }

        return {

            "product_name":

            data.get(
                "product_name"
            ),

            "brand":

            data.get(
                "brand"
            ),

            "ingredients":

            data.get(
                "ingredients",
                []
            ),

            "nutrition":

            data.get(
                "nutrition",
                {}
            ),

            "claims":

            data.get(
                "claims",
                []
            ),

            "additives":

            data.get(
                "additives",
                []
            ),

            "allergens":

            data.get(
                "allergens",
                []
            ),

            "food_category":

            data.get(
                "food_category"
            ),

            "confidence":

            data.get(
                "confidence",
                0
            ),

            # =====================================
            # UPGRADE 3 (Part 2): Vision success boolean
            # =====================================
            "vision_success":
            
            data != {}

        }