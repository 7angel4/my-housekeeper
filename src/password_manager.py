from database import Database
from constants import *

class PasswordExistsException(Exception):
    """
    Exception raised when trying to add a password to a site and username 
    that already has a password.

    Attributes:
        password -- input password which caused the error
        message -- explanation of the error
    """
    def __init__(self, password, message=f'Password already exists for the given site and username'):
        self.password = password
        self.message = message
        super().__init__(self.message)

class PasswordManager:
    def __init__(self):
        self.db = Database()

    def _add(self, site, username, password):
        query = f'INSERT INTO {CREDENTIALS} (site, username, password) VALUES (?, ?, ?)'
        self.db.execute_query(query, (site, username, password))        

    def get_credentials(self, site):
        query = f'SELECT username, password FROM {CREDENTIALS} WHERE site = ?'
        result = self.db.fetch_query(query, (site,))
        return result if result else None

    def get_password(self, site, username):
        query = f'SELECT password FROM {CREDENTIALS} WHERE site = ? AND username = ?'
        result = self.db.fetch_query(query, (site, username))
        if result:
            return result[0]
        return None

    def add_credentials(self, site, username, password):
        self._add(site, username, password)

    def add_password(self, site, username, password):
        # check if password already exists
        if self.get_password(self, site):
            raise PasswordExistsException(password)
        self._add(site, username, password)

    def update_password(self, site, username, password):
        query = f'''UPDATE {CREDENTIALS} 
                    SET password = ?
                    WHERE site = ? AND username = ?'''
        self.db.execute_query(query, (password, site, username))
    
    def delete_site(self, site):
        self.db.execute_query(f'DELETE FROM {CREDENTIALS} WHERE site = {site}')
    
    def delete_credentials(self, site, username):
        self.db.execute_query(f'''DELETE FROM {CREDENTIALS} 
                              WHERE site = {site} AND username = {username}''')