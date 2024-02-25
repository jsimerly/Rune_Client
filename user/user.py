class User:
    _instance = None
    is_logged_in = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(User, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, username=None):
        if username is not None:
            self.username = username
            self.is_logged_in = True

    def serialize(self):
        return {'username': self.username}