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


def get_bonus_points(password, common_passw_list=None):
    if common_passw_list:
        blacklist_password_check = True
        blacklist_password_check = password not in common_passw_list
        lower_upper_characters = check_characters(password)
        spec_character_check = any(char for char in password if char in punctuation)
    else:
        blacklist_password_check = False
        lower_upper_characters = check_characters(password)
        spec_character_check = any(char for char in password if char in punctuation)
    return sum([num for num in (blacklist_password_check, lower_upper_characters, spec_character_check)])


def get_password_strength(password, bonus_points=0):
    alphabetSize = len(set(password)) + 1 + bonus_points
    count_bits = int(log2(alphabetSize) * len(password))
    if count_bits <= 5:
        return 1
    elif 6 <= count_bits <= 14:
        return 2
    elif 15 <= count_bits <= 19:
        return 3
    elif 20 <= count_bits <= 24:
        return 4
    elif 25 <= count_bits <= 29:
        return 5
    elif 30 <= count_bits <= 35:
        return 6
    elif 36 <= count_bits <= 39:
        return 7
    elif 40 <= count_bits <= 45:
        return 8
    elif 46 <= count_bits <= 49:
        return 9
    elif count_bits >= 50:
        return 10


if __name__ == '__main__':
    password_list_from_text = load_password_list('./most_common_passwords.txt')
    users_password = input('\nEnter your password> ')
    get_bonus_for_complexity = get_bonus_points(users_password, password_list_from_text)
    print(get_password_strength(users_password, get_bonus_for_complexity))
