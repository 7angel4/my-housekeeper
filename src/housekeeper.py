import argparse
from constants import *

import credentials
import accounting

def cli():
    global_parser = argparse.ArgumentParser(prog=APP_NAME)
    subparsers = global_parser.add_subparsers(
        title='commands', help='functionalities', dest='command'
    )
    
    credentials_parser = subparsers.add_parser(CREDENTIALS, help='credentials manager')
    credentials.subparsers(credentials_parser)

    accounting_parser = subparsers.add_parser(ACCOUNTING, help='accountant')
    accounting.subparsers(accounting_parser)

    return global_parser.parse_args()

def main():
    args = cli()
    if args.command == CREDENTIALS:
        credentials.handle_cli(args)
    elif args.command == ACCOUNTING:
        accounting.handle_cli(args)
    else:
        print('Unknown command')

if __name__ == '__main__':
    main()
