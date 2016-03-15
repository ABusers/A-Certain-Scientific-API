import requests as r
import requests_cache
from datetime import timedelta
import errors as e
from functools import wraps
from parser import parse


# Requests method with caching
r_cache = requests_cache.CachedSession(expire_after=timedelta(hours=6))


def _require_login(func):
    """Decorator that throws an error when user isn't logged in."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # args[0] will always be self
        if not args[0].logged_in:
            raise e.LoginRequired('must be logged in')
        return func(*args, **kwargs)
    return wrapper


class Funimation(object):
    def __init__(self, username=None, password=None):
        self.headers = {'userName': 'none',
                        'userType': 'FunimationSubscriptionUser',
                        'userRole': 'All-AccessPass',
                        'userAge': '18', 'userId': '0',
                        'Authorization': '12345'}
        self.logged_in = False
        self.base_url = 'https://api-funimation.dadcdigital.com/xml/'
        '''
        All sub urls will not have a preceding slash
        The reason for this is the url that fetches all submenus doesn't follow
        this convention.
        '''
        self.menus = 'mobile/menu/?territory=US'

    def login(self, username, password):
        """Login and set the authentication headers
        Args:
            username (str):
            password (str):
        Code by sinap
        """
        resp = parse(r.post(self.base_url+'auth/login/?',
                                {'username': username, 'password': password}).text)
        if 'error' in resp:
            raise e.AuthenticationFailed('username or password is incorrect')
        # the API returns what headers should be set
        self.headers=resp['authentication']['parameters']['header']
        self.logged_in = True

    @_require_login
    def get_history(self):
        resp = parse(r.get(self.base_url+'history/get-items/?',headers=self.headers).text)
