import argparse
import textwrap
import sys


class MyParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(MyParser, self).__init__(*args, **kwargs)
        self.prog = 'Password complexity'
        self.formatter_class = argparse.RawDescriptionHelpFormatter
        self.description = textwrap.dedent('''\
                      Script for password complexity check \n
                      -----------------------------------------------------------------
                      This script needs file for better work:
                      *most_common_passwords.txt - list of bad passwords according to \
                                                 the investigations of data breaches \
                                                and hack attacks in 2015.

                      If you want to stop the program press Ctrl+C.
                      ------------------------------------------------------------------
                      This program had been tested on Python 3.5.2.
                      ''')
        self.add_argument('--file', nargs='?',
                          help='Paste full path to file with bad passwords,\
                            e.g --file /home/user/documents/most_common_passwords.txt\
                            (default: %(default)s)',
                          type=str, default=None)

    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)

    def check_python_version(self):
        if sys.version_info < (3, 5):
            self.print_help()
            raise SystemExit('\nSorry, this code needs Python 3.5 or higher\n')
