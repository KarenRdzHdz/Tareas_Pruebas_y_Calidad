"""
computeStatistics.py

This program reads a file containing numeric data and computes
descriptive statistics such as mean, median, mode, variance,
and standard deviation using basic algorithms.

The program handles invalid data, prints the results to the
console, writes them to StatisticsResults.txt, and displays
execution time.
"""
# pylint: disable=invalid-name

import sys
import time


def read_numbers(file_name):
    """
    Reads numeric values from a file.

    Invalid data is reported but does not stop execution.

    Args:
        file_name (str): Name of the file containing numbers.

    Returns:
        list: A list of valid float numbers.
    """
    numbers = []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                value = line.strip()

                try:
                    number = float(value)
                    numbers.append(number)
                except ValueError:
                    print(
                        f"Invalid data at line {line_number}: '{value}'"
                    )

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    if not numbers:
        print("Error: No valid numbers found in the file.")
        sys.exit(1)

    return numbers


def mean(numbers):
    """
    Calculates the mean (average) of a list of numbers.

    Args:
        numbers (list): List of numeric values.

    Returns:
        float: Mean of the numbers.
    """
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def median(numbers):
    """
    Calculates the median of a list of numbers.

    Args:
        numbers (list): List of numeric values.

    Returns:
        float: Median value.
    """
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    middle = n // 2

    if n % 2 == 0:
        return (sorted_numbers[middle - 1] +
                sorted_numbers[middle]) / 2
    return sorted_numbers[middle]


def mode(numbers):
    """
    Calculates the mode (most frequent value).

    Args:
        numbers (list): List of numeric values.

    Returns:
        float: Mode of the numbers.
    """
    frequency = {}

    for num in numbers:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    max_count = 0
    mode_value = None

    for num, count in frequency.items():
        if count > max_count:
            max_count = count
            mode_value = num

    return mode_value


def variance(numbers, avg):
    """
    Calculates the variance of a list of numbers.

    Args:
        numbers (list): List of numeric values.
        avg (float): Mean of the numbers.

    Returns:
        float: Variance.
    """
    total = 0

    for num in numbers:
        diff = num - avg
        total += diff * diff

    return total / len(numbers)


def standard_deviation(var):
    """
    Calculates the standard deviation.

    Args:
        var (float): Variance.

    Returns:
        float: Standard deviation.
    """
    # raíz cuadrada sin usar math
    return var ** 0.5


def write_results(results):
    """
    Writes the statistics results to a file.

    Args:
        results (str): Formatted statistics results.
    """
    with open("StatisticsResults.txt", "w",
              encoding="utf-8") as file:
        file.write(results)


def main():
    """
    Main function that orchestrates file reading,
    statistics calculation, and result output.
    """
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    start_time = time.time()

    numbers = read_numbers(file_name)

    avg = mean(numbers)
    med = median(numbers)
    mod = mode(numbers)
    var = variance(numbers, avg)
    std_dev = standard_deviation(var)

    elapsed_time = time.time() - start_time

    results = (
        f"Statistics Results\n"
        f"-------------------\n"
        f"Count: {len(numbers)}\n"
        f"Mean: {avg}\n"
        f"Median: {med}\n"
        f"Mode: {mod}\n"
        f"Standard Deviation: {std_dev}\n"
        f"Variance: {var}\n"
        f"Execution Time: {elapsed_time:.6f} seconds\n"
    )

    print(results)
    write_results(results)


if __name__ == "__main__":
    main()
