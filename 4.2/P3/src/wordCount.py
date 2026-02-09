"""
wordCount.py

Reads a text file and counts the frequency of each distinct word.
Results are printed to the console and written to WordCountResults.txt.
Invalid data is reported but execution continues.
Execution time is displayed and recorded.
"""

# pylint: disable=invalid-name

import sys
import time


def read_words(file_name):
    """
    Reads words from a file and returns a list of words.

    Args:
        file_name (str): File containing text data.

    Returns:
        list: List of words found in the file.
    """
    words = []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    print(f"Empty line at {line_number}")
                    continue

                current_word = ""

                for char in line:
                    if char.isalnum():
                        current_word += char.lower()
                    else:
                        if current_word:
                            words.append(current_word)
                            current_word = ""

                if current_word:
                    words.append(current_word)

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    if not words:
        print("Error: No valid words found in file.")
        sys.exit(1)

    return words


def count_words(words):
    """
    Counts the frequency of each distinct word.

    Args:
        words (list): List of words.

    Returns:
        dict: Dictionary with word frequencies.
    """
    frequencies = {}

    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    return frequencies


def write_results(results):
    """
    Writes the word count results to a file.

    Args:
        results (str): Formatted results.
    """
    with open("WordCountResults.txt", "w", encoding="utf-8") as file:
        file.write(results)


def sort_frequencies(frequencies):
    """
    Sorts the word frequencies in descending order
    using a basic selection sort algorithm.

    Args:
        frequencies (dict): Word frequency dictionary.

    Returns:
        list: Sorted list of tuples (word, count).
    """
    items = list(frequencies.items())
    n = len(items)

    for i in range(n):
        max_index = i

        for j in range(i + 1, n):
            if items[j][1] > items[max_index][1]:
                max_index = j

        items[i], items[max_index] = items[max_index], items[i]

    return items


def main():
    """
    Main execution function.
    """
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    start_time = time.time()

    words = read_words(file_name)
    frequencies = count_words(words)

    output_lines = []
    output_lines.append("Word Count Results")
    output_lines.append("------------------")

    sorted_words = sort_frequencies(frequencies)

    for word, count in sorted_words:
        line = f"{word}: {count}"
        print(line)
        output_lines.append(line)

    elapsed_time = time.time() - start_time
    time_line = f"\nExecution Time: {elapsed_time:.6f} seconds"

    print(time_line)
    output_lines.append(time_line)

    write_results("\n".join(output_lines))


if __name__ == "__main__":
    main()
