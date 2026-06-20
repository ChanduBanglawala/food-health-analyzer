"""
ingredient_analyzer.py
"""

import re


class IngredientAnalyzer:

    RISKY_INGREDIENTS = {
        "palm oil": "Contains Palm Oil",
        "hydrogenated": "Contains Hydrogenated Fat",
        "high fructose corn syrup": "Contains High Fructose Corn Syrup",
        "msg": "Contains MSG",
        "monosodium glutamate": "Contains MSG",
        "aspartame": "Contains Artificial Sweetener",
        "sucralose": "Contains Artificial Sweetener",
        "acesulfame": "Contains Artificial Sweetener",
    }

    @classmethod
    def analyze(cls, product):

        ingredients = (
            str(product.get("ingredients_text", ""))
            .lower()
        )

        warnings = []

        for ingredient, message in cls.RISKY_INGREDIENTS.items():
            if ingredient in ingredients:
                warnings.append(message)

        return {
            "ingredient_warnings": warnings,
            "ingredient_count": len(
                re.split(r"[,;]", ingredients)
            ) if ingredients else 0
        }