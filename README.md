# 🥗 Food Health Analyzer

An AI-powered Food Health Analyzer that helps users identify food products and understand their nutritional quality using Computer Vision, Data Engineering, and Large Language Models.

The application allows users to search for products by name, scan barcodes, extract text from product packaging using OCR, or detect food products from images using YOLO. It then retrieves product information from a large-scale food database and generates easy-to-understand health insights.

---

## 🚀 Features

### 🔍 Product Search
- Search food products by name
- Fast retrieval using DuckDB and Apache Parquet
- Supports millions of food products

### 📷 Barcode Scanning
- Scan product barcodes from images
- Automatically identify products

### 📝 OCR-Based Product Recognition
- Extract product names from packaging using EasyOCR
- Useful when barcode scanning is unavailable

### 🎯 YOLO-Based Food Detection
- Detect food products directly from images
- Automatic product identification workflow

### 🤖 AI-Powered Health Analysis
- LangChain-powered workflow
- OpenRouter LLM integration
- Generates nutritional explanations
- Explains ingredients and additives
- Provides health recommendations

### 📊 Health Scoring
Analyzes:
- Calories
- Sugar
- Fat
- Saturated Fat
- Sodium/Salt
- Additives
- Nutri-Score

---

# 🏗️ System Architecture

```text
User Input
│
├── Product Name
├── Barcode Image
├── OCR Image
└── Food Image
        │
        ▼
 Computer Vision Layer
 ├── Barcode Scanner
 ├── EasyOCR
 └── YOLOv8
        │
        ▼
 DuckDB Search Engine
        │
        ▼
 Product Information
        │
        ▼
 LangChain + OpenRouter LLM
        │
        ▼
 Health Analysis
        │
        ▼
 User-Friendly Explanation
```

---

# 🛠️ Tech Stack

## Data Engineering
- Python
- DuckDB
- PyArrow
- Apache Parquet
- Pandas

## Computer Vision
- OpenCV
- EasyOCR
- YOLOv8
- Pyzbar

## AI & LLM
- LangChain
- OpenRouter
- Large Language Models (LLMs)

## Frontend
- Streamlit

---

# 📂 Project Structure

```text
food-health-analyzer/
│
├── app.py
│
├── food_project/
│
│   ├── core/
│   │   ├── search_engine.py
│   │   └── food_engine.py
│   │
│   ├── vision/
│   │   ├── barcode_scanner.py
│   │   ├── ocr_reader.py
│   │   └── yolo_detector.py
│   │
│   └── llm/
│       └── explanation_generator.py
│
├── data/
│
├── models/
│
├── requirements.txt
│
├── README.md
│
└── dataset_convert_in_PARQUET_form.ipynb
```

---

# 📊 Dataset

This project uses the Open Food Facts dataset.

### Dataset Source

Open Food Facts is one of the world's largest open food databases containing millions of food products and nutritional information.

Official Data Repository:

https://world.openfoodfacts.org/data

Downloaded Dataset:

https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz

### Original Dataset

| Format | Size |
|----------|----------|
| Compressed CSV (.gz) | ~0.9 GB |
| Uncompressed CSV | ~9 GB |

### Dataset Contents

The dataset contains:

- Product Names
- Brands
- Ingredients
- Nutrition Facts
- Calories
- Sugars
- Fat
- Saturated Fat
- Proteins
- Additives
- Allergens
- Nutri-Score
- NOVA Groups
- Countries
- Categories

and more than **200 product attributes**.

### Dataset Scale

- 4.5+ Million Food Products
- 200+ Columns
- Global Product Coverage

---

# ⚡ Dataset Optimization

Querying a 9 GB CSV file is slow for real-time applications.

To improve performance:

- Converted CSV dataset into Apache Parquet format
- Reduced storage overhead
- Improved query performance
- Enabled fast DuckDB analytics

### Conversion Notebook

The complete conversion process is available in:

`dataset_convert_in_PARQUET_form.ipynb`

GitHub Notebook:

https://github.com/ChanduBanglawala/food-health-analyzer/blob/main/datset_convert_in_PARQUET_form.ipynb

---

# ⚙️ Search Engine

The project uses:

- DuckDB
- Apache Parquet

to perform:

- Product Search
- Barcode Search
- Brand Search
- OCR Product Matching
- Product Detail Retrieval

without requiring a traditional database server.

---

# 🤖 AI-Powered Analysis

The application integrates:

- LangChain
- OpenRouter
- LLMs

to generate:

### Nutritional Insights

Example:

- Is the product healthy?
- Is the sugar level high?
- Are there harmful additives?
- Is the sodium content excessive?

### Ingredient Explanations

Example:

- What does this additive do?
- Is this preservative safe?
- Are there allergy concerns?

### Personalized Recommendations

Example:

- Suitable for weight loss?
- Suitable for children?
- Better alternatives?

---

# 📸 Product Identification Methods

## Method 1: Product Name Search

User enters:

```text
Kit Kat
```

System searches product database directly.

---

## Method 2: Barcode Scan

Upload barcode image.

System:

```text
Image
   ↓
Barcode Scanner
   ↓
Product Lookup
```

---

## Method 3: OCR

Upload product image.

System:

```text
Image
   ↓
EasyOCR
   ↓
Extract Product Name
   ↓
Search Database
```

---

## Method 4: YOLO Detection

Upload food image.

System:

```text
Image
   ↓
YOLOv8
   ↓
Food Detection
   ↓
Database Search
```

---

# 🚀 Installation

Clone repository:

```bash
git clone https://github.com/ChanduBanglawala/food-health-analyzer.git

cd food-health-analyzer

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📈 Future Improvements

- Vector Search using Embeddings
- RAG-based Ingredient Analysis
- Personalized Diet Recommendations
- Multi-language Support
- Mobile Application
- Voice-Based Food Search
- Nutrition Comparison Engine

---

# 🏆 Key Highlights

✅ 4.5+ Million Food Products

✅ DuckDB + Parquet Data Pipeline

✅ LangChain + OpenRouter Integration

✅ OCR-Based Product Recognition

✅ Barcode-Based Product Lookup

✅ YOLOv8 Food Detection

✅ AI-Generated Nutritional Insights

✅ Streamlit Web Application


---

## 🚀 Screenshots

Image Detection:

<img width="1365" height="674" alt="Screenshot 2026-06-20 173816" src="https://github.com/user-attachments/assets/e5260b21-cf15-462a-94ba-62c768efa8dd" />


Product Name:

<img width="1362" height="629" alt="Screenshot 2026-06-20 180818" src="https://github.com/user-attachments/assets/fe31a13c-e76b-4df2-9192-9b4b848b65f3" />

Video Sample:


# ⭐ If you found this project useful

Please consider starring the repository.
