import requests
import os
def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses
        print(response.status_code) #if status code is 200, request is successful, if 500, server error
        data = response.json()
        products = data.get('products', [])
        print(f"Successfully fetched {len(products)} products.")
        return products
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch products: {e}")
        return []


def create_product_mapping(api_products):
    product_mapping = {}
    for product in api_products:
        product_id = product['id']
        product_info = {
            'title': product.get('title', 'N/A'),
            'category': product.get('category', 'N/A'),
            'brand': product.get('brand', 'N/A'),
            'rating': product.get('rating', 0)
        }
        product_mapping[product_id] = product_info
    return product_mapping

def enrich_sales_data(transactions, product_mapping):
    enriched_transactions = []

    for transaction in transactions:
        enriched = transaction.copy()

        # Default enrichment values
        enriched.update({
            "API_Category": None,
            "API_Brand": None,
            "API_Rating": None,
            "API_Match": False
        })

        product_id_str = transaction.get("ProductID", "")

        if isinstance(product_id_str, str) and product_id_str.startswith("P"):
            try:
                product_id = int(product_id_str[1:])
                product_info = product_mapping.get(product_id)

                if product_info:
                    enriched["API_Category"] = product_info.get("category")
                    enriched["API_Brand"] = product_info.get("brand")
                    enriched["API_Rating"] = product_info.get("rating")
                    enriched["API_Match"] = True

            except ValueError:
                pass  # Invalid numeric part

        enriched_transactions.append(enriched)

    return enriched_transactions

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions to a text file in the 'data' folder.
    Ensures folder exists.
    """
    # Ensure folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8', newline='') as file:
        header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
        file.write(header)
        for t in enriched_transactions:
            line = "|".join([
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")),
                str(t.get("Quantity", 0)),
                str(t.get("UnitPrice", 0.0)),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category", "")),
                str(t.get("API_Brand", "")),
                str(t.get("API_Rating", "")),
                "Yes" if t.get("API_Match", False) else "No"
            ]) + "\n"
            file.write(line)
    return filename


import os
from datetime import datetime
from collections import defaultdict
def generate_sales_report(enriched_transactions, transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive report in the 'output' folder.
    Ensures folder exists.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    # -----------------------------
    # Pre-processing
    # -----------------------------
    total_revenue = 0.0
    dates = []
    region_sales = defaultdict(float)
    region_transactions = defaultdict(int)
    product_qty = defaultdict(int)
    product_revenue = defaultdict(float)
    customer_spend = defaultdict(float)
    customer_orders = defaultdict(set)
    daily_data = defaultdict(lambda: {"revenue": 0.0, "transactions": 0, "customers": set()})

    for t in transactions:
        quantity = t.get("Quantity", 0)
        unit_price = t.get("UnitPrice", 0.0)
        revenue = quantity * unit_price
        total_revenue += revenue

        date = t.get("Date", "N/A")
        dates.append(date)

        region = t.get("Region", "Unknown")
        region_sales[region] += revenue
        region_transactions[region] += 1

        product = t.get("ProductName", "Unknown")
        product_qty[product] += quantity
        product_revenue[product] += revenue

        customer = t.get("CustomerID", "Unknown")
        customer_spend[customer] += revenue
        customer_orders[customer].add(date)

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transactions"] += 1
        daily_data[date]["customers"].add(customer)

    total_transactions = total_records
    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # -----------------------------
    # Top entities
    # -----------------------------
    top_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
    top_customers = sorted(customer_spend.items(), key=lambda x: x[1], reverse=True)[:5]

    best_selling_day = max(daily_data.items(), key=lambda x: x[1]["revenue"])[0] if daily_data else "N/A"
    low_products = [p for p, qty in product_qty.items() if qty < 5]  # low quantity products

    # -----------------------------
    # API Enrichment Summary
    # -----------------------------
    enriched_total = len(enriched_transactions)
    success_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    failed_products = [t.get("ProductName", "Unknown") for t in enriched_transactions if not t.get("API_Match")]
    success_rate = (success_count / enriched_total * 100) if enriched_total else 0

    # -----------------------------
    # Report Writing
    # -----------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 44 + "\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {now}\n")
        f.write(f"     Records Processed: {total_records}\n")
        f.write("=" * 44 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':10}{'Sales':15}{'% of Total':12}{'Transactions'}\n")
        for region, sales in sorted(region_sales.items(), key=lambda x: x[1], reverse=True):
            percent = (sales / total_revenue * 100) if total_revenue else 0
            f.write(f"{region:10}₹{sales:13,.2f}  {percent:8.2f}%     {region_transactions[region]}\n")
        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':5}{'Product':25}{'Qty Sold':10}{'Revenue'}\n")
        for i, (prod, rev) in enumerate(top_products, 1):
            f.write(f"{i:<5}{prod:25}{product_qty[prod]:<10}₹{rev:,.2f}\n")
        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':5}{'Customer ID':15}{'Total Spent':15}{'Orders'}\n")
        for i, (cust, spent) in enumerate(top_customers, 1):
            f.write(f"{i:<5}{cust:15}₹{spent:13,.2f}  {len(customer_orders[cust])}\n")
        f.write("\n")

        # DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Date':12}{'Revenue':15}{'Txns':8}{'Customers'}\n")
        for date in sorted(daily_data):
            d = daily_data[date]
            f.write(f"{date:12}₹{d['revenue']:13,.2f}  {d['transactions']:<8}{len(d['customers'])}\n")
        f.write("\n")

        # PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best Selling Day: {best_selling_day}\n")
        f.write("Low Performing Products:\n")
        for p in low_products:
            f.write(f" - {p}\n")
        f.write("\nAverage Transaction Value per Region:\n")
        for r in region_sales:
            avg = region_sales[r] / region_transactions[r]
            f.write(f" - {r}: ₹{avg:,.2f}\n")
        f.write("\n")

        # API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Products Enriched: {enriched_total}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Failed Products:\n")
        for p in failed_products:
            f.write(f" - {p}\n")

    return output_file

