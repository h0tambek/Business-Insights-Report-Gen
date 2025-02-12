import os
import pandas as pd
import requests
import json
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()

# Constants for external data source, these are mock services for now (will update with real callss)
COMPETITOR_API_URL = "https://api.competit0r.com/prices"
SUPPLY_CHAIN_API_URL = "https://api.supplystuff.com/restocking"

# Load the CSV file
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # Remove whitespace from column names
    df = df.rename(columns={"our_price": "price", "product_name": "name"})
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert price to float
    df['current_stock'] = pd.to_numeric(df['current_stock'], errors='coerce')  # Convert stock to numeric
    return df.dropna(subset=['name', 'price'])

# Fetch competitor pricing (mock function, will replace with API call)
def get_competitor_prices():
    response = requests.get(COMPETITOR_API_URL)  # Replace with actual API
    if response.status_code == 200:
        return response.json()
    return {}

# Fetch supply chain data (mock function, will replace with API call)
def get_supply_chain_data():
    response = requests.get(SUPPLY_CHAIN_API_URL)  # Replace with actual API
    if response.status_code == 200:
        return response.json()
    return {}

# Generate the insights for the business 
def generate_insights(df, competitor_data, supply_data):
    insights = []
    for index, row in df.iterrows():
        product = row['name']
        our_price = row['price']
        competitor_price = competitor_data.get(product, None)
        stock = row['current_stock']
        restock_threshold = row.get('restock_threshold', 10)
        supply_delay = supply_data.get(product, 0)
        
        if competitor_price:
            price_diff = our_price - competitor_price
            pricing_msg = f"{product}: Our price is {'higher' if price_diff > 0 else 'lower'} than competitors by ${abs(price_diff):.2f}."
            insights.append(pricing_msg)
        
        if stock <= restock_threshold:
            restock_msg = f"{product}: Low stock ({stock} left). Estimated restock delay: {supply_delay} days. Order soon."
            insights.append(restock_msg)
    
    return insights

# Save the insights to a report
def save_report(insights):
    with open("report.md", "w") as f:
        f.write("# Business Insights Report\n\n")
        for insight in insights:
            f.write(f"- {insight}\n")

if __name__ == "__main__":
    data_file = "data/products.csv"
    df = load_data(data_file)
    competitor_data = get_competitor_prices()
    supply_data = get_supply_chain_data()
    insights = generate_insights(df, competitor_data, supply_data)
    save_report(insights)
    print("Report generated: report.md")
