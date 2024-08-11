import argparse
from pathlib import Path
from constants import *

import credentials

def cli():
    global_parser = argparse.ArgumentParser(prog=APP_NAME)
    subparsers = global_parser.add_subparsers(
        title='commands', help='functionalities', dest='command'
    )
    # password manager
    credentials_parser = subparsers.add_parser('credentials', help='credentials manager')
    credentials.subparsers(credentials_parser)

    return global_parser.parse_args()

def main():
    args = cli()
    if args.command == 'credentials':
        credentials.handle_cli(args)
    else:
        print('Unknown command')

if __name__ == '__main__':
    main()
