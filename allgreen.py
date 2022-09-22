from datetime import date, timedelta
from random import randint
import random
import string
import sys
import os

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

try:
    start_year = int(sys.argv[1])
    start_month = int(sys.argv[2])
    start_day = int(sys.argv[3])
    end_year = int(sys.argv[4])
    end_month = int(sys.argv[5])
    end_day = int(sys.argv[6])
except:
    print("There is something wrong with your input values... Please try again...")

start_date = date(start_year, start_month, start_day)
end_date = date(end_year, end_month, end_day)

try:
    for single_date in daterange(start_date, end_date):
        for commits in range(3, randint(4, 10)):
            n = get_random_string(8)
            with open("file.txt", "a") as file:
                file.write(n)
            os.system("git add .")
            os.system(f"git commit -m {n} --date={str(single_date)}")
    os.system("git push -u origin main")
except KeyboardInterrupt:
    print("Terminating...")
    exit()