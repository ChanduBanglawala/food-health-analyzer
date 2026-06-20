"""
nutrition_analyzer.py
"""

import pandas as pd

class NutritionAnalyzer:
    @staticmethod
    def clean(value):

        if pd.isna(value):
            return 0

        try:
            return float(value)
        except Exception:
            return 0

    @staticmethod
    def analyze(product):

        calories = NutritionAnalyzer.clean(
            product.get("energy-kcal_100g")
        )

        sugar = NutritionAnalyzer.clean(
            product.get("sugars_100g")
        )

        fat = NutritionAnalyzer.clean(
            product.get("fat_100g")
        )

        salt = NutritionAnalyzer.clean(
            product.get("salt_100g")
        )

        protein = NutritionAnalyzer.clean(
            product.get("proteins_100g")
        )

        fiber = NutritionAnalyzer.clean(
            product.get("fiber_100g")
        )

        report = {
            "calories": calories,
            "sugar": sugar,
            "fat": fat,
            "salt": salt,
            "protein": protein,
            "fiber": fiber,
        }

        report["sugar_status"] = (
            "High" if sugar > 15
            else "Moderate" if sugar > 5
            else "Low"
        )

        report["salt_status"] = (
            "High" if salt > 1.5
            else "Moderate" if salt > 0.5
            else "Low"
        )

        report["fat_status"] = (
            "High" if fat > 20
            else "Moderate" if fat > 10
            else "Low"
        )

        return report
