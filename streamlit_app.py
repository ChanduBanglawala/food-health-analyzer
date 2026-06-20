import streamlit as st

from food_project.core.search_engine import SearchEngine
from food_project.core.food_engine import FoodEngine
from food_project.llm import explanation_generator
from food_project.vision import barcode_scanner
from food_project.vision.ocr_reader import OCRReader
from food_project.vision.yolo_detector import FoodDetector

PARQUET_PATH = r"C:\Users\neha\food_products.parquet"

engine = SearchEngine(PARQUET_PATH)
food_engine = FoodEngine()

st.set_page_config(
    page_title="Food Health Analyzer",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 Food Health Analyzer")

# ==================================================
# TABS
# ==================================================

tab1, tab2 = st.tabs(
    [
        "🔍 Product Search",
        "📷 Image Analysis"
    ]
)

product = None

# ==================================================
# TAB 1 - PRODUCT SEARCH
# ==================================================

with tab1:

    search = st.text_input(
        "Enter Product Name"
    )

    if st.button(
        "Search Product"
    ):

        if not search.strip():
            st.warning(
                "Please enter a product name"
            )
            st.stop()

        with st.spinner(
            "Searching products..."
        ):

            results = engine.search_product(
                search
            )

        if not results:
            st.error(
                "No products found"
            )

        else:

            selected = results[0]

            product = engine.search_barcode(
                selected["code"]
            )

# ==================================================
# TAB 2 - IMAGE ANALYSIS
# ==================================================

with tab2:

    uploaded_file = st.file_uploader(
        "Upload Food Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            width=300
        )

        if st.button(
            "Analyze Image"
        ):

            with st.spinner(
                "Analyzing image..."
            ):

                import tempfile
                import os

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".jpg"
                ) as tmp:

                    tmp.write(
                        uploaded_file.getbuffer()
                    )

                    image_path = tmp.name

                # ---------------------
                # YOLO Detection
                # ---------------------

                detector = FoodDetector()

                detected_objects = detector.detect(
                    image_path
                )

                if detected_objects:

                    st.success(
                        f"Detected Objects: {', '.join(detected_objects)}"
                    )

                # ---------------------
                # Barcode Scan
                # ---------------------

                barcode = barcode_scanner.scan_barcode(
                    image_path
                )

                if barcode:

                    st.success(
                        f"Barcode Found: {barcode}"
                    )

                    product = engine.search_barcode(
                        barcode
                    )

                else:

                    st.warning(
                        "No barcode detected. Using OCR..."
                    )

                    reader = OCRReader()

                    text = reader.extract_text(
                        image_path
                    )

                    st.write(
                        "Detected Text:",
                        text
                    )

                    results = engine.search_product(
                        text
                    )

                    if results:

                        st.success(
        "Matching product found."
    )

                        product = engine.search_barcode(
        results[0]["code"]
    )

                    else:
                        st.warning(
        "Product not found in database. Using AI analysis..."
    )

                        llm_response =explanation_generator.ExplanationGenerator(
                            text
                        )

                        st.markdown(llm_response)
    

            
        try:
                    os.remove(image_path)
        except:
                    pass
# ==================================================
# REPORT
# ==================================================

if product:

    report = food_engine.analyze(
        product
    )

    st.header(
        report["product_name"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Health Score",
            report["health_score"]["score"]
        )

    with col2:

        st.metric(
            "Grade",
            report["health_score"]["grade"]
        )

    with col3:

        st.metric(
            "Brand",
            report["brand"] or "Unknown"
        )

    st.divider()

    # AI ANALYSIS

    st.subheader(
        "🤖 AI Nutrition Analysis"
    )

    ai = report.get(
        "ai_explanation",
        {}
    )

    st.write(
        ai.get(
            "summary",
            "No AI summary available."
        )
    )

    st.subheader("✅ Pros")

    pros = ai.get(
        "pros",
        []
    )

    if pros:

        for item in pros:
            st.success(item)

    else:

        st.write(
            "No major advantages identified."
        )

    st.subheader("❌ Cons")

    cons = ai.get(
        "cons",
        []
    )

    if cons:

        for item in cons:
            st.error(item)

    else:

        st.write(
            "No major concerns identified."
        )

    st.subheader(
        "📌 Recommendation"
    )

    st.info(
        ai.get(
            "recommendation",
            "No recommendation available."
        )
    )

    st.divider()

    # NUTRITION

    st.subheader("🍽 Nutrition")
    st.json(report["nutrition"])

    st.subheader("🧪 Ingredients")
    st.json(report["ingredients"])

    st.subheader("⚠ Additives")
    st.json(report["additives"])

    st.subheader("🥜 Allergens")
    st.json(report["allergens"])

    st.subheader("🏭 NOVA Classification")
    st.json(report["nova"])

    st.subheader("🌍 Environmental Impact")
    st.json(report["environment"])