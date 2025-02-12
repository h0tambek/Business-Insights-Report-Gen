import os
import time
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import utils  # Import that utils module

# Load environment variables
load_dotenv()

# API Credentials (shhh) 
PRICE_API_KEY = os.getenv("PRICE_API_KEY")

# API URLs
PRICE_API_URL = "https://api.priceapi.com/v2/jobs"
PRICE_API_RESULTS_URL = "https://api.priceapi.com/v2/jobs"

# Load CSV Data  and clean that up cuz we can't even have digital bacteria in this house 
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"our_price": "price", "product_name": "name"})
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['current_stock'] = pd.to_numeric(df['current_stock'], errors='coerce')
    return df.dropna(subset=['name', 'price'])

# Step 1: Create Bulk Request for Competitor Prices im  using price api here
def create_bulk_request(product_names):
    response = requests.post(PRICE_API_URL, json={
        "token": PRICE_API_KEY,
        "source": "google_shopping",
        "topic": "product_and_offers",
        "country": "us",
        "key": "term",
        "values": product_names  
    })

    if response.status_code == 200:
        data = response.json()
        print(f"Bulk request created. Job ID: {data['job_id']}")
        return data["job_id"]
    else:
        print(f"Failed to create bulk request: {response.text}")
        return None

# Step 2: Check Job Status Until Finished
def wait_for_job_completion(job_id):
    status_url = f"{PRICE_API_RESULTS_URL}/{job_id}?token={PRICE_API_KEY}"
    while True:
        response = requests.get(status_url)
        if response.status_code == 200:
            data = response.json()
            print(f"Job status: {data['status']} (Progress: {data.get('progress', 0)}%)")

            if data["status"] == "finished":
                print("Job finished, fetching results...")
                return True
        else:
            print(f"Failed to check job status: {response.text}")
            return False

        time.sleep(10)  # Wait 10 seconds before checking again

# Step 3: view the json for the Competitor Price Results
def get_competitor_prices(job_id):
    response = requests.get(f"{PRICE_API_RESULTS_URL}/{job_id}/download.json?token={PRICE_API_KEY}")

    if response.status_code == 200:
        data = response.json()
        competitor_prices = {}

        for product in data.get("results", []):
            if product["success"] and product["content"]:
                try:
                    product_name = product["query"]["value"]
                    offers = product["content"].get("offers", [])
                    
                    prices = [float(offer["price_with_shipping"]) for offer in offers if "price_with_shipping" in offer]
                    
                    if prices:
                        competitor_prices[product_name] = min(prices)
                    else:
                        print(f"No valid prices found for {product_name}")
                except Exception as e:
                    print(f"Error extracting price for {product_name}: {e}")

        print("Competitor prices extracted:", competitor_prices)
        return competitor_prices
    else:
        print(f"Failed to get competitor prices: {response.text}")
        return {}

# Generate those insights
def generate_insights(df, competitor_data):
    insights = []

    for _, row in df.iterrows():
        product, our_price = row['name'], row['price']
        competitor_price = competitor_data.get(product)
        stock, restock_threshold = row['current_stock'], row.get('restock_threshold', 10)

        # Competitor price comparison
        if competitor_price is not None:
            price_diff = our_price - competitor_price
            insights.append(f"{product}: Our price is {'higher' if price_diff > 0 else 'lower'} than competitors by ${abs(price_diff):.2f}.")
        else:
            insights.append(f"{product}: No competitor prices found.")

        # Low stock warning
        if stock <= restock_threshold:
            insights.append(f"{product}: Low stock ({stock} left). Order soon.")

    # Useful Insight: Pricing Strategy
    high_priced_products = [p for p, price in competitor_data.items() if df[df['name'] == p]['price'].values[0] > price]
    if high_priced_products:
        insights.append(f"Pricing Alert: {len(high_priced_products)} products are priced higher than competitors. Consider revising pricing strategies.")

    return insights

# Save report
def save_report(insights):
    with open("report.md", "w", encoding="utf-8") as f:
        f.write("# Business Insights Report\n\n")
        f.write("## Insights\n\n")
        for insight in insights:
            f.write(f"- {insight}\n")
        
        # Document External Data Source
        f.write("\n## Data Sources\n")
        f.write("- **PriceAPI**: Used to fetch competitor product prices from Google Shopping. Provides real-time pricing for market analysis. More details at [PriceAPI](https://www.priceapi.com).\n")


if __name__ == "__main__":
    data_file = "data/products.csv"

    # Generate the CSV file if not there already
    if not os.path.exists(data_file):
        utils.generate_csv(data_file)

    df = load_data(data_file)
    product_names = df['name'].tolist()

    # Step 1: Request competitor prices
    job_id = create_bulk_request(product_names)
    if job_id and wait_for_job_completion(job_id):
        competitor_data = get_competitor_prices(job_id)
    else:
        competitor_data = {}

    # Step 2: Generate insights
    insights = generate_insights(df, competitor_data)

    # Step 3: Save the report
    save_report(insights)

    print("\n✅ Report generated: report.md")
