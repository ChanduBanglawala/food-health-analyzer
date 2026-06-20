"""
search_engine.py

Fast product search using DuckDB + Parquet
"""

from pathlib import Path

import duckdb
from rapidfuzz import fuzz


class SearchEngine:

    def __init__(self, parquet_path: str):

        self.parquet_path = parquet_path

        if not Path(parquet_path).exists():
            raise FileNotFoundError(
                f"Parquet file not found: {parquet_path}"
            )

        self.con = duckdb.connect()

        # Faster for large datasets
        self.con.execute("""
            PRAGMA threads=8;
        """)

        self.con.execute(f"""
            CREATE OR REPLACE VIEW products AS
            SELECT *
            FROM read_parquet('{parquet_path}')
        """)

    # --------------------------------------------------
    # Barcode Search
    # --------------------------------------------------

    def search_barcode(self, barcode: str):

        result = self.con.execute(
            """
            SELECT *
            FROM products
            WHERE code = ?
            LIMIT 1
            """,
            [str(barcode)]
        ).fetchdf()

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    # --------------------------------------------------
    # Product Search
    # --------------------------------------------------

    def search_product(
        self,
        query_text: str,
        limit: int = 10
    ):

        result = self.con.execute(
            """
            SELECT
                code,
                product_name,
                brands,
                nutriscore_grade,
                nova_group
            FROM products
            WHERE
                (
                    product_name IS NOT NULL
                    AND lower(product_name)
                        LIKE lower(?)
                )
                OR
                (
                    brands IS NOT NULL
                    AND lower(brands)
                        LIKE lower(?)
                )
                OR
                (
                    generic_name IS NOT NULL
                    AND lower(generic_name)
                        LIKE lower(?)
                )
            LIMIT ?
            """,
            [
                f"%{query_text}%",
                f"%{query_text}%",
                f"%{query_text}%",
                limit
            ]
        ).fetchdf()

        return result.to_dict("records")

    # --------------------------------------------------
    # Brand Search
    # --------------------------------------------------

    def search_brand(
        self,
        brand: str,
        limit: int = 10
    ):

        result = self.con.execute(
            """
            SELECT
                code,
                product_name,
                brands,
                nutriscore_grade,
                nova_group
            FROM products
            WHERE
                brands IS NOT NULL
                AND lower(brands)
                    LIKE lower(?)
            LIMIT ?
            """,
            [
                f"%{brand}%",
                limit
            ]
        ).fetchdf()

        return result.to_dict("records")

    # --------------------------------------------------
    # OCR / Fuzzy Search
    # --------------------------------------------------

    def search_product_fuzzy(
        self,
        text: str,
        limit: int = 50
    ):

        text = text.lower().strip()

        # OCR corrections
        text = text.replace("0", "o")
        text = text.replace("1", "l")
        text = text.replace("5", "s")

        direct_results = self.search_product(
            text,
            limit
        )

        if direct_results:

            ranked = sorted(
                direct_results,
                key=lambda x: fuzz.ratio(
                    text,
                    str(
                        x.get(
                            "product_name",
                            ""
                        )
                    ).lower()
                ),
                reverse=True
            )

            return ranked[:10]

        all_results = []

        for word in text.split():

            if len(word) < 3:
                continue

            results = self.search_product(
                word,
                limit
            )

            all_results.extend(results)

        if not all_results:
            return []

        ranked = sorted(
            all_results,
            key=lambda x: fuzz.partial_ratio(
                text,
                str(
                    x.get(
                        "product_name",
                        ""
                    )
                ).lower()
            ),
            reverse=True
        )

        seen = set()
        unique = []

        for item in ranked:

            code = item.get("code")

            if code not in seen:
                seen.add(code)
                unique.append(item)

        return unique[:10]

    # --------------------------------------------------
    # Full Product
    # --------------------------------------------------

    def get_product(
        self,
        barcode: str
    ):
        return self.search_barcode(barcode)

    # --------------------------------------------------
    # Close
    # --------------------------------------------------

    def close(self):
        self.con.close()


if __name__ == "__main__":

    engine = SearchEngine(
        "data/food_products.parquet"
    )

    print("\nBarcode Search")
    print("-" * 50)

    print(
        engine.search_barcode(
            "3017620422003"
        )
    )

    print("\nProduct Search")
    print("-" * 50)

    print(
        engine.search_product(
            "nutella"
        )[:3]
    )

    print("\nFuzzy Search")
    print("-" * 50)

    print(
        engine.search_product_fuzzy(
            "nutelia 400g"
        )[:3]
    )

    engine.close()