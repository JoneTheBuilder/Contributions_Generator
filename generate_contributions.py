from datetime import date, timedelta
from random import randint
import random
import string
import sys
import os


def daterange(start_date, end_date):
    """
    Generate a range of dates between start_date and end_date.

    Args:
        start_date (datetime.date): The start date.
        end_date (datetime.date): The end date.

    Yields:
        datetime.date: The dates in the range.
    """
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def get_random_string(length=8):
    """
    Generate a random string of lowercase letters.

    Args:
        length (int): Length of the generated string. Default is 8.

    Returns:
        str: A random string of lowercase letters.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def main():
    """
    Generate Git contributions based on command-line arguments.

    This script generates Git contributions with random commit messages
    on specified dates between a start and end date provided as command-line arguments.
    """
    if len(sys.argv) != 7:
        print("Usage: python3 generate_contributions.py <start_year> <start_month> <start_day> <end_year> <end_month> <end_day>")
        return

    try:
        start_year = int(sys.argv[1])
        start_month = int(sys.argv[2])
        start_day = int(sys.argv[3])
        end_year = int(sys.argv[4])
        end_month = int(sys.argv[5])
        end_day = int(sys.argv[6])
    except ValueError:
        print("Invalid date input. Please enter integers for year, month, and day.")
        return

    try:
        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)
    except ValueError as e:
        print(f"Error in date conversion: {e}")
        return

    for single_date in daterange(start_date, end_date):
        for _ in range(3, randint(10, 100)):
            commit_message = get_random_string()
            with open("file.txt", "a") as file:
                file.write(commit_message + "\n")
            os.system("git add .")
            formatted_date = single_date.strftime("%a %b %d %H:%M:%S %Y %z")
            if os.name == 'nt':  # Check if the OS is Windows
                os.system(f'set GIT_COMMITTER_DATE="{formatted_date}" && git commit -m "{commit_message}" --date="{formatted_date}"')
            else:  # For Unix-like systems
                os.system(f'GIT_COMMITTER_DATE="{formatted_date}" git commit -m "{commit_message}" --date="{formatted_date}"')


    os.system("git push -u origin main")

    # Clean up temporary file
    try:
        os.remove("file.txt")
    except OSError as e:
        print(f"Error deleting file: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted. Exiting...")
        sys.exit(0)
