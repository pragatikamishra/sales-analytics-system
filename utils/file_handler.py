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

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid_count = 0

    for tx in transactions:
        if (
            tx["Quantity"] <= 0
            or tx["UnitPrice"] <= 0
            or not tx["TransactionID"].startswith("T")
            or not tx["ProductID"].startswith("P")
            or not tx["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue
        valid.append(tx)

    before = len(valid)

    if region:
        valid = [t for t in valid if t["Region"] == region]

    if min_amount is not None or max_amount is not None:
        def amount_ok(t):
            amt = t["Quantity"] * t["UnitPrice"]
            if min_amount and amt < min_amount:
                return False
            if max_amount and amt > max_amount:
                return False
            return True

        valid = [t for t in valid if amount_ok(t)]

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid),
        "filtered": before - len(valid),
    }

    return valid, summary
