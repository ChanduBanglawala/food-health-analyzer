"""
allergen_analyzer.py
"""


class AllergenAnalyzer:

    COMMON_ALLERGENS = [
        "milk",
        "soy",
        "gluten",
        "wheat",
        "peanut",
        "tree nut",
        "egg",
        "fish",
        "shellfish"
    ]

    @classmethod
    def analyze(cls, product):

        allergens = str(
            product.get("allergens_en", "")
        ).lower()

        found = []

        for allergen in cls.COMMON_ALLERGENS:
            if allergen in allergens:
                found.append(allergen)

        return {
            "allergens_found": found,
            "allergen_count": len(found)
        }