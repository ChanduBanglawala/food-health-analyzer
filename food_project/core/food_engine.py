from ..analyzers.nutrition_analyzer import NutritionAnalyzer
from ..analyzers.ingredient_analyzer import IngredientAnalyzer
from ..analyzers.additive_analyzer import AdditiveAnalyzer
from ..analyzers.allergen_analyzer import AllergenAnalyzer
from ..analyzers.nova_analyzer import NovaAnalyzer
from ..analyzers.environmental_analyzer import EnvironmentalAnalyzer

from ..llm.explanation_generator import ExplanationGenerator

class FoodEngine:
    def __init__(self):
        self.explainer = ExplanationGenerator()

    def analyze(self, product):
        nutrition = NutritionAnalyzer.analyze(product)
        ingredients = IngredientAnalyzer.analyze(product)
        additives = AdditiveAnalyzer.analyze(product)
        allergens = AllergenAnalyzer.analyze(product)
        nova = NovaAnalyzer.analyze(product)
        environment = EnvironmentalAnalyzer.analyze(product)

        report = {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "nutrition": nutrition,
            "ingredients": ingredients,
            "additives": additives,
            "allergens": allergens,
            "nova": nova,
            "environment": environment,
        }

        try:
            ai_result = self.explainer.generate(report)

            report["health_score"] = {
                "score": ai_result.get("health_score", 0),
                "grade": ai_result.get("grade", "Unknown"),
            }

            report["ai_explanation"] = {
                "summary": ai_result.get("summary", ""),
                "pros": ai_result.get("pros", []),
                "cons": ai_result.get("cons", []),
                "recommendation": ai_result.get("recommendation", ""),
                "confidence": ai_result.get("confidence", "Unknown"),
            }

        except Exception as e:
            report["health_score"] = {
                "score": 0,
                "grade": "Unknown",
            }

            report["ai_explanation"] = {
                "summary": f"AI analysis unavailable: {str(e)}",
                "pros": [],
                "cons": [],
                "recommendation": "",
                "confidence": "Low",
            }

        return report
