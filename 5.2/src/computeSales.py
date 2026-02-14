#!/usr/bin/env python3
"""
computeSales.py

Compute total sales cost based on a price catalogue and sales record.
"""

import json
import sys
import time
from pathlib import Path


def load_json_file(file_path):
    """
    Load a JSON file and return its content.

    Args:
        file_path (str): Path to JSON file.

    Returns:
        dict or list: Parsed JSON content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ERROR: File not found -> {file_path}")
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format -> {file_path}")
    except OSError as exc:
        print(f"ERROR: Cannot read file {file_path} -> {exc}")
    return None


def build_price_dictionary(price_catalogue):
    """
    Build a dictionary for quick product price lookup.

    Args:
        price_catalogue (list): List of product dictionaries.

    Returns:
        dict: Dictionary with product name as key and price as value.
    """
    price_dict = {}
    for product in price_catalogue:
        try:
            name = product["title"]
            price = float(product["price"])
            price_dict[name] = price
        except (KeyError, ValueError, TypeError):
            print(f"WARNING: Invalid product entry skipped -> {product}")
    return price_dict


def compute_sales_total(price_dict, sales_record):
    """
    Compute total sales cost.

    Args:
        price_dict (dict): Product price dictionary.
        sales_record (list): List of sales transactions.

    Returns:
        float: Total sales cost.
    """
    total_cost = 0.0

    for sale in sales_record:
        try:
            product_name = sale["title"]
            quantity = int(sale["quantity"])

            if product_name not in price_dict:
                print(f"WARNING: Product not found -> {product_name}")
                continue

            if quantity < 0:
                print(f"WARNING: Negative quantity -> {sale}")
                continue

            total_cost += price_dict[product_name] * quantity

        except (KeyError, ValueError, TypeError):
            print(f"WARNING: Invalid sale entry skipped -> {sale}")

    return total_cost


def write_results(total_cost, elapsed_time):
    """
    Write results to SalesResults.txt file.

    Args:
        total_cost (float): Computed total cost.
        elapsed_time (float): Execution time.
    """
    output_text = (
        "SALES RESULTS\n"
        "-------------------------\n"
        f"Total Sales: ${total_cost:,.2f}\n"
        f"Execution Time: {elapsed_time:.6f} seconds\n"
    )

    print(output_text)

    try:
        with open("SalesResults.txt", "w", encoding="utf-8") as file:
            file.write(output_text)
    except OSError as exc:
        print(f"ERROR: Could not write results file -> {exc}")


def main():
    """
    Main function.
    """
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    start_time = time.time()

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    if not Path(price_file).is_file() or not Path(sales_file).is_file():
        print("ERROR: One or both files do not exist.")
        sys.exit(1)

    price_catalogue = load_json_file(price_file)
    sales_record = load_json_file(sales_file)

    if price_catalogue is None or sales_record is None:
        print("ERROR: Cannot process files due to previous errors.")
        sys.exit(1)

    price_dict = build_price_dictionary(price_catalogue)
    total_cost = compute_sales_total(price_dict, sales_record)

    elapsed_time = time.time() - start_time

    write_results(total_cost, elapsed_time)


if __name__ == "__main__":
    main()