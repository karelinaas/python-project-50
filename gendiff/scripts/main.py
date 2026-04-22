import argparse
from gendiff import generate_diff
from gendiff.scripts.parser import parse_file


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    parser.add_argument(
        "-f",
        "--format",
        default="stylish",
        help="Output format (default: stylish)",
    )
    
    args = parser.parse_args()

    first_file_data = parse_file(args.first_file)
    second_file_data = parse_file(args.second_file)

    diff_result = generate_diff(first_file_data, second_file_data, args.format)
    print(diff_result)


if __name__ == "__main__":
    main()
