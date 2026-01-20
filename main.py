import os
from utils.file_handler import (read_sales_data, parse_transactions, validate_and_filter)
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data,
    generate_sales_report
)

def main():
    print("="*40)
    print("       SALES ANALYTICS SYSTEM")
    print("="*40)
    
    try:
        
        # 1. Read Sales Data
        
        print("\n[1/10] Reading sales data...")
        filename = "data/sales_data.txt"
        raw_data = read_sales_data(filename, file_encoder="utf-8")
        if not raw_data:
            print(f"✗ No data read from {filename}. Exiting.")
            return
        print(f"✓ Successfully read {len(raw_data)} transactions")

       
        # 2. Parse Transactions
       
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Display Filter Options

        regions = sorted(set(t["Region"] for t in transactions))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        min_amt, max_amt = min(amounts), max(amounts)
        print("\n[3/10] Filter Options Available:")
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}")

        filter_choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        region_filter = None
        min_amount_filter = None
        max_amount_filter = None
        if filter_choice == "y":
            region_filter = input("Enter region to filter (or leave blank): ").strip() or None
            min_amount_input = input(f"Enter minimum amount (₹{min_amt:,.0f}): ").strip()
            max_amount_input = input(f"Enter maximum amount (₹{max_amt:,.0f}): ").strip()
            min_amount_filter = float(min_amount_input) if min_amount_input else None
            max_amount_filter = float(max_amount_input) if max_amount_input else None

        
        # 4. Validate and Filter Transactions
       
        print("\n[4/10] Validating transactions...")
        valid_tx, invalid_count, filter_summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_amount_filter,
            max_amount=max_amount_filter
        )
        print(f"✓ Valid: {filter_summary['final_count']} | Invalid: {filter_summary['invalid']}")

    
        # 5. Data Analysis
      
        print("\n[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_tx)
        region_stats = region_wise_sales(valid_tx)
        top_products = top_selling_products(valid_tx)
        customer_stats = customer_analysis(valid_tx)
        daily_stats = daily_sales_trend(valid_tx)
        peak_day = find_peak_sales_day(valid_tx)
        low_products = low_performing_products(valid_tx)
        print("✓ Analysis complete")

       
        # 6. Fetch Products from API
  
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

      
        # 7. Enrich Sales Data

        print("\n[7/10] Enriching sales data...")
        enriched_tx = enrich_sales_data(valid_tx, product_mapping)
        success_count = sum(1 for t in enriched_tx if t.get("API_Match"))
        success_rate = (success_count / len(valid_tx) * 100) if valid_tx else 0
        print(f"✓ Enriched {success_count}/{len(valid_tx)} transactions ({success_rate:.1f}%)")

        # 8. Save Enriched Data
        enriched_file = save_enriched_data(enriched_tx, filename="data/enriched_sales_data.txt")
        print(f"✓ Saved to: {enriched_file}")

        # 9. Generate Report
        report_file = generate_sales_report(enriched_tx, enriched_tx, output_file="output/sales_report.txt")
        print(f"✓ Report saved to: {report_file}")


        # 10. Complete
       
        print("\n[10/10] Process Complete!")
        print("="*40)

    except Exception as e:
        print(f"\n✗ An error occurred: {e}")

if __name__ == "__main__":
    main()
