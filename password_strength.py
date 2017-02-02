import getpass
from os import path
from math import log2
from string import punctuation


def load_password_list(filepath):
    if not path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='cp1251') as file:
        return [line.strip() for line in file.readlines()]


def check_characters(password):
    upper_case_check = any(char.isupper() for char in password)
    lower_case_check = any(char.islower() for char in password)
    if all((upper_case_check, lower_case_check)):
        return 1.0
    else:
        return 0.5


def get_complexity_bonus_points(password, common_passw_list=None):
    if common_passw_list:
        blacklist_password_check = False
        blacklist_password_check = password not in common_passw_list
        lower_upper_characters = check_characters(password)
        spec_character_check = any(char for char in password if char in punctuation)
    else:
        blacklist_password_check = False
        lower_upper_characters = check_characters(password)
        spec_character_check = any(char for char in password if char in punctuation)
    return sum([num for num in (blacklist_password_check, lower_upper_characters, spec_character_check)])


def get_password_strength_in_bits(password, bonus_points=0):
    count_unique_chars = len(set(password)) + 1 + bonus_points
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
        if number_of_bits in range(value[0], value[1]):
            return key


if __name__ == '__main__':
    password_list_from_text = load_password_list('./most_common_passwords.txt')
    user_password = getpass.getpass(prompt='\nEnter your password> ', stream=None)
    get_bonus_for_complexity = get_complexity_bonus_points(user_password, password_list_from_text)
    get_password_complexity = get_password_strength_in_bits(user_password, get_bonus_for_complexity)
    print(convert_bits_to_points(get_password_complexity))
