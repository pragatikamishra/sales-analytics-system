import csv
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# READ SALES DATA

def read_sales_data(filename,file_encoder): 
    try: 
        data = [] 
        with open(file=filename, mode='r', encoding=file_encoder,newline='\n',) as file: 
            file_content=csv.reader(file,delimiter='|') 
            header=next(file_content,None) #skip header 
            for row in file_content: 
                if row and any(field.strip() 
                    for field in row): 
                     data.append('|'.join(row))
            return data 
    except UnicodeDecodeError: 
        print(f'{filename} file is not in UTF-8 encoding') 
        return data 
    except FileNotFoundError: 
        print(f'{filename} file does not exist') 
        return data


# PARSE TRANSACTIONS

def parse_transactions(raw_lines): 
    transactions = [] 
    for line in raw_lines: 
         fields = line.split('|') 
         if len(fields) != 8:
              continue # Skip rows with incorrect number of fields 
         transaction_id = fields[0].strip() 
         date = fields[1].strip() 
         product_id = fields[2].strip() 
         product_name = fields[3].replace(',', ' ').strip() # Remove commas in ProductName 
         try: 
              quantity = int(fields[4].replace(',', '').strip()) # Remove commas and convert to int 
              unit_price = float(fields[5].replace(',', '').strip()) # Remove commas and convert to float 
         except ValueError: 
              continue # Skip rows with invalid numeric data 
         customer_id = fields[6].strip() 
         region = fields[7].strip() 
         transaction = { 'TransactionID': transaction_id, 
                        'Date': date, 
                        'ProductID': product_id, 
                        'ProductName': product_name, 
                        'Quantity': quantity, 
                        'UnitPrice': unit_price, 
                        'CustomerID': customer_id, 
                        'Region': region }
         transactions.append(transaction) 
    return transactions

# VALIDATE & FILTER


# def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
#     valid = []
#     invalid_count = 0

#     #validation
#     for tx in transactions:
#         if (
#             tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0 or
#             not tx["TransactionID"].startswith("T") or
#             not tx["ProductID"].startswith("P") or
#             not tx["CustomerID"].startswith("C")):
#             invalid_count += 1
#             continue
#         valid_transactions.append(tx)

#     total_input = len(transactions) 
#     filtered_by_region = 0 
#     filtered_by_amount = 0

#     # Filter by region 
#     if region: 
#         before_count = len(valid_transactions) 
#         valid_transactions = [tx for tx in valid_transactions 
#         if tx['Region'] == region] 
#         filtered_by_region = before_count - len(valid_transactions)

#     # Filter by amount
#     if min_amount is not None or max_amount is not None:
#          before_count = len(valid_transactions) 
#          def amount_filter(tx): 
#             amount = tx['Quantity'] * tx['UnitPrice'] 
#             if min_amount is not None and amount < min_amount: 
#                 return False
#             if max_amount is not None and amount > max_amount: 
#                 return False 
#             return True
#          valid_transactions = [tx for tx in valid_transactions if amount_filter(tx)] 
#          filtered_by_amount = before_count - len(valid_transactions) 
#          final_count = len(valid_transactions)

#          filter_summary = { 
#             'total_input': total_input,
#             'invalid': invalid_count, 
#             'filtered_by_region': filtered_by_region, 
#             'filtered_by_amount': filtered_by_amount, 
#             'final_count': final_count } 
#     return valid_transactions, invalid_count, filter_summary


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    try:
        # Validation
        for tx in transactions:
            if (tx['Quantity'] <= 0 or tx['UnitPrice'] <= 0 or
                not tx['TransactionID'].startswith('T') or
                not tx['ProductID'].startswith('P') or
                not tx['CustomerID'].startswith('C')):
                invalid_count += 1
                continue
            valid_transactions.append(tx)

        # Filter by region
        if region:
            valid_transactions = [tx for tx in valid_transactions if tx['Region'] == region]

        # Filter by amount
        if min_amount is not None or max_amount is not None:
            def amount_filter(tx):
                amt = tx['Quantity'] * tx['UnitPrice']
                if min_amount is not None and amt < min_amount:
                    return False
                if max_amount is not None and amt > max_amount:
                    return False
                return True
            valid_transactions = [tx for tx in valid_transactions if amount_filter(tx)]

        # Filter summary
        filter_summary = {
            "total_input": len(transactions),
            "invalid": invalid_count,
            "final_count": len(valid_transactions)
        }

        return valid_transactions, invalid_count, filter_summary

    except Exception as e:
        # Always return something so main.py doesn’t crash
        return [], 0, {"total_input": 0, "invalid": 0, "final_count": 0}
