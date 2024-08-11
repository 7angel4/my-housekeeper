from database import Database
from constants import *
import argparse

class UserExistsException(Exception):
    """
    Exception raised when trying to add a password to a site and username 
    that already has a password.
    """
    def __init__(self):
        super().__init__('Password already exists for the given site and username')

class IncorrectPasswordException(Exception):
    """
    Exception raised when entered password does not match the stored password.

    Attributes:
        password -- input password which caused the error
        message -- explanation of the error
    """
    def __init__(self, password, message=f'Incorrect password'):
        self.password = password
        self.message = message
        super().__init__(self.message)

class CredentialsManager:
    def __init__(self):
        self.db = Database()

    def _add(self, site, username, password):
        query = f'INSERT INTO {CREDENTIALS} (site, username, password) VALUES (?, ?, ?)'
        self.db.execute_query(query, (site, username, password))        

    def username_exists(self, site, username):
        query = f"SELECT 1 FROM {CREDENTIALS} WHERE site = '{site}' AND username = '{username}'"
        return True if self.db.fetch_query(query) else False
        
    def get_credentials(self, site):
        query = f"SELECT username, password FROM {CREDENTIALS} WHERE site = '{site}'"
        result = self.db.fetch_query(query)
        return result if result else None

    def get_password(self, site, username):
        query = f'SELECT password FROM {CREDENTIALS} WHERE site = ? AND username = ?'
        result = self.db.fetch_query(query, (site, username))
        return result[0][0] if result else None

    def add_credentials(self, site, username, password):
        # check if password already exists
        if self.username_exists(site, username):
            raise UserExistsException(password)
        self._add(site, username, password)

    def update_password(self, site, username, input_password, new_password):
        if input_password != self.get_password(site, username):
            raise IncorrectPasswordException(input_password)
        query = f'''UPDATE {CREDENTIALS} 
                    SET password = ?
                    WHERE site = ? AND username = ?'''
        self.db.execute_query(query, (new_password, site, username))
    
    def delete_site(self, site):
        self.db.execute_query(f'DELETE FROM {CREDENTIALS} WHERE site = {site}')
    
    def delete_credentials(self, site, username):
        self.db.execute_query(f"DELETE FROM {CREDENTIALS} \
                              WHERE site = '{site}' AND username = '{username}'")
        
    def print_credential(self, username, password):
        print(f'{"USERNAME":10s}:', username)
        print(f'{"PASSWORD":10s}:', password)

def subparsers(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', help='actions on credentials', dest='action'
    )

    # add credentials
    add_parser = subparsers.add_parser('add', help='Add a new credential')
    add_parser.add_argument('-s', '--site', required=True, help='site name')
    add_parser.add_argument('-u', '--username', required=True, help='username')
    add_parser.add_argument('-p', '--password', required=True, help='password')

    # update credentials
    update_parser = subparsers.add_parser('update', help='Update a credential')
    update_parser.add_argument('-s', '--site', required=True, help='site name')
    update_parser.add_argument('-u', '--username', required=True, help='username')
    update_parser.add_argument('-op', '--old-password', required=True, help='old password')
    update_parser.add_argument('-np', '--new-password', required=True, help='new password')

    # get credentials
    get_parser = subparsers.add_parser('get', help='Get credential(s)')
    get_parser.add_argument('-s', '--site', required=True, help='site name')
    get_parser.add_argument('-u', '--username', required=False, help='username (if not provided, lists all stored credentials)')

    # delete credentials
    del_parser = subparsers.add_parser('delete', help='Delete a credential')
    del_parser.add_argument('-s', '--site', required=True, help='site name')
    del_parser.add_argument('-u', '--username', required=True, help='username')

    return subparsers

def handle_cli(args):
    cm = CredentialsManager()
    if args.action == 'add':
        cm.add_credentials(args.site, args.username, args.password)
        print('Added password for', args.site)
    elif args.action == 'update':
        cm.update_password(args.site, args.username, args.old_password, args.new_password)
        print('Updated password for', args.site)
    elif args.action == 'get':
        if args.username:
            cm.print_credential(args.username, cm.get_password(args.site, args.username))
        else:
            credentials = cm.get_credentials(args.site)
            if credentials:
                for username, password in credentials:
                    cm.print_credential(username, password)
                    print()
            else:
                print('No password found for', args.site)
    elif args.action == 'delete':
        cm.delete_credentials(args.site, args.username)
        print('Deleted credentials for', args.site)
   
