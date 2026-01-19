def calculate_total_revenue(transactions):
    total_revenue = 0.0
    for txn in transactions:
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        total_revenue += quantity * unit_price
    return round(total_revenue, 2)


def region_wise_sales(transactions):
    region_stats = {}
    total_sales = 0.0
    for txn in transactions:
        region = txn.get("Region", "Unknown")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        sales_amount = quantity * unit_price
        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }
        region_stats[region]['total_sales'] += sales_amount
        region_stats[region]['transaction_count'] += 1
        total_sales += sales_amount
    for region, stats in region_stats.items():
        stats['percentage'] = round((stats['total_sales'] / total_sales) * 100, 2) if total_sales > 0 else 0.0
    sorted_region_stats = dict(sorted(region_stats.items(), key=lambda item: item[1]['total_sales'], reverse=True))
    return sorted_region_stats


def top_selling_products(transactions, n=5):
    product_stats = {}
    for txn in transactions:
        product = txn.get("ProductName", "Unknown")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        revenue = quantity * unit_price
        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }
        product_stats[product]['total_quantity'] += quantity
        product_stats[product]['total_revenue'] += revenue
    sorted_products = sorted(product_stats.items(), key=lambda item: item[1]['total_quantity'], reverse=True)
    top_n_products = [
        (product, stats['total_quantity'], round(stats['total_revenue'], 2))
        for product, stats in sorted_products[:n]
    ]
    return top_n_products


def customer_analysis(transactions):
    customer_stats = {}
    for txn in transactions:
        customer_id = txn.get("CustomerID", "Unknown")
        product = txn.get("ProductName", "Unknown")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        amount_spent = quantity * unit_price
        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
        customer_stats[customer_id]['total_spent'] += amount_spent
        customer_stats[customer_id]['purchase_count'] += 1
        customer_stats[customer_id]['products_bought'].add(product)
    for customer_id, stats in customer_stats.items():
        stats['avg_order_value'] = round(stats['total_spent'] / stats['purchase_count'], 2) if stats['purchase_count'] > 0 else 0.0
        stats['products_bought'] = list(stats['products_bought'])
        stats['total_spent'] = round(stats['total_spent'], 2)
    sorted_customer_stats = dict(sorted(customer_stats.items(), key=lambda item: item[1]['total_spent'], reverse=True))
    return sorted_customer_stats


def daily_sales_trend(transactions):
    date_stats = {}
    for txn in transactions:
        date = txn.get("Date", "Unknown")
        customer_id = txn.get("CustomerID", "Unknown")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        revenue = quantity * unit_price
        if date not in date_stats:
            date_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }
        date_stats[date]['revenue'] += revenue
        date_stats[date]['transaction_count'] += 1
        date_stats[date]['unique_customers'].add(customer_id)
    for date, stats in date_stats.items():
        stats['unique_customers'] = len(stats['unique_customers'])
        stats['revenue'] = round(stats['revenue'], 2)
    sorted_date_stats = dict(sorted(date_stats.items(), key=lambda item: item[0]))
    return sorted_date_stats


def find_peak_sales_day(transactions):
    date_stats = daily_sales_trend(transactions)   
    peak_date = None
    max_revenue = 0.0
    for date, stats in date_stats.items():
        if stats['revenue'] > max_revenue:
            max_revenue = stats['revenue']
            peak_date = date
    if peak_date is not None:
        peak_stats = date_stats[peak_date]
        return (peak_date, peak_stats['revenue'], peak_stats['transaction_count'])
    else:
        return (None, 0.0, 0)
    

def low_performing_products(transactions, threshold=10):
    product_stats = {}
    for txn in transactions:
        product = txn.get("ProductName", "Unknown")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        revenue = quantity * unit_price
        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }
        product_stats[product]['total_quantity'] += quantity
        product_stats[product]['total_revenue'] += revenue
    low_performers = [
        (product, stats['total_quantity'], round(stats['total_revenue'], 2))
        for product, stats in product_stats.items()
        if stats['total_quantity'] < threshold
    ]
    low_performers.sort(key=lambda x: x[1])  # Sort by TotalQuantity ascending
    return low_performers