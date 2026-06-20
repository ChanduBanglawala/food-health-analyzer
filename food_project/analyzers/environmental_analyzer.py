"""
environmental_analyzer.py
"""


class EnvironmentalAnalyzer:

    @classmethod
    def analyze(cls, product):

        grade = product.get(
            "environmental_score_grade"
        )

        score = product.get(
            "environmental_score_score"
        )

        return {
            "environmental_grade": grade,
            "environmental_score": score
        }
