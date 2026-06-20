"""
additive_analyzer.py
"""


class AdditiveAnalyzer:

    HIGH_RISK = {
        "en:e102",
        "en:e110",
        "en:e122",
        "en:e124",
        "en:e129",
        "en:e211",
        "en:e621"
    }

    @classmethod
    def analyze(cls, product):

        additives = product.get(
            "additives_tags",
            []
        )

        if additives is None:
            additives = []

        risky = []

        for additive in additives:
            if additive.lower() in cls.HIGH_RISK:
                risky.append(additive)

        return {
            "total_additives": len(additives),
            "risky_additives": risky
        }