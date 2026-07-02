# 🎯 Consolidated Customer Analytics & Insights Dashboard

An end-to-end data pipeline and interactive business intelligence solution designed to analyze customer demographics, evaluate campaign performance, and uncover spending behaviors across channels. This project processes a dataset of over 56,000 transaction records, implements rule-based segmentation, stores structured data in MySQL, and deploys a clean dashboard interface via Streamlit.

---

## 🚀 Key Business Objectives Met
* **Identify High-Value Targets:** Profile the top 10% of spenders to understand what drives brand engagement.
* **Optimize Marketing Spends:** Pinpoint the demographic variables (Income, Family Composition, Tenure) that trigger positive campaign conversion.
* **Unclutter Operations:** Break down multi-dimensional datasets into a structured, executive-ready dashboard using clear visual layouts, labels, and legends.

---

## 🛠️ Tech Stack & Architecture

* **Development Environment:** Visual Studio Code (Jupyter Notebook extensions)
* **Data Processing & Engineering:** Python, Pandas, NumPy
* **Data Storage & Pipeline:** MySQL Database Server, SQLAlchemy
* **Executive Visualization:** Streamlit Web Framework, Plotly Express

```text
[ Raw CSV Data ] 
       │ (Feature Engineering: Age, Tenure, Outliers Managed via Clipping)
       ▼
[ Segmented Data ] 
       │ (Literal Range Text Mapping via np.select)
       ▼
[ MySQL Database ] ───(Live Streaming Connection)───► [ Streamlit Executive UI ]
```

---

## 📊 Core Dataset Modifications

During the data engineering phase inside VS Code, the following analytical layers were successfully derived:
1. **Age Derivation:** Calculated dynamically by subtracting the birth year from the operational reference year (`2026`).
2. **Customer Loyalty Tracking:** Transformed the `Dt_Customer` column into a clear datetime datatype and generated a standardized `Customer_Tenure_Days` field based on a specific baseline milestone.
3. **Outlier Mitigation:** Identified 705 outlier records via Interquartile Range (IQR) analysis and applied the statistical `.clip()` boundary constraint to prevent data skewing without row count loss.
4. **Rule-Based Strategic Segmentation:** Derived 6 text-categorized operational profiles via `np.select` including:
   * **High Income:** Income > ₹75,000 (`75001–99999`)
   * **Young Customer:** Age < 30 (`18–29`)
   * **High Web Engagement:** Web visits > 5 (`6–20`)
   * **High Spender:** Total spend tracking above the dynamic 90th percentile boundary (`> ₹50,000`)

---

## 💻 Installation & Environment Setup

Ensure you have Python 3.9+ and MySQL installed locally.

### 1. Clone the Repository
```bash
git clone https://github.com
cd customer-analytics-dashboard
```

### 2. Install Project Dependencies
Run the following package script inside your terminal instance to install all operational pipeline connectors:
```bash
pip install pandas numpy streamlit plotly mysql-connector-python sqlalchemy
```

### 3. Initialize the Database Schema
Execute this script inside your local MySQL Workbench or database client interface:
```sql
CREATE DATABASE IF NOT EXISTS my_analytics_db;
USE my_analytics_db;

CREATE TABLE customers_spend (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year_birth INT,
    Age INT,
    Income DECIMAL(10,2),
    Total_Spend DECIMAL(10,2),
    Customer_Tenure_Days INT,
    Segment_High_Income VARCHAR(30),
    Segment_Young_Customer VARCHAR(20),
    Segment_Campaign_Responder VARCHAR(5),
    Segment_High_Web_Engagement VARCHAR(20),
    Segment_Family_Customer VARCHAR(20),
    Segment_High_Spender VARCHAR(30)
);
```

---

## ⚙️ Running the Applications

### 1. Execute Data Pipeline (Upload to MySQL)
Run the script to read your modified CSV, apply the segmentation configurations, and batch-upload the 56,000 rows into your MySQL Server instance:
```bash
python upload_to_mysql.py
```

### 2. Launch the Streamlit Dashboard Instance
To bypass default operating system shell command restrictions on Windows environments, spin up the local server utilizing the python module directly:
```bash
python -m streamlit run app.py
```

---

## 📈 Dashboard Layout & Visual Design

The user interface prioritizes clarity and context to deliver high-density information without visual clutter:
* **Global Control Filter Sidebar:** Enables immediate cross-filtering across categorical variables like Country, Education, Marital Status, Age bands, and Income bands.
* **Tab 1: Customer Profile Analysis:** Evaluates whether relationship retention drives revenue utilizing an annotated box plot mapping `Customer_Tenure_Days` against spending tiers.
* **Tab 2: Campaign Conversion Drivers:** Implements a 100% Stacked Bar Chart to capture exact conversion rate proportions across ascending earning buckets.
* **Tab 3: Omnichannel Demographics:** Tracks continuous web footprint averages (`NumWebVisitsMonth`) across cross-sectional demographic combinations.
