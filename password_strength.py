import getpass
import argparse
import textwrap
import sys
from os import path
from math import log2
from string import punctuation

RANGES_FOR_CONVERTING_BITS = [(1, 6), (6, 14), (14, 19), (19, 24),
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
        blacklist_password_check = 1.0 if password not in bad_passwords_list else 0
        any_char_is_in_upper_case = any(char.isupper() for char in password)
        any_char_is_in_lower_case = any(char.islower() for char in password)
        bonus_for_lower_or_upper_case_character = 1.0 if all((any_char_is_in_upper_case,
                                                              any_char_is_in_lower_case)) else 0.5
        spec_character_check = any(char for char in password if char in punctuation)
    else:
        blacklist_password_check = 0
        any_char_is_in_upper_case = any(char.isupper() for char in password)
        any_char_is_in_lower_case = any(char.islower() for char in password)
        bonus_for_lower_or_upper_case_character = 1.0 if all((any_char_is_in_upper_case,
                                                              any_char_is_in_lower_case)) else 0.5
        spec_character_check = any(char for char in password if char in punctuation)
    bonus_points_for_complexity = sum([num for num in (blacklist_password_check,
                                                       bonus_for_lower_or_upper_case_character,
                                                       spec_character_check)])
    count_unique_chars = len(set(password)) + 1 + bonus_points_for_complexity
    return int((log2(count_unique_chars) * len(password)) / 2)


def convert_bits_to_points(number_of_bits, RANGES_FOR_CONVERTING_BITS=RANGES_FOR_CONVERTING_BITS):
    return [index for index, bits_range in enumerate(RANGES_FOR_CONVERTING_BITS)
            if number_of_bits in range(*bits_range)]


if __name__ == '__main__':
    parser = create_parser()
    parser.check_python_version()
    args = parser.parse_args()
    bad_passwords_list = load_password_list(args.file) if args.file else None
    user_password = getpass.getpass(prompt='\nEnter your password> ', stream=None)
    overall_password_complexity = get_password_strength_in_bits(user_password, bad_passwords_list)
    print(convert_bits_to_points(overall_password_complexity)[0])
