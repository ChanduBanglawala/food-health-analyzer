"""
health_score.py
"""


class HealthScore:

    @staticmethod
    def calculate(product):

        score = 100

        sugar = product.get("sugars_100g", 0) or 0
        salt = product.get("salt_100g", 0) or 0
        fat = product.get("fat_100g", 0) or 0

        nova = product.get("nova_group")

        if sugar > 20:
            score -= 20

        if salt > 1.5:
            score -= 15

        if fat > 20:
            score -= 15

        if nova == 4:
            score -= 25

        score = max(0, min(score, 100))

        if score >= 80:
            grade = "A"
        elif score >= 60:
            grade = "B"
        elif score >= 40:
            grade = "C"
        elif score >= 20:
            grade = "D"
        else:
            grade = "E"

        return {
            "score": score,
            "grade": grade
        }