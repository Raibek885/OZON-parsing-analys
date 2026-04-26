# Ozon Data Intelligence Pipeline: From Scraping to Predictive Modeling

This project represents the full data lifecycle for the **Ozon** marketplace: from bypassing advanced anti-bot systems and data scraping to deep cleaning, feature engineering, and building predictive models.

## 🛠 Tech Stack
* **Data Sourcing:** Python, Selenium, `undetected-chromedriver`.
* **Data Processing:** Pandas, NumPy.
* **Feature Engineering & Modeling:** Scikit-learn, CatBoost/XGBoost/LightGBM.
* **Visualization:** Matplotlib, Seaborn, Plotly.

---

## 🚀 Quick Start

### 1. Install Dependencies
Ensure you have Python 3.9+ installed and run the following command:
```bash
pip install -r requirements.txt
```

### 2. Parser Configuration (Bypassing Protection)
Ozon utilizes robust anti-fraud systems. To prevent the script from getting banned instantly, you must mimic a real user session by extracting your personal cookies and headers:

1. Open [Ozon](https://www.ozon.ru) in your browser.
2. Open Developer Tools (**F12**) and navigate to the **Network** tab.
3. Filter the requests by **XHR**.
4. Look for a request where the URL contains `pixis` (this is Ozon's internal API for fetching product data).
5. Right-click on the request -> **Copy** -> **Copy as cURL (bash)**.
6. Go to [convertcurl.com](https://convertcurl.com/) and paste your copied cURL command.
7. Extract the `cookies` and `headers` from the output and paste them into your parser's configuration file or environment variables.

### 3. Why Undetected Chromedriver?
We use the `undetected-chromedriver` library because standard Selenium leaves specific "fingerprints" (webdriver flags) that are immediately flagged and banned by Ozon and Cloudflare. This library patches the Chrome binary on the fly, allowing us to bypass automation detection and scrape safely.

---

## 🔄 Data Lifecycle (Workflow)

### Stage 1: Data Scraping (Parsing)
The scraping process is split into two steps for maximum speed and fault tolerance:
1. **`parsing_links.py`**: First, open this script to collect the direct links to product cards from search results or specific categories.
2. **`parsing_cards.py`**: Next, run this script to iterate through the collected links and extract full product specifications. 
   * *Note:* We do not parse raw HTML. The script fetches data by directly calling Ozon's **internal API**, which returns a clean, structured JSON containing all product characteristics.

### Stage 2: Data Cleaning
Run the cleaning script to sanitize the raw data:
* Drops duplicates.
* Removes hard errors and garbage data.
* Handles missing values (imputation).
* Fixes data types (e.g., converting string prices to floats).

### Stage 3: Feature Engineering
Open **`feat_eng.ipynb`**:
This is where raw data is transformed into predictive features:
* Parsing nested JSON characteristics into distinct columns.
* Calculating discount percentages and processing dates.
* Categorical encoding and generating synthetic metrics (e.g., score weights based on review counts).

### Stage 4: Visualization & EDA
* Visualizing price distributions across categories.
* Plotting feature correlation matrices.
* Analyzing market niches and competitor density to uncover business insights.

### Stage 5: Modeling
Training Machine Learning models to predict target metrics (e.g., pricing trends or sales probability):
* Algorithm selection and baseline testing.
* Hyperparameter tuning.
* Model evaluation using standard metrics (RMSE, MAE, R²).

---

## 📂 Data Storage

All datasets are stored in the `/data` directory and are strictly versioned according to their pipeline stage:

* `data/raw/` — Primary "dirty" data immediately after scraping (JSON/CSV).
* `data/cleaned/` — Sanitized data after removing errors and duplicates. The final dataset containing engineered features, ready to be fed into the ML model.
