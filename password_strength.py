'''

    the use of both upper-case and lower-case letters (case sensitivity)
    inclusion of one or more numerical digits
    inclusion of special characters, such as @, #, $
    prohibition of words found in a password blacklist
    prohibition of words found in the user's personal information
    prohibition of use of company name or an abbreviation
    prohibition of passwords that match the format of calendar dates, license plate numbers, telephone numbers, or other common numbers

'''
# from sys import argv
from os import path


def load_password_list(filepath):
    if not path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='cp1251') as file:
        return [line.strip() for line in file.readlines()]


def get_password_strength(password, common_passw_list=None):
    if common_passw_list:
        pass
    else:
        password_len = 
        upper_case_check = any(char.isupper() for char in password)
        lower_upper_case_check = any(char.islower() for char in password)


if __name__ == '__main__':
    password_list_from_text = load_password_list('./most_common_passwords.txt')
    users_password = input('\nEnter your password> ')
    print(get_password_strength(users_password))
    # print(password_list_from_text)
