class User:
    _instance = None
    is_logged_in = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(User, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        return cls._instance

    def init(self, user: dict):
        if user is not None:
            self.username = user['username']
            User.is_logged_in = True

    @property
    def serialized(self):
        return {'username': self.username}