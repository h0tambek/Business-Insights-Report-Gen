# Business Insights Report Generator

This project automates the process of gathering competitor pricing data and generating business insights.

## 🚀 Features
- Fetches competitor prices from PriceAPI
- Generates insights based on price comparisons and stock levels
- Saves insights into a markdown report (`report.md`)

## 📜 Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/h0tambek/Business-Insights-Report-Gen.git
cd Business-Insights-Report-Gen
```

### 2️⃣ Install Dependencies
Make sure you have Python installed. Then, install the required packages:
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys
1. Rename `.env.example` to `.env`:
   ```sh
   mv .env.example .env   # macOS/Linux
   ren .env.example .env   # Windows (cmd)
   ```
2. Open `.env` and add your price api key:
   ```ini
   PRICE_API_KEY=your_priceapi_key
   ```
   **⚠️ DO NOT share your `.env` file. It contains sensitive data.**

### 4️⃣ Run the Script
Execute the analysis script:
```sh
python analysis.py
```

## 📊 How It Works
1. Loads your product data from `data/products.csv`
2. Fetches competitor prices using PriceAPI
3. Compares your prices with competitors
4. Generates insights and saves them in `report.md`

## ⚠️ Known Issues & Limitations
- Some product names may not match competitor listings exactly.
- API rate limits apply (check [PriceAPI docs](https://www.priceapi.com/)).
- No real-time stock updates; ensure `products.csv` is updated manually.

## 🕒 Time Spent on Each Component
- **Data handling & API integration:** 3 hours
- **Insight generation logic:** 2 hours
- **Code refactoring & testing:** 2 hours
- **Documentation & README:** 1 hour

## 🛠 Dependencies
- Python 3.x
- `requests`
- `pandas`
- `dotenv`
