import pandas as pd

# Generate a CSV file with improper product data
def generate_csv(file_path):
    products = [
        ["Organic Coffee Beans (1lb)", 14.99, "Beverages", 45, 25, "2024-11-15", "Be"],
        ["Premium Green Tea (50 bags)", 8.99, "Beverages", 32, 20, "2024-11-10", "Te"],
        ["Masala Chai Mix (12oz)", 9.99, "beverages", 18, 15, "2024-11-18", "Spice W"],
        ["Yerba Mate Loose Leaf (1lb)", "$12.99", "Beverages", 5, 10, "2024-11-01", "S"],
        ["Hot Chocolate Mix (1lb)", 7.99, "Beverages", 50, 30, "11/12/2024", "Sweet"],
        ["Earl Grey Tea (100 bags)", 11.99, "beverages", 28, 25, "2024-11-14", "Tea"],
        ["Espresso Beans (1lb)", 16.99, "Beverages", 22, 20, "2024-11-16", "Bean Bro"],
        ["Chamomile Tea (30 bags)", 6.99, "Tea", 12, 15, "2024-11-05", "Tea Time Imp"],
        ["Matcha Green Tea Powder (4oz)", 19.99, "Beverages", 8, None, "2024-11-17", "Te"],
        ["Decaf Coffee Beans (1lb)", 15.99, "Beverages", 15, 15, "2024-11-13", "Bean"],
        ["Mint Tea (25 bags)", 7.49, "Beverages", "out of stock", 12, "2024-10-30", "T"],
        ["Instant Coffee (8oz)", 11.99, "coffee", 25, 20, "2024-11-19", "Coffee Cor"],
        ["Rooibos Tea (40 bags)", None, "Beverages", 30, 20, "2024-11-08", "Tea Time Imp"],
        ["cold brew concentrate", 13.99, "Beverages", 19, 15, "2024-11-20", "Bean Br"]
    ]
    columns = ["product_name", "our_price", "category", "current_stock", "restock_threshold", "restock_date", "supplier"]
    df = pd.DataFrame(products, columns=columns)
    df.to_csv(file_path, index=False)
    print(f"CSV file generated at: {file_path}")

if __name__ == "__main__":
    generate_csv("data/products.csv")