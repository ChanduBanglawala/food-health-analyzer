"""
nova_analyzer.py
"""


class NovaAnalyzer:

    NOVA_DESCRIPTIONS = {
        1: "Unprocessed or minimally processed",
        2: "Processed culinary ingredients",
        3: "Processed foods",
        4: "Ultra-processed foods"
    }

    @classmethod
    def analyze(cls, product):

        nova = product.get("nova_group")

        return {
            "nova_group": nova,
            "description":
            cls.NOVA_DESCRIPTIONS.get(
                nova,
                "Unknown"
            )
        }