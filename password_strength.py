import getpass
import argparse
import textwrap
import sys
from os import path
from math import log2
from string import punctuation

ENTROPY_BITS = [(1, 6), (6, 14), (14, 19), (19, 24),
                (24, 29), (29, 35), (35, 39), (39, 45),
                (45, 50), (50, 1000)]


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)

    def check_python_version(self):
        if sys.version_info < (3, 5):
            self.print_help()
            raise SystemExit('\nSorry, this code needs Python 3.5 or higher\n')


def create_parser():
    parser = MyParser(prog='Password complexity', formatter_class=argparse.RawDescriptionHelpFormatter,
                      description=textwrap.dedent('''\
                      Script for password complexity check \n
                      -----------------------------------------------------------------
                      This script needs file for better work:
                      *most_common_passwords.txt - list of bad passwords according to \
                                                 the investigations of data breaches \
                                                and hack attacks in 2015.

                      If you want to stop the program press Ctrl+C.
                      ------------------------------------------------------------------
                      This program had been tested on Python 3.5.2.
                      '''))
    parser.add_argument('--file', nargs='?',
                        help='Paste full path to file with bad passwords,\
                              e.g --file /home/user/documents/most_common_passwords.txt\
                              (default: %(default)s)',
                        type=str, default=None)
    return parser


def load_password_list(filepath):
    if not path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def get_password_strength_in_bits(password, bad_passwords_list=None):
    if bad_passwords_list:
        password_in_blacklist = True if password not in bad_passwords_list else False
        has_uppercase_chars = any(char.isupper() for char in password)
        has_lowercase_chars = any(char.islower() for char in password)
        letter_case_bonus = 1.0 if all((has_uppercase_chars,
                                        has_lowercase_chars)) else 0.5
        has_special_chars = any(char for char in password if char in punctuation)
    else:
        password_in_blacklist = False
        has_uppercase_chars = any(char.isupper() for char in password)
        has_lowercase_chars = any(char.islower() for char in password)
        letter_case_bonus = 1.0 if all((has_uppercase_chars,
                                        has_lowercase_chars)) else 0.5
        has_special_chars = any(char for char in password if char in punctuation)
    bonus_points = sum([num for num in (password_in_blacklist,
                                        letter_case_bonus,
                                        has_special_chars)])
    complexity_points = len(set(password)) + 1 + bonus_points
    return int((log2(complexity_points) * len(password)) / 2)


def convert_bits_to_points(number_of_bits, ENTROPY_BITS=ENTROPY_BITS):
    return [index for index, bits_range in enumerate(ENTROPY_BITS)
            if number_of_bits in range(*bits_range)]


if __name__ == '__main__':
    parser = create_parser()
    parser.check_python_version()
    args = parser.parse_args()
    bad_passwords_list = load_password_list(args.file) if args.file else None
    user_password = getpass.getpass(prompt='\nEnter your password> ', stream=None)
    overall_password_complexity = get_password_strength_in_bits(user_password, bad_passwords_list)
    print(convert_bits_to_points(overall_password_complexity)[0])
