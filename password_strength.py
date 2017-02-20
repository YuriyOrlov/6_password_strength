import getpass
import argparse
import textwrap
import sys
from os import path
from math import log2
from string import punctuation


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


def acquire_bonus_points_for_characters(password):
    is_chars_upper_case = any(char.isupper() for char in password)
    is_chars_lower_case = any(char.islower() for char in password)
    if all((is_chars_upper_case, is_chars_lower_case)):
        return 1.0
    else:
        return 0.5


def gain_complexity_bonus_points(password, common_passw_list=None):
    if common_passw_list:
        blacklist_password_check = 1.0 if password not in common_passw_list else 0
        lower_upper_characters = acquire_bonus_points_for_characters(password)
        spec_character_check = any(char for char in password if char in punctuation)
    else:
        blacklist_password_check = 0
        lower_upper_characters = acquire_bonus_points_for_characters(password)
        spec_character_check = any(char for char in password if char in punctuation)
    return sum([num for num in (blacklist_password_check, lower_upper_characters, spec_character_check)])


def get_password_strength_in_bits(password, password_list_from_text=None):
    get_bonus_for_complexity = gain_complexity_bonus_points(user_password, password_list_from_text)
    count_unique_chars = len(set(password)) + 1 + get_bonus_for_complexity
    return int((log2(count_unique_chars) * len(password)) / 2)


def convert_bits_to_points(number_of_bits):
    ranges = {1: (1, 6),
              2: (6, 14),
              3: (14, 19),
              4: (19, 24),
              5: (24, 29),
              6: (29, 35),
              7: (35, 39),
              8: (39, 45),
              9: (45, 50),
              10: (50, 1000)}
    for key, value in ranges.items():
        if number_of_bits in range(*value):
            return key


if __name__ == '__main__':
    parser = create_parser()
    parser.check_python_version()
    args = parser.parse_args()
    password_list_from_text = load_password_list(args.file) if args.file else None
    print(password_list_from_text)
    user_password = getpass.getpass(prompt='\nEnter your password> ', stream=None)
    get_password_complexity = get_password_strength_in_bits(user_password, password_list_from_text)
    print(convert_bits_to_points(get_password_complexity))
