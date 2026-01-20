import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# READ SALES DATA

def read_sales_data(filename, encoding="utf-8"):
    data = []
    file_path = os.path.join(DATA_DIR, filename)

    try:
        with open(file_path, "r", encoding=encoding, newline="") as file:
            reader = csv.reader(file, delimiter="|")
            next(reader, None)  # skip header

            for row in reader:
                if row and any(field.strip() for field in row):
                    data.append("|".join(row))
        return data

    except UnicodeDecodeError:
        print(f"Encoding issue in {filename}")
        return []

    except FileNotFoundError:
        print(f"{filename} not found")
        return []



# PARSE TRANSACTIONS

def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        fields = line.split("|")
        if len(fields) != 8:
            continue

        try:
            transaction = {
                "TransactionID": fields[0].strip(),
                "Date": fields[1].strip(),
                "ProductID": fields[2].strip(),
                "ProductName": fields[3].replace(",", " ").strip(),
                "Quantity": int(fields[4].replace(",", "").strip()),
                "UnitPrice": float(fields[5].replace(",", "").strip()),
                "CustomerID": fields[6].strip(),
                "Region": fields[7].strip(),
            }
            transactions.append(transaction)

        except ValueError:
            continue

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
