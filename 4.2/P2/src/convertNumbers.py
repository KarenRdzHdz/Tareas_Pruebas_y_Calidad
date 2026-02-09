"""
convertNumbers.py

Reads a file containing numbers and converts each valid number
to binary and hexadecimal using basic algorithms.

Invalid data is reported but does not stop execution.
Results are printed to the console and saved to
ConvertionResults.txt along with execution time.
"""

# pylint: disable=invalid-name

import sys
import time


def read_numbers(file_name):
    """
    Reads integer numbers from a file.

    Args:
        file_name (str): File containing numeric data.

    Returns:
        list: Valid integers.
    """
    numbers = []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                value = line.strip()

                try:
                    number = int(value)
                    numbers.append(number)
                except ValueError:
                    print(
                        f"Invalid data at line {line_number}: '{value}'"
                    )

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    if not numbers:
        print("Error: No valid numbers found.")
        sys.exit(1)

    return numbers


def decimal_to_binary(number):
    """
    Converts decimal to binary.
    Positive -> minimal bits.
    Negative -> minimal two's complement
    rounded to multiple of 4.
    """

    if number >= 0:
        if number == 0:
            return "0"

        binary = ""
        value = number

        while value > 0:
            binary = str(value % 2) + binary
            value //= 2

        return binary

    # NEGATIVE
    abs_value = abs(number)

    bits = abs_value.bit_length() + 1

    # round to multiple of 4
    if bits % 4 != 0:
        bits += 4 - (bits % 4)

    value = (1 << bits) + number

    binary = ""

    while value > 0:
        binary = str(value % 2) + binary
        value //= 2

    return binary.zfill(bits)


def binary_to_hexadecimal(binary, original_number):
    hex_chars = "0123456789ABCDEF"

    if original_number < 0:
        # extend sign to 32 bits
        binary = binary.rjust(32, '1')

    else:
        padding = (4 - len(binary) % 4) % 4
        binary = ("0" * padding) + binary

    hexadecimal = ""

    for i in range(0, len(binary), 4):
        group = binary[i:i+4]
        value = 0

        for bit in group:
            value = value * 2 + int(bit)

        hexadecimal += hex_chars[value]

    return hexadecimal.lstrip("0") or "0"


def write_results(results):
    """
    Writes conversion results to a file.

    Args:
        results (str): Formatted results.
    """
    with open("ConversionResults.txt", "w", encoding="utf-8") as file:
        file.write(results)


def main():
    """
    Main execution function.
    """
    if len(sys.argv) < 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    start_time = time.time()

    numbers = read_numbers(file_name)

    output_lines = []
    output_lines.append("Conversion Results")
    output_lines.append("-------------------")

    for number in numbers:
        binary = decimal_to_binary(number)
        hexadecimal = binary_to_hexadecimal(binary, number)

        line = (
            f"Decimal: {number} | "
            f"Binary: {binary} | "
            f"Hexadecimal: {hexadecimal}"
        )

        print(line)
        output_lines.append(line)

    elapsed_time = time.time() - start_time
    time_line = f"\nExecution Time: {elapsed_time:.6f} seconds"

    print(time_line)
    output_lines.append(time_line)

    write_results("\n".join(output_lines))


if __name__ == "__main__":
    main()
