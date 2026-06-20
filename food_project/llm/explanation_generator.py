import json

from .llm_client import LLMClient


class ExplanationGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate(self, product):

        prompt = f"""
You are an expert nutritionist, food scientist, and public health advisor.

Your task is to evaluate the healthiness of a food product using all available information.

========================
PRODUCT INFORMATION
===================

Product Name:
{product.get("product_name")}

Brand:
{product.get("brands")}

Ingredients:
{product.get("ingredients_text")}

Nutrition Per 100g:

Calories:
{product.get("energy-kcal_100g")}

Sugar:
{product.get("sugars_100g")}

Fat:
{product.get("fat_100g")}

Protein:
{product.get("proteins_100g")}

Salt:
{product.get("salt_100g")}

Fiber:
{product.get("fiber_100g")}

NutriScore:
{product.get("nutriscore_grade")}

NOVA Classification:
{product.get("nova_group")}

Additives:
{product.get("additives_tags")}

Allergens:
{product.get("allergens_tags")}

Environmental Grade:
{product.get("environmental_score_grade")}

========================
EVALUATION RULES
================

Evaluate based on:

1. Sugar content
2. Fat content
3. Salt content
4. Protein content
5. Fiber content
6. Calorie density
7. Ingredient quality
8. Artificial additives
9. NOVA processing level
10. NutriScore
11. Allergens
12. Environmental impact

Scoring Guidelines:

A = 80-100 (Excellent)
B = 60-79 (Good)
C = 40-59 (Average)
D = 20-39 (Poor)
E = 0-19 (Very Poor)

Important:

* Do NOT assume missing values are healthy.
* If nutrition data is missing, reduce confidence and score appropriately.
* Ultra-processed foods (NOVA 4) should generally score lower.
* High sugar, high salt, and excessive fat should reduce scores.
* Higher protein and fiber should improve scores.
* Favor simple ingredient lists and minimally processed foods.
* Be strict and realistic.
* A candy, chocolate bar, sugary cereal, soft drink, or highly processed snack should rarely receive a score above 40.

========================
OUTPUT FORMAT
=============

Return ONLY valid JSON.

{{
"health_score": 0,
"grade": "A",
"confidence": "High",

```
"summary": "",

"pros": [],

"cons": [],

"recommendation": ""
```

}}
"""

        try:
            response = self.llm.generate(prompt)

            response = response.strip()

            if response.startswith("```json"):
                response = response.replace(
                    "```json", ""
                ).replace(
                    "```", ""
                ).strip()

            return json.loads(response)

        except Exception as e:

            print("LLM Error:", e)

            return {
                "health_score": 50,
                "grade": "C",
                "summary": "Unable to analyze product",
                "pros": [],
                "cons": [],
                "recommendation": "Try again later"
            }
