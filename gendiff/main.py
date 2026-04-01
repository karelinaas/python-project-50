import argparse
import json
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    
    args = parser.parse_args()

    with open(args.first_file, "r") as f:
        first_file_data = json.load(f)

    with open(args.second_file, "r") as f:
        second_file_data = json.load(f)

    diff_result = generate_diff(first_file_data, second_file_data)
    print(diff_result)


if __name__ == "__main__":
    main()
